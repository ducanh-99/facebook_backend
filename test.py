import inspect


class Test:

    def __init__(self):
        self.a = 1
        self.b = 2

    def abc(self):
        x = 1
        try:
            print(x)
            self.a = 2
        except NameError:
            print("Variable x is not defined")
            self.a = 3
        return self.a


a = [{"a": 1, 'b' : 2}, {"a" : 2}]
a.remove({"a" :1})
print(a)
