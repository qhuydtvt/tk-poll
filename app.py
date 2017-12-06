from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/create_poll')
def create_poll():
    return render_template("poll_create.html")

if __name__ == '__main__':
  app.run(debug=True)
