#!/usr/bin/env python3
import math
import re
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

import roman  # type: ignore

UT1_UTC_RX = re.compile(r"UT1-UTC\s*=\s*([0-9.+-]+)\s*([+-])\s*([0-9.]+)\s*\(MJD\s*-\s*(\d+)\)\s*-\s*\(UT2-UT1\)")
ACCURACY_RX = re.compile(r"S t = 0.00025 \(MJD-(\d+)\)\*\*0.75")
ISSUE_RX = re.compile(r"Vol. ([XIV]+) No. ([0-9]+)")


class BulletinA:
    @dataclass
    class LeapSecondPrediction:

        # The day the predicted leap second will happen
        # Should be either the 1st of January (as in, the leap second is added to the end of December the previous year)
        # or 1st July (leap second added to the end of the last day of June)
        predicted_leap_day: date

        # Is the leap second a positive (ie, an extra second is inserted) leap second
        is_positive: bool

        # The seconds difference between UT1 and UTC that caused this prediction
        ut1_utc_delta: Decimal

        accuracy: Decimal

    class NoPrediction(Exception):
        """
        Raised when no prediction can be made
        """

        pass

    class ParseError(Exception):
        """
        Raised when the file cannot be parsed
        """

        pass

    @classmethod
    def parse(cls, filename: str) -> "BulletinA":
        """
        Create a new BulletinA instance by reading the parameters from the given file

        Expects the file to contain lines like:
        `UT1-UTC = dut1 +/- rate * (MJD - mjd1) - (UT2-UT1)`
        `t = 0.00025 * (MJD-mjd2) * 0.75`
        `Vol. XXIV No. 1`

        Which are parsed to find the relevent information to construct a BulletinA object
        """
        with open(filename) as f:
            content = f.read()

        if f1 := UT1_UTC_RX.search(content):
            groups = f1.groups()
            dut1 = Decimal(groups[0])
            rate = Decimal(groups[1] + groups[2])
            mjd1 = Decimal(groups[3])
        else:
            raise BulletinA.ParseError("Failed to find prediction formula")

        if f2 := ACCURACY_RX.search(content):
            mjd2 = Decimal(f2.groups()[0])
        else:
            raise BulletinA.ParseError("Failed to find accuracy formula")

        if issue := ISSUE_RX.search(content):
            volume, number = issue.groups()
        else:
            raise BulletinA.ParseError("Cannot determine bulletin number")

        return cls(dut1, rate, mjd1, mjd2, roman.fromRoman(volume) + 1987, int(number))

    def __init__(self, dut1: Decimal, rate: Decimal, mjd1: Decimal, mjd2: Decimal, year: int, number: int):
        self.dut1 = dut1
        self.rate = rate
        self.mjd1 = mjd1
        self.mjd2 = mjd2
        self.year = year
        self.number = number

    def leap_second_prediction(self, delta_limit: float = 0.5, years_limit: int = 50) -> LeapSecondPrediction:
        """
        :param delta_limit: The absolute UT1-UTC difference to allow before deciding a leap second will be added
        :param years_limit: How many years in the future to calculate before giving up
        """

        # TODO: Work out a reasonable starting date based on the issue date of the bulletin
        predict_day = date(2022, 1, 1)
        finish_year = predict_day.year + years_limit

        while predict_day.year < finish_year:
            mjd3 = BulletinA.iso8601_mjd(predict_day)
            u = BulletinA.ut1_utc(self.dut1, self.rate, self.mjd1, mjd3)
            a = BulletinA.accuracy(self.mjd2, mjd3)

            if abs(u) > delta_limit:
                return BulletinA.LeapSecondPrediction(
                    predicted_leap_day=predict_day, is_positive=u < 0, ut1_utc_delta=u, accuracy=a
                )

            if predict_day.month == 1:
                predict_day = date(predict_day.year, 7, 1)
            else:
                predict_day = date(predict_day.year + 1, 1, 1)

        raise BulletinA.NoPrediction(f"No leap second predicted before {predict_day}")

    @property
    def cannonical_url(self):
        return "https://datacenter.iers.org/data/6/bulletina-{}-{}.txt".format(
            roman.toRoman(self.year - 1987).lower(), str(self.number).zfill(3)
        )

    @staticmethod
    def iso8601_mjd(for_date: date):
        return Decimal(
            for_date.year * 1461 / 4
            - for_date.year / 100
            + for_date.year / 400
            + for_date.month * 153 / 5
            + for_date.day
            - 679004
        )

    @staticmethod
    def besselian_year(mjd):
        return Decimal(Decimal("2000.0") + (mjd - Decimal("51544.03") / Decimal("365.2422")))

    @staticmethod
    def ut2_ut1(mjd):
        T = BulletinA.besselian_year(mjd)
        tT = Decimal(2 * math.pi) * T
        return Decimal(
            +0.022 * math.sin(tT) - 0.012 * math.cos(tT) - 0.006 * math.sin(2 * tT) + 0.007 * math.cos(2 * tT)
        )

    @staticmethod
    def ut1_utc(dut1, rate, mjd1, mjd3):
        return dut1 + rate * (mjd3 - mjd1) - BulletinA.ut2_ut1(mjd3)

    @staticmethod
    def accuracy(mjd2, mjd3):
        return 0.00025 * pow(float(mjd3 - mjd2), 0.75)
