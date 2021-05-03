## Leap Second Precitions

This is the source for the leap second predictor that is hosted on https://www.565851109.xyz - it also includes some code for manipulating Bulletins that may be useful

### Building the site

Jenkins takes care of doing this automatically and uploading to S3, but manually, using Poetry:

``` sh
poetry install
mkdir dist
poetry run bulletin-a
```

This repo needs to be updated weekly when the new IERS Bulletin is published. This repo includes a script to automatically fetch the files and update this repo using the Gitea API, but it is pretty specific to my setup and probably isn't much use for others.

### Calculating the prediction

The math is a bit beyond me, but the bulletin contains a formula like:

`UT1-UTC = dut1 +/- rate * (MJD - mjd1) - (UT2-UT1)`

and

`t = 0.00025 * (MJD-mjd2) * 0.75`

where `dut1`, `rate`, `mjd1` and `mjd2` are constants, and `MJD` is the date to predict for.

Borrowing Tonys' code, you can calculate a predicted value for `UT1-UTC` for an arbitary date in the future. I'm picking the 1st of July and 1st of January to see `UT1-UTC` is greater than 0.5 or less than -0.5, in which case a leap second would be needed. If `UT1-UTC` is negative, then a positive leap second would be needed, otherwise a negative one. I find that trying to calculate predictions that are too close to when the bulletin was issued produce nonsense answers, and I stop calculating if there is no answer by 2060.
