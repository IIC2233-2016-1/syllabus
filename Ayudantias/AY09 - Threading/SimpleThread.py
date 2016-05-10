''' Simple Thread '''

import time
import random
from threading import Thread

def myfunc(i):
    sleeping_time = random.randint(1,5)
    print ("sleeping {0} sec from thread {1}".format(sleeping_time, i))
    time.sleep(sleeping_time)
    print ("finished sleeping from thread {0}".format(i))

for i in range(10):
    t = Thread(target=myfunc, args=(i,))
    t.start()
