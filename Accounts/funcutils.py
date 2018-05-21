# -- START FUNCTION LIST --
def parse_date(ddate):
    """Error checking for input dates"""
    if "/" in ddate:
        ddate = ddate.split("/")
    elif "-" in ddate:
        ddate = ddate.split("-")
    else:
        raise ValueError("Date contains invalid seperator")

    try:
        ddate = tuple(map(lambda x: int(x), ddate))
    except ValueError:
        raise ValueError("Date contains invalid variables types")

    if len(ddate) != 3:
        raise ValueError("Date contains invalid number of variables")

    # All errors have been safely checked -- now create a valid date object
    return date(year = ddate[2], 
                month = ddate[0],
                day = ddate[1])

def valid_date(ddate):
"""Date parsing used in final output date checking"""
    ddate = tuple(map(lambda x: int(x), ddate.split("/")))
    ddate = date(year = 2000 + ddate[2],
                    month = ddate[0],
                    day = ddate[1])
    return start <= ddate <= end
# -- END OF FUNCTIONS -- 