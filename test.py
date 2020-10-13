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


a = [1,2,2,2,3]
if 2 in a:
    a.remove(2)
print (a)

"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDI0OTgzMzcsIm5iZiI6MTYwMjQ5ODMzNywianRpIjoiMjk3MDdkYTktZmY0OC00YjUzLWE2MDQtODVmNTg1MTlkMWJiIiwiZXhwIjoxNjAzMTAzMTM3LCJpZGVudGl0eSI6IjVmNzgwMTFkZWYwNTdiMTAxNWZhYTM4MCIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.4mExjgjWMIqySvFxNY3LOuZ6JellIAHMJ6BNm1NHB4I"
