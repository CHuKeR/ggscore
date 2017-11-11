import datetime
import pytz


print(datetime.datetime.utcnow())


print(datetime.datetime.now(tz=pytz.timezone('Europe/Moscow')).day)