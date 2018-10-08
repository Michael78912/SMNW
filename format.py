import os


def main(dir):
    for i in os.listdir(dir):
        if os.path.isdir(os.path.join(dir, i)):
            main(os.path.join(dir, i))
        elif i.endswith('.py'):
            print('formatting %s' % i)
            os.system('yapf -i ' + os.path.join(dir, i))
            os.system('autopep8 -i ' + os.path.join(dir, i))


if __name__ == '__main__':
    main('.')
