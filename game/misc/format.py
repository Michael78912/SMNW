import os
os.chdir(r'C:\Users\Michael\Desktop\stickmanranger')
print(
    'hi! I am formatting your files in your current project, stickmanranger!')
for i in os.listdir():
    try:
        if i.endswith('.py'):
            print('formatting %a' % i)
            os.system('yapf -i %s' % i)
    except:
        pass
print('done!')
import time
time.sleep(1)
