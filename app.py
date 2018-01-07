from flask import *
from flask_socketio import SocketIO
from mlab import *

from utils.code import code_6
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


def get_voter_code():
    voter_code = session.get('voter_code', None)
    if voter_code is None:
        voter_code = code_6()
        session['voter_code'] = voter_code
    return voter_code

def is_poll_owner(poll):
    owned_poll_code = session.get('owned_poll_code', None)
    return owned_poll_code == poll.code

def get_owned_poll_code():
    return session.get('owned_poll_code', None)

@app.route('/poll/<poll_code>', methods=['GET', 'POST'])
def poll(poll_code):
    poll = Poll.objects(code=poll_code.upper()).first()
    if poll is None:
        return "<h2>Poll not found</h2>"
    elif is_poll_owner(poll):
        return redirect(url_for("poll_stats", poll_code=poll.code))
    elif request.method == 'GET':
            print(poll.code, get_voter_code())
            vote = Vote.find(poll, get_voter_code())
            print(vote)
            # User already voted?
            if vote is not None:
                ## Yes, then return their vote status
                return redirect(url_for('vote', vote_id=vote.id))
            else:
                ## No, show them the poll to vote
                poll.choices = Choice.objects(poll=poll)
                return render_template('poll.html', poll=poll)
    elif request.method == "POST":
        form = request.form
        voter_code = get_voter_code()
        voter_name = form['voter_name']
        def criteria(vote_point):
            return -vote_point.point
        vote_points = sorted([VotePoint.create(key, value)
                       for key, value in form.items()
                       if key != 'voter_name'],
                       key=criteria)

        vote = Vote.create(poll, vote_points, voter_name, voter_code)
        vote.save()
        socketio.emit(poll_code, {
            "votes_count": Vote.objects(poll=poll).count()
        })
        return redirect(url_for('vote', vote_id=vote.id))


@app.route('/vote/<vote_id>', methods=['GET', 'POST'])
def vote(vote_id):
    vote = Vote.objects().with_id(vote_id.upper())
    if vote is None or vote.voter_code != get_voter_code():
        return "<h2>Vote not found or you're not owner of this code</h2>"
    elif request.method == 'GET':
        # Does user own this poll
        if is_poll_owner(vote.poll):
            # Yes, just show them the stats
            return redirect(url_for('poll_stats', poll_code=vote.poll.code))
        else:
            # No, show them what they have voted
            return render_template('vote.html', vote=vote)
    elif request.method == 'POST':
        # POST request to delete poll
        poll_code = vote.poll.code
        vote.delete()
        socketio.emit(poll_code, {
            "votes_count": Vote.objects(poll=vote.poll).count()
        })
        return redirect(url_for('poll', poll_code=poll_code))


@app.route("/poll_stats")
def poll_stats_default():
    poll_code = get_owned_poll_code()
    if poll_code is None:
        return "<h2>You are currently not owning any poll</h2>"
    else:
        return redirect(url_for("poll_stats", poll_code=poll_code))


@app.route("/poll_stats/<poll_code>", methods=['GET', 'POST'])
def poll_stats(poll_code):
    poll = Poll.with_code(poll_code)
    poll.votes = Vote.with_poll(poll)
    if not is_poll_owner(poll):
        return "<h2>Poll not found or you are not the owner of this poll</h2>"
    elif request.method == 'GET':
        return render_template("poll_stats.html", poll=poll)
    elif request.method == 'POST':
        poll.choices = Choice.with_poll(poll)
        poll.results = [{
                            "value": choice.value,
                            "total_point": sum([vote.sum_points(choice) for vote in poll.votes])
                        }
                        for choice in poll.choices]
        poll.final_list = poll.results[0: poll.final_pick]
        def criteria(result):
            return result['total_point']
        poll.max_point = max(poll.results, key=criteria)['total_point']

        return render_template("poll_results.html", poll=poll)


if __name__ == '__main__':
  socketio.run(app, port=6969)
