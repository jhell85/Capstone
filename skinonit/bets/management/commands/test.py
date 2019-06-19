import datetime
import pytz
from datetime import timedelta

gamedate_aware = pytz.timezone("US/Eastern").localize(datetime.datetime.strptime('2019-06-14-8:10PM', '%Y-%m-%d-%I:%M%p'))
print(gamedate_aware)