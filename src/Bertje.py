from transformers import AutoTokenizer, AutoModel, TFAutoModel, RobertaTokenizer, RobertaForSequenceClassification
from happytransformer import  HappyTextToText, TTSettings


# tokenizer = AutoTokenizer.from_pretrained("GroNLP/bert-base-dutch-cased")
# model = AutoModel.from_pretrained("GroNLP/bert-base-dutch-cased")  # PyTorch
# # model = TFAutoModel.from_pretrained("GroNLP/bert-base-dutch-cased")  # Tensorflow
#
# # tokenizer = RobertaTokenizer.from_pretrained("pdelobelle/robbert-v2-dutch-base")
# # model = RobertaForSequenceClassification.from_pretrained("pdelobelle/robbert-v2-dutch-base")
#
# input_text_1 = "grammar: Ik jij hij wil spelen"
# input_ids = tokenizer(input_text_1, return_tensors="pt").input_ids
#
# outputs = model.generate(input_ids, do_sample=False, max_length=30)
# output = tokenizer.batch_decode(outputs, skip_special_tokens=True)

# print(input_text_1)

# https://huggingface.co/yhavinga/t5-base-dutch
# https://huggingface.co/docs/transformers/model_doc/t5
beam_settings =  TTSettings(num_beams=5, min_length=1, max_length=20)
# example_1 = "grammar: dit iss een slechte zin"
example_2 = "translate English to Dutch:: I enjoy writing articles"
happy_tt = HappyTextToText("T5", "yhavinga/t5-base-dutch")
# happy_tt = HappyTextToText("GroNLP/bert-base-dutch-cased")
# happy_tt = HappyTextToText("DTAI-KULeuven/robbert-2022-dutch-base")
# HappyTextToText()

result_2 = happy_tt.generate_text(example_2, args=beam_settings)
print(result_2)


# output_text_1 = happy_tt.generate_text(input_text_1, args=beam_settings)
# print(output_text_1.text)