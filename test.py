# def test(**kwargs):
#     print(kwargs["test1"]) 
#     print(kwargs["test2"]) 
#     for i in kwargs:
#         print (i)

# test(test1 = 1, test2 = 2)

# import datetime
# import pytz

# utc_now = pytz.utc.localize(datetime.datetime.utcnow())
# pst_now = utc_now.astimezone(pytz.timezone("Asia/Vientiane"))
# pst_now1 = utc_now.astimezone(pytz.timezone("Asia/Saigon"))

# print(pst_now , pst_now1)
# print (pytz.all_timezones)
class Test():
    def a(self):
        print("a")

print(Test.a)