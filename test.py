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


ab = Test()
print (ab.abc())
a = 1+2
