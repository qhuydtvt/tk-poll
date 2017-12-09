from flask import *
from mlab import *
from models.poll import *
from models.choice import *
from models.vote import *
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


@app.route('/poll/<poll_code>', methods=['GET', 'POST'])
def poll(poll_code):
    poll_code = poll_code.upper()
    poll = Poll.objects(code=poll_code).first()
    if request.method == 'GET':
        if poll is None:
            return "<h2>Poll not found</h2>"
        else:
            if 'voter_code' in session:
                voter_code = session['voter_code']
                vote = Vote.objects(voter_code=voter_code).first()
                if vote is not None and vote.poll.code == poll_code:
                    return redirect(url_for('vote', voter_code=voter_code))

            poll.is_owner = session.get('owned_poll_code', None) == poll_code
            poll.choices = Choice.objects(poll=poll)
            return render_template('poll.html', poll=poll)
    else:
        form = request.form
        voter_name = form['voter_name']
        vote_points = [VotePoint.create(key, value) for key,value in form.items() if key != 'voter_name']
        vote = Vote.create(poll=poll, vote_points=vote_points, voter_name=voter_name)
        vote.save()
        session['voter_code'] = vote.voter_code
        return redirect(url_for('vote', voter_code=vote.voter_code))


@app.route('/vote/<voter_code>', methods=['GET', 'POST'])
def vote(voter_code):
    voter_code = voter_code.upper()
    vote = Vote.objects(voter_code=voter_code).first()
    if vote is not None:
        if request.method == 'GET':
            return render_template('vote.html', vote=vote)
        else:
            poll_code = vote.poll.code
            vote.delete()
            return redirect(url_for('poll', poll_code=poll_code))
    else:
        return "Vote not found"



if __name__ == '__main__':
  app.run(debug=True)
