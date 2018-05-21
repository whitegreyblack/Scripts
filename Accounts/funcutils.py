from collections import namedtuple
import datetime

# -- INTERNAL VARIABLES--
date_format = "%m/%d/%y"
date_model = namedtuple("DateModel", "year month date")

INVALID_VARIABLE_NUMBER = """
Date contains invalid number of variables (expected: 3, got {})
"""[1:]

# -- START FUNCTION LIST --
def parse_date(date: str) -> datetime.date:
    """Error checking for user input dates"""
    # checks seperator - only want slashes or dashes
    if "/" in date:
        date = date.split("/")
    elif "-" in date:
        date = date.split("-")
    else:
        raise ValueError("Date contains invalid seperator")

    # checks date variables between seperators
    try:
        date = tuple(map(lambda x: int(x), date))
    except ValueError as exception:
        exit("Date contains invalid variables types")

    try:
        month, day, year = date
    except ValueError:
        exit(INVALID_VARIABLE_NUMBER.format(len(date)))

    # All errors have been safely checked -- now create a valid date object
    return datetime.date(year=date[2], month=date[0], day=date[1])

def valid_date(date, seperator="/") -> bool:
    """Date parsing used in csv date inputs"""
    date = tuple(map(lambda x: int(x), date.split(seperator)))
    date = datetime.date(year=2000 + date[2],
                         month=date[0],
                         day=date[1])
    return start <= date <= end
# -- END OF FUNCTIONS --

if __name__ == "__main__":
    print("Utils for date time manipulation in accounts.py and creditcard.py")
    # print(parse_date("10/a/6/6"))
    # print(parse_date("10/5/6/6"))