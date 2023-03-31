import os

import numpy as np
from torch import cuda
from torch.utils.data import DataLoader, Dataset
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, T5Tokenizer

import DataCreator
import wandb
from src.utils.Util import *


# PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128



def get_device():
    # return 'cpu'
    return 'cuda' if cuda.is_available() else 'cpu'


class T5Dataset(Dataset):

    def __init__(self, data: pd.DataFrame, tokenizer: T5Tokenizer, source_text_len: int, target_text_len: int,
                 source_attribute: str, target_attribute: str):
        self.__tokenizer = tokenizer

        self.__data = data

        self.__source_text_len = source_text_len

        self.__target_text_len = target_text_len

        self.__source_attribute = source_attribute

        self.__target_attribute = target_attribute

    def __len__(self):
        return len(self.__data)

    def __getitem__(self, index):
        source_text = str(self.__data.iloc[index][self.__source_attribute])

        target_text = str(self.__data.iloc[index][self.__target_attribute])

        source = self.__tokenizer.batch_encode_plus([source_text],
                                                    max_length=self.__source_text_len,
                                                    pad_to_max_length=True,
                                                    truncation=True,
                                                    return_tensors='pt')

        target = self.__tokenizer.batch_encode_plus([target_text],
                                                    truncation=True,
                                                    max_length=self.__target_text_len,

                                                    pad_to_max_length=True,
                                                    return_tensors='pt')

        source_ids = source['input_ids'].squeeze()

        source_mask = source['attention_mask'].squeeze()

        target_ids = target['input_ids'].squeeze()

        return {
            'source_ids': source_ids.to(dtype=TENSOR_DTYPE),
            'source_mask': source_mask.to(dtype=TENSOR_DTYPE),
            'target_ids': target_ids.to(dtype=TENSOR_DTYPE),
            'target_ids_y': target_ids.to(dtype=TENSOR_DTYPE)
        }


