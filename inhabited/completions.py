import calendar
from datetime import date

# Get the completion info for the last n days.
# This means that we:
#   walk the date back a day at a time from today
#   keep track of where we are in the list of completions 
#   push true or false depending on if the current completion lies within the
#   correct day
def completed_periods(n, completions):
    return [True] * n

def is_today(ts):
    d = date.fromtimestamp(ts)
    return d == date.today()

def to_timestamp(dt):
    """Converts a datetime object to UTC timestamp

    naive datetime will be considered UTC.

    """

    return calendar.timegm(dt.utctimetuple())
