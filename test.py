# def test(**kwargs):
#     print(kwargs["test1"]) 
#     print(kwargs["test2"]) 
#     for i in kwargs:
#         print (i)

# test(test1 = 1, test2 = 2)

import datetime
import pytz

d = datetime.datetime.now()
timezone = pytz.timezone("Asia/Vientiane")
d_aware = timezone.localize(d)
print (d)
# print (pytz.all_timezones)