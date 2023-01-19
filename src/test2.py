from transformers import T5Tokenizer, T5ForConditionalGeneration, AutoTokenizer, FlaxAutoModelForSeq2SeqLM, AutoModelForSeq2SeqLM

# tokenizer = T5Tokenizer.from_pretrained("t5-small")
# model = T5ForConditionalGeneration.from_pretrained("t5-small")

# tokenizer = AutoTokenizer.from_pretrained("t5-base")
# model = AutoModelForSeq2SeqLM.from_pretrained("t5-base")


tokenizer = AutoTokenizer.from_pretrained("flax-community/t5-base-dutch-demo")
model = FlaxAutoModelForSeq2SeqLM.from_pretrained("flax-community/t5-base-dutch-demo")

# tokenizer = AutoTokenizer.from_pretrained("yhavinga/t5-base-dutch")
# model = FlaxT5ForConditionalGeneration.from_pretrained("yhavinga/t5-base-dutch")

task_prefix = "translate English to Dutch:"
# use different length sentences to test batching
sentences = ["The house is wonderful.", "I like to work in NYC."]

inputs = tokenizer([task_prefix + sentence for sentence in sentences], return_tensors="pt", padding=True)
print(inputs)
output_sequences = model.generate(
    input_ids=inputs["input_ids"],
    attention_mask=inputs["attention_mask"],
    do_sample=False,  # disable sampling to test if batching affects output
)

print(tokenizer.batch_decode(output_sequences, skip_special_tokens=True))