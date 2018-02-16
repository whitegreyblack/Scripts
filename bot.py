import click
from slacker import Slacker

def test():
    return "Testing Scheduler with Slack"

def punchin():
    return "Logged in"

def gitpull():
    return "Pull your repos"

def hydrate():
    return "Drink water"

def lunchtime():
    return "Time to eat"

def timesheet():
    return "It's Friday"

def gitpush():
    return "Push your repos"

def punchout():
    return "Logged out"

options={
    'test': test,
    'punchin': punchin,
    'hydrate': hydrate,
    'lunchtime': lunchtime,
    'timesheet': timesheet,
    'gitpush': gitpush,
    'gitpull': gitpull,
    'punchout': punchout,
    }

@click.command()
@click.option('-e', help='Generated Event')
def main(e):
    slack = Slacker('xoxb-217367545728-QShRfL25wcFiyFZKXYRLA7ZN')
    if str(e) in options:
        slack.chat.post_message('#general', (options[e])())

if __name__ == "__main__":
    main()