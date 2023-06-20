#!/usr/bin/env python3
import base64
import datetime
import os

import requests
import roman  # type: ignore

from . import BulletinA, bulletins

"""
Fetches the newest Bulletin A from IERS, and updates the repo using the Gitea API

Bulletins have a (roman numeral formatted!?) Volume number for the year (Vol 1 is 1987, 2021 is Vol 34),
and an issue number for the week of the year. New issues usually come out on Thursdays (UTC).
"""

now = datetime.datetime.utcnow()

LATEST_FILE = "bulletin_a/bulletins/latest.txt"
REPO = "sites/leap-second-prediction"


def main():
    with bulletins.LATEST_FILE as f:
        current = BulletinA.parse(f)

    expected_number = int(now.strftime("%W"))
    if now.weekday() < 4:  # Thursday
        expected_number -= 1
    expected_volume = roman.toRoman(now.year - 1987)

    print(f"Current Bulletin: {current.year} No. {current.number}")
    print(f"Expected Bulletin: {now.year} No. {expected_number}")

    if current.year != now.year or current.number != expected_number:
        url = "https://datacenter.iers.org/data/6/bulletina-{}-{}.txt".format(
            expected_volume.lower(), str(expected_number).zfill(3)
        )
        print(f"Fetching {url}")
        resp = requests.get(url)
        if resp.status_code == 200:
            print("New version found")
            GITEA_API_ROOT = os.environ["GITEA_API_ROOT"]
            GITEA_API_TOKEN = os.environ["GITEA_API_TOKEN"]

            get_resp = requests.get(
                f"{GITEA_API_ROOT}/repos/{REPO}/contents/{LATEST_FILE}",
                headers={"Authorization": f"token {GITEA_API_TOKEN}"},
            )
            get_resp.raise_for_status()
            existing_sha = get_resp.json()["sha"]

            resp = requests.put(
                f"{GITEA_API_ROOT}/repos/{REPO}/contents/{LATEST_FILE}",
                headers={"Authorization": f"token {GITEA_API_TOKEN}"},
                json={
                    "author": {"email": "leapsecondbot@hhome.me", "name": "Leap Second Bot"},
                    "branch": "master",
                    "committer": {"email": "leapsecondbot@hhome.me", "name": "Leap Second Bot"},
                    "content": base64.b64encode(resp.text.encode("utf-8")).decode("utf-8"),
                    "dates": {"author": now.isoformat() + "Z", "committer": now.isoformat() + "Z"},
                    "message": f"Update Bulletin to Vol. {expected_volume} No. {expected_number}",
                    "sha": existing_sha,
                },
            )
            resp.raise_for_status()
        else:
            print("No new version found")
