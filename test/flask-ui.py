from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<html><body><h1>Hello world</h1></body></html>'

@app.route('/hello/<user>')
def hello_name(user):
    return render_template('index.html',name=user)

if __name__ == '__main__':
    app.run(debug=True)