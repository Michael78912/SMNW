import os

file = open('compiled.py', 'w')

def f(dir='.'):
    for i in os.listdir(dir):
        if os.path.isdir(os.path.join(dir, i)):
            f(os.path.join(dir, i))

        elif i.endswith('.py'):
            file.write(open(os.path.join(dir, i)).read())

f()
file.close()