class Trainer:

    def train(self, epoch: int, tokenizer: T5Tokenizer, data_loader, model, device, optimizer):
        model.train()

        for _, data in enumerate(data_loader, 0):
            y = data['target_ids'].to(device, dtype=TENSOR_DTYPE)
            y_ids = y[:, :-1].contiguous()
            lm_labels = y[:, 1:].clone().detach()
            lm_labels[y[:, 1:] == tokenizer.pad_token_id] = -100

            ids = data['source_ids'].to(device, dtype=TENSOR_DTYPE)
            mask = data['source_mask'].to(device, dtype=TENSOR_DTYPE)

            outputs = model(input_ids=ids, attention_mask=mask, decoder_input_ids=y_ids, labels=lm_labels)
            loss = outputs[0]

            if _ % 10 == 0:
                wandb.log({"Training Loss": loss.item()})

            if _ % 500 == 0:
                print_telegram(f'Epoch: {epoch}, Loss:  {loss.item()} at {_}')

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        wandb.log({"Epoch Loss": loss.item()})

    def validate(self, tokenizer: T5Tokenizer, model, device, loader):
        model.eval()

        sources = []
        predictions = []
        actuals = []

        with torch.no_grad():
            for _, data in enumerate(loader, 0):
                y = data['target_ids'].to(device, dtype=TENSOR_DTYPE)
                ids = data['source_ids'].to(device, dtype=TENSOR_DTYPE)
                mask = data['source_mask'].to(device, dtype=TENSOR_DTYPE)

                # TODO make sure you modify the max_length and/or the number of beams
                generated_ids = model.generate(
                    input_ids=ids,
                    attention_mask=mask,
                    max_length=32,
                    num_beams=1,
                    repetition_penalty=2.5,
                    length_penalty=1.0,
                    early_stopping=True
                )

                preds = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=True) for g in
                         generated_ids]
                target = [tokenizer.decode(t, skip_special_tokens=True, clean_up_tokenization_spaces=True) for t in y]
                source = [tokenizer.decode(t, skip_special_tokens=True, clean_up_tokenization_spaces=True) for t in ids]

                if _ % 100 == 0:
                    print_telegram(f'Validation completed until {_}')

                predictions.extend(preds)
                actuals.extend(target)
                sources.extend(source)

        return predictions, actuals, sources

    def start(self, df, delimiter: str = "\t"):
        wandb.init(project="thesis-thomas")

        config = wandb.config
        config.TRAIN_BATCH_SIZE = 4
        config.VALID_BATCH_SIZE = 4
        config.TRAIN_EPOCHS = NUMBER_OF_EPOCHS
        config.VAL_EPOCHS = 1
        config.LEARNING_RATE = 0.00005
        config.SEED = 42
        config.SOURCE_MAX_LEN = 256
        config.TARGET_MAX_LEN = 256
        torch.manual_seed(config.SEED)
        np.random.seed(config.SEED)
        torch.backends.cudnn.deterministic = True

        tokenizer = AutoTokenizer.from_pretrained(model_name)

        print_telegram(df.head())

        train_size = 0.985
        train_dataset = df.sample(frac=train_size, random_state=config.SEED)

        val_dataset = df.drop(train_dataset.index).reset_index(drop=True)
        train_dataset = train_dataset.reset_index(drop=True)

        print_telegram("FULL Dataset: {}".format(df.shape))
        print_telegram("TRAIN Dataset: {}".format(train_dataset.shape))
        print_telegram("TEST Dataset: {}".format(val_dataset.shape))

        training_set = T5Dataset(train_dataset, tokenizer, config.SOURCE_MAX_LEN, config.TARGET_MAX_LEN, "source",
                                 "target")

        val_set = T5Dataset(val_dataset, tokenizer, config.SOURCE_MAX_LEN, config.TARGET_MAX_LEN, "source", "target")

        train_params = {
            'batch_size': config.TRAIN_BATCH_SIZE,
            'shuffle': True,
            'num_workers': 0
        }

        val_params = {
            'batch_size': config.VALID_BATCH_SIZE,
            'shuffle': False,
            'num_workers': 0
        }

        training_loader = DataLoader(training_set, **train_params)
        val_loader = DataLoader(val_set, **val_params)

        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        device = get_device()
        model = model.to(device)

        optimizer = torch.optim.Adam(params=model.parameters(), lr=config.LEARNING_RATE, amsgrad=True)

        wandb.watch(model, log="all")

        print_telegram(f'Initiating Fine-Tuning for the model on our dataset, results can be found on {wandb.run.get_url()}')

        for epoch in range(config.TRAIN_EPOCHS):
            self.train(epoch, tokenizer, training_loader, model, device, optimizer)

            for _ in range(config.VAL_EPOCHS):
                predictions, actuals, sources = self.validate(tokenizer, model, device, val_loader)

                final_df = pd.DataFrame({'Source': sources, 'Prediction': predictions, 'Target': actuals})
                final_df.to_csv(f'{MODEL_SAVE_FOLDER}/predictions/predictions-epoch-{epoch}.csv')

                print_telegram('Output Files generated for review')


        tokenizer.save_pretrained(MODEL_SAVE_FOLDER)
        model.save_pretrained(MODEL_SAVE_FOLDER)


if __name__ == '__main__':
    model_name = 'google/flan-t5-base'
    # model_name = 'yhavinga/t5-base-dutch'
    MODEL_SAVE_FOLDER = f'{MODEL_SAVE_FOLDER}{model_name.replace("/","-")}-post-correction-{DATASET_SIZE}'
    if not os.path.exists(MODEL_SAVE_FOLDER + '/predictions'):
        os.makedirs(MODEL_SAVE_FOLDER + '/predictions')
    trainer = Trainer()

    df = DataCreator.get_dataframe()
    df = DataCreator.clean_dataframe(df)
    df = df.sample(DATASET_SIZE)
    df['source'] = "post-correction: " + df['source']

    trainer.start(df)