from flask import *
from mlab import *
from models.poll import *
from models.choice import *
from mlab import *

mlab_connect()
app = Flask(__name__)
app.config['SECRET_KEY'] = '6QUpegj5qNJnfvqhfkRheHRuLLxXsHPB'


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/create-poll', methods=['GET', 'POST'])
def create_poll():
    if request.method == 'GET':
        return render_template("poll_create.html")
    elif request.method == "POST":
        choice_keys = sorted([key for key, value in request.form.items() if "choice" in key])
        choice_values = [request.form[choice_key] for choice_key in choice_keys]
        final_pick = request.form['final_pick']
        poll = Poll.create(final_pick)
        poll.save()
        for choice_value in choice_values:
            new_choice = Choice(poll=poll, value=choice_value)
            new_choice.save()
        session['owned_poll_code'] = poll.code
        return redirect(url_for('poll', poll_code=poll.code))


@app.route('/poll/<poll_code>')
def poll(poll_code):
    poll_code = poll_code.upper()
    poll = Poll.objects(code=poll_code).first()
    if poll is None:
        return "<h2>Poll not found</h2>"
    else:
        poll.is_owner = session.get('owned_poll_code', None) == poll_code
        poll.choices = Choice.objects(poll=poll)
        return render_template('poll.html', poll=poll)


if __name__ == '__main__':
  app.run(debug=True)
