from flask import Flask, render_template, request, jsonify
from transformers import AutoModelWithLMHead, AutoTokenizer

app = Flask(__name__)

tokenizer = AutoTokenizer.from_pretrained("../models/t5-base-dutch-post-correction-50000")
model = AutoModelWithLMHead.from_pretrained("../models/t5-base-dutch-post-correction-50000")

def post_correct(input_text):
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    outputs = model.generate(input_ids, max_length=256, num_beams=1)
    return tokenizer.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)

messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]

@app.route('/')
def index():
    data = {'source:': "This text will be run through the thingy", 'target': post_correct("This text will be run through the thingy")}
    return render_template('index.html', messages=data)

@app.route('/calculate_result')
def calculate_result():
  a = int(request.args.get('val1'))
  b = int(request.args.get('val2'))
  return jsonify({"result":a+b})

if __name__ == "__main__":
    app.run()