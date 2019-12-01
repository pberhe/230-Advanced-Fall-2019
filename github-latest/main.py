"""
1. Receive a GitHub username from the command line.
2. Retrieve a list of "events" associated with that user. User events include things like pushing to a repository or opening up an issue on a repository.
3. Print out the time stamp associated with the first event in that list.
"""

import sys
import json
import requests

def get_response():
    username = sys.argv[1]

    response = requests.get("https://api.github.com/users/{}/events".format(username))
    events = json.loads(response.content)

    print(events[0]['created_at'])

if __name__ == "__main__":
    username = sys.argv[1]

    response = requests.get("https://api.github.com/users/{}/events".format(username))
    events = json.loads(response.content)

    print(events[0]['created_at'])
