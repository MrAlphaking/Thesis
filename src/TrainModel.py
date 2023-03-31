import os
from finetune_trainer import *
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, T5Tokenizer
from OCR import *
from src.ImageProcessing.ImageProcessor import ImageProcessor
from src.utils.Delpher import Delpher

import DataCreator
# import DataCreator

tokenizer1 = AutoTokenizer.from_pretrained("models/t5-base-dutch-post-correction-50000")
model1 = AutoModelForSeq2SeqLM.from_pretrained("models/t5-base-dutch-post-correction-50000")

tokenizer2 = AutoTokenizer.from_pretrained("models/google-flan-t5-base-post-correction-140000")
model2 = AutoModelForSeq2SeqLM.from_pretrained("models/google-flan-t5-base-post-correction-140000")

def post_correct1(input_text):
    input_ids = tokenizer1.encode(input_text, return_tensors="pt")
    outputs = model1.generate(input_ids, max_length=256, num_beams=1)
    return tokenizer1.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)

def post_correct2(input_text):
    input_ids = tokenizer2.encode(input_text, return_tensors="pt")
    outputs = model2.generate(input_ids, max_length=256, num_beams=1)
    return tokenizer2.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)

def pretty_print(input, expected_output):
    before = input.replace("post-correction: ", "").replace("</s>", "")
    print(f"Before: \t\t\t{before}")
    print(f"Model 1 Generated: \t{post_correct1(input)}")
    print(f"Model 2 Generated: \t{post_correct2(input)}")
    print(f"Should have been: \t{expected_output}")
    print()

# os.environ['OPENCV_LOG_LEVEL']='OFF'

if __name__ == "__main__":
    # trainer = Trainer()
    #
    # df = DataCreator.get_dataframe()
    # df = df.sample(DATASET_SIZE)
    # df['source'] = "post-correction: " + df['source']
    #
    # trainer.start(df)

    # img.show()
    input_text_1 = "post-correction: over de woningbow zei spreckster, dat de vrije bouver wiet am bod kont</s>"
    expected_output_1 = "Over de woningbouw zei spreekster, dat de vrije bouwer niet aan bod komt"
    pretty_print(input_text_1, expected_output_1)

    input_text_2 = "post-correction: Wamt voor een boom, als hij afychouven wordt, is er vervachtyng, dat hij zich nog zal vermderen, en zijn scheut niet zal. ophouden</s>"
    expected_output_2 = "Want voor een boom, als hij afgehouwen wordt, is er verwachting, dat hij zich nog zal veranderen, en zijn scheut niet zal ophouden"
    pretty_print(input_text_2, expected_output_2)

    input_text_3 = "post-correction: De schade is xuin aderhalé niljoen gulden</s>"
    expected_output_3 = "De schade is ruim anderhalf miljoen gulden"
    pretty_print(input_text_3, expected_output_3)

    input_text_4 = "post-correction: 2ij xette het onmiddel1ijk op een lopen, korte tijd later yevolyd door de ona</s>"
    expected_output_4 = "Zij zette het onmiddellijk op een lopen, korte tijd later gevolgd door de hond"
    pretty_print(input_text_4, expected_output_4)

    input_text_5 = "post-correction: Aileen de bestwurder van de luxe vayen werd Licht gevond</s>"
    expected_output_5 = "Alleen de bestuurder van de luxe wagen werd licht gewond"
    pretty_print(input_text_5, expected_output_5)




