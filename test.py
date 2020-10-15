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


a1 = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDI3NzI2NjYsIm5iZiI6MTYwMjc3MjY2NiwianRpIjoiNzYwY2M0MmMtN2UwOS00OWU2LTg0OGEtYjc4NjRjZTc0ZDY1IiwiZXhwIjoxNjAzMzc3NDY2LCJpZGVudGl0eSI6IjVmNzgwMTAyNjEzYmFkY2U4NGRjMzE2NiIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.W_fxe10FZY5-_hYMsoX-tx2yhVGh-JXr8czyoCNGlB0"
a2 = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDI3NzI2OTQsIm5iZiI6MTYwMjc3MjY5NCwianRpIjoiNTgwZmIxYTYtODNmYy00YTUxLWIyZDMtM2U2MTZhMjdkMjU0IiwiZXhwIjoxNjAzMzc3NDk0LCJpZGVudGl0eSI6IjVmNzgwMTFkZWYwNTdiMTAxNWZhYTM4MCIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.WqHyYUV-6mJ-x0dWt1B89ftmi3CBuZbf9I-jb9TH8MM"

