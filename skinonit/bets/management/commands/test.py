import datetime
import pytz
from datetime import timedelta

date_time = '2019-06-14-8:10PM'
gamedate_aware = pytz.timezone("US/Eastern").localize(datetime.datetime.strptime(date_time, '%Y-%m-%d-%I:%M%p'))
print(gamedate_aware)