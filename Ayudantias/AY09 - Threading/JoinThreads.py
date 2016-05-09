''' Join in Thread '''

import time
import random
from threading import Thread

def myfunc(i):
    sleeping_time = random.randint(1,3)
    print ("sleeping {0} sec from thread {1}".format(sleeping_time, i))
    time.sleep(sleeping_time)
    print ("finished sleeping from thread {0}".format(i))

for i in range(7):
    t = Thread(target=myfunc, args=(i,))
    t.start()
    t.join()   # Comentar para ver la diferencia


print("Esta linea")
print("Y esta otra")
print("Y estos numeros")

for i in range(10):
    print(i)

print("Se imprimen despues de los threads se terminen de ejecutar")
