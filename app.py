from flask import *
from mlab import *
from models.poll import *
from models.choice import *
from mlab import *

mlab_connect()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/create_poll', methods=['GET', 'POST'])
def create_poll():
    if request.method == 'GET':
        return render_template("poll_create.html")
    elif request.method == "POST":
        choice_values = list(request.form.values())
        poll = Poll.create()
        poll.save()
        for choice_value in choice_values:
            new_choice = Choice(poll=poll, value=choice_value)
            new_choice.save()
        return redirect(url_for('poll', poll_code=poll.code))


@app.route('/poll/<poll_code>')
def poll(poll_code):
    poll = Poll.objects(code=poll_code.upper()).first()
    if poll is None:
        return "<h2>Poll not found</h2>"
    else:
        return "HELLO"


if __name__ == '__main__':
  app.run(debug=True)
