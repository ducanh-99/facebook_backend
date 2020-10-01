from flask_mongoengine import Document
import inspect


class Test:
    def __init__ (self):
        self.a = 1
        self.b = 2
    
    def abc(self):
        self.a = 3

def test(a):
    a.abc()
    print (a.a)


ab  = Test()
test(ab)
print (ab.a)