# CSTimer Total
Get the total time you have spent cubing while using CSTimer and other similar stats.

## Requirements
- Python 3.9+

## How to use
1. Download or clone this repo.
2. Open [CSTimer](https://cstimer.net/) and download your times using the `Export to file` button in the `EXPORT` menu.
3. Place the downloaded file in the same folder as the Python script from this repo and make sure the downloaded file ends with `.txt`.
4. Run the Python script `cstimer_total.py`.

## Example Output
```
> ls
cstimer_XX_YY.txt  cstimer_total.py  LICENSE  README.md

> python3.9 cstimer_total.py
============================================================
You have spent a total of X hours, Y minutes and Z seconds of solving in CSTimer
With a total of X solves
Average time: X seconds

The session you have spent the most time solving with is 3x3
In that session you spent a total of X hours, Y minutes and Z seconds
With a total of X solves
Average time: X seconds

The session you have the most solves with is 3x3
In that session you spent a total of X hours, Y minutes and Z seconds
With a total of X solves
Average time: X seconds


2x2
X hours, Y minutes and Z seconds
X solves
Average time: X seconds

3x3
X hours, Y minutes and Z seconds
X solves
Average time: X seconds

4x4
X hours, Y minutes and Z seconds
X solves
Average time: X minutes and X seconds

5x5
X hours, Y minutes and Z seconds
X solves
Average time: X minutes and X seconds