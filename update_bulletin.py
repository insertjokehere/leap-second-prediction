#!/usr/bin/env python3
import requests
import roman
import re
import base64
import datetime
import os
import hashlib

"""
Fetches the newest Bulletin A from IERS, and updates the repo using the Gitea API

Bulletins have a (roman numeral formatted!?) Volume number for the year (Vol 1 is 1987, 2021 is Vol 34),
and an issue number for the week of the year. New issues usually come out on Thursdays (UTC).
"""

now = datetime.datetime.utcnow()

LATEST_FILE = "bulletin_a_latest.txt"
REPO = "sites/leap-second-prediction"

with open(LATEST_FILE) as f:
    content = f.read()

current_issue, current_number = re.search("Vol. ([XIV]+) No. ([0-9]+)", content).groups()

expected_issue = roman.toRoman(now.year - 1987)
expected_number = now.strftime("%W").zfill(3)

print(f"Current Bulletin: Vol. {current_issue} No. {current_number}")
print(f"Expected Bulletin: Vol. {expected_issue} No. {expected_number}")

if current_issue.upper() != expected_issue or current_number != expected_number:
    url = "https://datacenter.iers.org/data/6/bulletina-{}-{}.txt".format(expected_issue.lower(), expected_number)
    print(f"Fetching {url}")
    resp = requests.get(url)
    if resp.status_code == 200:
        print("New version found")
        GITEA_API_ROOT = os.environ["GITEA_API_ROOT"]
        GITEA_API_TOKEN = os.environ["GITEA_API_TOKEN"]

        get_resp = requests.get(
            f"{GITEA_API_ROOT}/repos/{REPO}/contents/{LATEST_FILE}",
            headers={
                "Authorization": f"token {GITEA_API_TOKEN}"
            }
        )
        get_resp.raise_for_status()
        existing_sha = get_resp.json()["sha"]

        resp = requests.put(
            f"{GITEA_API_ROOT}/repos/{REPO}/contents/{LATEST_FILE}",
            headers={
                "Authorization": f"token {GITEA_API_TOKEN}"
            },
            json={
                "author": {
                    "email": "leapsecondbot@hhome.me",
                    "name": "Leap Second Bot"
                },
                "branch": "master",
                "committer": {
                    "email": "leapsecondbot@hhome.me",
                    "name": "Leap Second Bot"
                },
                "content": base64.b64encode(resp.text.encode("utf-8")).decode("utf-8"),
                "dates": {
                    "author": now.isoformat() + "Z",
                    "committer": now.isoformat() + "Z"
                },
                "message": f"Update Bulletin to Vol. {expected_issue} No. {expected_number}",
                "sha": existing_sha
            }
        )
        resp.raise_for_status()
    else:
        print("No new version found")
