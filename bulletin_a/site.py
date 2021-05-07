import argparse
import json
import os.path
from dataclasses import asdict
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from jinja2 import Template

from . import BulletinA, bulletins, templates


def encoder(o):
    if isinstance(o, date):
        return o.isoformat()
    elif isinstance(o, datetime):
        return o.isoformat()
    elif isinstance(o, Decimal):
        return str(o)

    return json.JSONEncoder().default(o)


def serialize(bulletin: BulletinA, result: Optional[BulletinA.LeapSecondPrediction]):
    output = {
        "source": {"year": bulletin.year, "number": bulletin.number, "url": bulletin.cannonical_url,},
        "next_leap_second": None,
    }

    if result:
        output["next_leap_second"] = asdict(result)

    return output


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--output-directory", default="dist/")

    args = argparser.parse_args()

    with bulletins.LATEST_FILE as f:
        bulletin = BulletinA.parse(f)

    try:
        prediction = bulletin.leap_second_prediction()
    except BulletinA.NoPrediction:
        prediction = None

    latest = serialize(bulletin, prediction)
    data = {
        "latest": latest,
        str(bulletin.year): {str(bulletin.number): latest},
        "last_updated": datetime.utcnow(),
    }

    index_template = Template(templates.INDEX_TEMPLATE)

    with open(os.path.join(args.output_directory, "index.html"), "w") as f:
        f.write(index_template.render(**data))

    with open(os.path.join(args.output_directory, "index.json"), "w") as f:
        json.dump(data, f, default=encoder)
