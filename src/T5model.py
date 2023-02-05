from transformers import T5Tokenizer, T5ForConditionalGeneration, FlaxT5ForConditionalGeneration, AutoTokenizer, FlaxAutoModelForSeq2SeqLM, AutoModelForSeq2SeqLM, pipeline
import torch
# tokenizer = T5Tokenizer.from_pretrained("t5-small")
# model = T5ForConditionalGeneration.from_pretrained("t5-small")

# tokenizer = AutoTokenizer.from_pretrained("t5-base")
# model = AutoModelForSeq2SeqLM.from_pretrained("t5-base")


# tokenizer = AutoTokenizer.from_pretrained("flax-community/t5-base-dutch-demo")
# model = FlaxAutoModelForSeq2SeqLM.from_pretrained("flax-community/t5-base-dutch-demo")
#
# tokenizer = AutoTokenizer.from_pretrained("yhavinga/t5-base-dutch")
# model = T5ForConditionalGeneration.from_pretrained("yhavinga/t5-base-dutch")

# https://huggingface.co/yhavinga/t5-base-36L-ccmatrix-multi
# https://askubuntu.com/questions/1147177/how-to-enable-nvidia
device_num = 0 if torch.cuda.is_available() else -1
device = "cpu" if device_num < 0 else f"cuda:{device_num}"

print(device_num, device)
tokenizer = AutoTokenizer.from_pretrained("yhavinga/t5-small-24L-ccmatrix-multi")
model = AutoModelForSeq2SeqLM.from_pretrained("yhavinga/t5-small-24L-ccmatrix-multi").to(device)
params = {"max_length": 128, "num_beams": 4, "early_stopping": True}
en_to_nl = pipeline("translation_en_to_nl", tokenizer=tokenizer, model=model, device=device_num)
print(en_to_nl("""Young Wehling was hunched in his chair, his head in his hand. He was so rumpled, so still and colorless as to be virtually invisible.""",
               **params)[0]['translation_text'])
nl_to_en = pipeline("translation_nl_to_en", tokenizer=tokenizer, model=model, device=device_num)
print(nl_to_en("""De jonge Wehling zat gebogen in zijn stoel, zijn hoofd in zijn hand. Hij was zo stoffig, zo stil en kleurloos dat hij vrijwel onzichtbaar was.""",
               **params)[0]['translation_text'])



#
# task_prefix = "translate Dutch to English"
# # use different length sentences to test batching
# # sentences = ["The house is wonderful.", "I like to work in NYC."]
# sentences = ["Hallo wie ben jij?", "Leuk u te ontmoeten"]
#
# inputs = tokenizer([task_prefix + sentence for sentence in sentences], return_tensors="pt", padding=True)
# print(inputs)
# output_sequences = model.generate(
#     input_ids=inputs["input_ids"],
#     attention_mask=inputs["attention_mask"],
#     do_sample=False,  # disable sampling to test if batching affects output
# )
#
# print(tokenizer.batch_decode(output_sequences, skip_special_tokens=True))