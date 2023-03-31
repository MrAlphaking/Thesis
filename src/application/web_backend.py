import requests
from flask import Flask, render_template, request, jsonify
from transformers import AutoModelWithLMHead, AutoTokenizer
import random
from src.utils.Util import progress_bar
import string
import requests
from src.utils.Delpher import *
app = Flask(__name__)


tokenizer = AutoTokenizer.from_pretrained("../models/t5-base-dutch-post-correction-50000")
model = AutoModelWithLMHead.from_pretrained("../models/t5-base-dutch-post-correction-50000")
# tokenizer = AutoTokenizer.from_pretrained("../models/google-flan-t5-base-post-correction-140000")
# model = AutoModelWithLMHead.from_pretrained("../models/google-flan-t5-base-post-correction-140000")
task_prefix = 'post-correction: '
delpher = Delpher()
def post_correct(input_text):
    input_text = task_prefix + input_text + "</s>"
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    outputs = model.generate(input_ids, max_length=256, num_beams=1)
    return tokenizer.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)

def post_correct_block(input_text):
    sentences = input_text.split(".")
    return_sentences = sentences

    inputs = tokenizer([task_prefix + sentence + "</s>" for sentence in sentences], return_tensors="pt", padding=True)

    output_sequences = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_length=256,
        num_beams=1,
        do_sample=False,  # disable sampling to test if batching affects output
    )
    output = tokenizer.batch_decode(output_sequences, skip_special_tokens=True)
    print(output)

    return_sentences = zip(return_sentences, output)

    for sentence in return_sentences:
        print(f'{sentence[0]} ----- {sentence[1]}')

    output_string = ""
    for sentence in output:
        output_string += sentence + '. '
    return output_string, return_sentences




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate_result')
def calculate_result():
    # a = int(request.args.get('val1'))
    # b = int(request.args.get('val2'))
    # res = ''.join(random.choices(string.ascii_uppercase +
    #                            string.digits, k=100))

    year = random.randint(1700, 1900)
    response = delpher.query(1940,1950, maximum_records=1)
    for key in response:
        # print(response[key]['ocr'])
        # print(requests.get(response[key]['ocr']).content)

        with urlopen(response[key]['ocr']) as f:
            tree = ET.parse(f)
            root = tree.getroot()
            return_string_source = ""
            return_string_target = ""
            return_sentences_combined = []
            for children in root:
                if children.tag == 'title':
                    return_string_source += f'<h1>{children.text}</h1>'
                    output_string, return_sentences = post_correct_block(children.text)
                    return_sentences_combined.append(return_sentences)
                    return_string_target += f'<h1>{output_string}</h1>'
                if children.tag == 'p':
                    return_string_source += f'<p>{children.text}</p>'
                    output_string, return_sentences = post_correct_block(children.text)
                    return_sentences_combined.append(return_sentences)
                    return_string_target += f'<p>{output_string}</p>'
            # print(return_string_source)
        print("send")
        return jsonify({"source": return_string_source, "target": return_string_target, "image": "image will be here"})
    return jsonify({"result": "No article could be found"})


if __name__ == "__main__":
    app.run()