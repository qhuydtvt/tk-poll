from flask import *
from flask_socketio import SocketIO, emit
from mlab import *
from models.poll import *
from models.choice import *
from models.vote import *
from mlab import *

mlab_connect()
app = Flask(__name__)
app.config['SECRET_KEY'] = '6QUpegj5qNJnfvqhfkRheHRuLLxXsHPB'
app.config['DEBUG'] = True
app.config['PORT'] = 6969
socketio = SocketIO(app)

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
            if session.get("owned_poll_code", None) == poll.code:
                ## is Owner
                return redirect(url_for("poll_stats", poll_code=poll.code))
            else:
                voter_code = session.get('voter_code', None)
                vote =  Vote.find_by_voter_code(voter_code)
                # User already voted?
                if vote is not None and vote.poll.code == poll_code:
                    ## Yes, then return their vote status
                    return redirect(url_for('vote', voter_code=voter_code))
                else:
                    ## No, show them the poll to vote
                    poll.choices = Choice.objects(poll=poll)
                    return render_template('poll.html', poll=poll)
    else:
        form = request.form
        voter_name = form['voter_name']
        vote_points = [VotePoint.create(key, value) for key,value in form.items() if key != 'voter_name']
        vote = Vote.create(poll=poll, vote_points=vote_points, voter_name=voter_name)
        vote.save()
        emit(poll_code, {
            "votes_count": Vote.objects(poll=poll).count()
        })
        session['voter_code'] = vote.voter_code
        return redirect(url_for('vote', voter_code=vote.voter_code))


@app.route('/vote/<voter_code>', methods=['GET', 'POST'])
def vote(voter_code):
    voter_code = voter_code.upper()
    vote = Vote.objects(voter_code=voter_code).first()
    if vote is not None:
        if request.method == 'GET':
            # Does user own this poll
            if session.get('owned_poll_code', None) == vote.code:
                # Yes, just show them the stats
                return render_template('vote_stats.html')
            else:
                # No, show them what they have voted
                return render_template('vote.html', vote=vote)
        else:
            # POST request to delete poll
            poll_code = vote.poll.code
            vote.delete()
            return redirect(url_for('poll', poll_code=poll_code))
    else:
        return "<h2>Poll not found</h2>"


@app.route("/poll_stats/<poll_code>")
def poll_stats(poll_code):
    poll = Poll.with_code(poll_code)
    if poll is None:
        return "<h2>Poll not found</h2>"
    else:
        votes = Vote.with_poll(poll)
        poll.votes = votes
        return render_template("poll_stats.html", poll=poll)


if __name__ == '__main__':
  socketio.run(app, port=6969)
