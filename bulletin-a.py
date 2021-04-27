#!/usr/bin/env python3
import re
import math
import json
from datetime import datetime
from decimal import Decimal
from jinja2 import Template

with open("bulletin_a_latest.txt") as f:
    content = f.read()

groups = re.search(r"UT1-UTC\s*=\s*([0-9.+-]+)\s*([+-])\s*([0-9.]+)\s*\(MJD\s*-\s*(\d+)\)\s*-\s*\(UT2-UT1\)", content).groups()
dut1 = Decimal(groups[0])
rate = Decimal(groups[1] + groups[2])
mjd1 = Decimal(groups[3])
mjd2 = Decimal(re.search(r"S t = 0.00025 \(MJD-(\d+)\)\*\*0.75", content).groups()[0])

issue, number = re.search("Vol. ([XIV]+) No. ([0-9]+)", content).groups()

print(dut1, rate, mjd1, mjd2)
print(issue, number)

y = 2022
m = 1
d = 1

def iso8601_mjd(y, m, d):
    return Decimal(y*1461/4 - y/100 + y/400 + m*153/5 + d - 679004)

def besselian_year(mjd):
    return Decimal(Decimal("2000.0") + (mjd - Decimal("51544.03") / Decimal("365.2422")))

def ut2_ut1(mjd):
    T = besselian_year(mjd)
    tT = Decimal(2 * math.pi) * T
    return Decimal(+ 0.022 * math.sin(tT) - 0.012 * math.cos(tT) - 0.006 * math.sin(2*tT) + 0.007 * math.cos(2*tT))

def ut1_utc(dut1, rate, mjd1, mjd3):
    return(dut1 + rate * (mjd3 - mjd1) - ut2_ut1(mjd3))

def accuracy(mjd2, mjd3):
    return(0.00025 * pow(float(mjd3 - mjd2), 0.75))


has_result = False
while True and y < 2060:
    mjd3 = iso8601_mjd(y, m, d)
    u = ut1_utc(dut1, rate, mjd1, mjd3)
    a = accuracy(mjd2, mjd3)

    if (u > 0.5 or u < -0.5):
        has_result = True
        break

    if m == 1:
        m = 7
    else:
        m = 1
        y += 1

data = {
    "source": {
        "number": number,
        "issue": issue,
        "url": "https://datacenter.iers.org/data/6/bulletina-{}-{}.txt".format(issue.lower(), number)
    },
    "next_leap_second": {
        "year": y,
        "month": m,
        "is_positive": u < 0
    },
    "last_updated": datetime.utcnow().isoformat()
}

if not has_result:
    data["next_leap_second"] = None

with open("index.html.tpl") as f:
    index_template = Template(f.read())

with open("dist/index.html", "w") as f:
    f.write(index_template.render(**data))

with open("dist/index.json", "w") as f:
    json.dump(data, f)
