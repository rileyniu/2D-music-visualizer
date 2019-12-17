from flask import Flask, render_template

app = Flask(__name__)
# app._static_folder = os.path.abspath("static/")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/_func/', methods=['POST'])
def _func():
    print("received POST")
    return "success"

if __name__ == "__main__":
    app.run(debug=True, port=4621)
