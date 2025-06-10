from flask import Flask, render_template, request
from text_summary import summarizer

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = ''
    original_text = ''
    original_len = 0
    summary_len = 0

    if request.method == 'POST':
        original_text = request.form['input_text']
        summary, _, original_len, summary_len = summarizer(original_text)

    return render_template('index.html',
                           original_text=original_text,
                           summary=summary,
                           original_len=original_len,
                           summary_len=summary_len)

if __name__ == '__main__':
    app.run(debug=True)
