import numpy
import timeit

print('hi')

timeit.timeit('''
big_list = [['hi'] * 1000] * 1000
for i in big_list:
    for s in i:
        pass''')
print(time.time(), 'after loops')
