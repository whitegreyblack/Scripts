from collections import namedtuple
import datetime

# -- INTERNAL VARIABLES--
DATE_FORMAT = "%m/%d/%y"
date_model = namedtuple("DateModel", "year month date")

INVALID_VARIABLE_NUMBER = """
Date contains invalid number of variables (expected: 3, got {})
"""[1:]

# -- START FUNCTION LIST --
def parse_date(date: str, date_format: str=DATE_FORMAT) -> datetime.date:
    """Error checking for user input dates"""
    date_model = datetime.datetime.strptime(date, date_format)
    if date_model.year > datetime.datetime.now().year % 2000:
        date_model.replace(year=date_model.year - 100)
    return date_model.date()

def valid_date(date: str, start: str, end: str=None, seperator="/") -> bool:
    """
    Date parsing used in csv date inputs. Checks if date is between two date 
    points.
    """
    date = parse_date(date)
    if not isinstance(start, datetime.date):
        start = parse_date(start)
    if not end:
        end = datetime.datetime.now().date()
    return start <= date <= end
# -- END OF FUNCTIONS --

if __name__ == "__main__":
    print("Utils for date time manipulation in accounts.py and creditcard.py")