## Control 5

----------------

### Forma 1

**(6 ptos)** Suponga que se tiene un grupo de instancias que se ejecutan como Threads a lo largo de un proceso. Los productos o resultados de algunos de esos hilos son necesarios para ejecutar otras funciones del proceso principal. Explique cómo podría asegurarse de que los resultados estarán listos para cuando deban ser usados por el proceso principal.

#### *Respuesta*

 Dentro del programa principal, después de instanciar y comenzar los threads habría que usar el comando `instancia_thread.join()` para que el programa principal espere a que el thread termine para continuar ejecutándose. Ejemplo:
 ```
 from threading import Thread
 etc..etc.. #parte del programa principal

# instancio threads
th = Thread(target= alguna_funcion)
th2 = Thread(target= alguna_otra_funcion)

# incio los threads
th.start()
th2.start()

# aplico join() y se bloquea el programa principal
th.join()
th2.join()

# el programa esperará a que terminen los threads y continuará leyendo lo que sigue..

```

==============


### Forma 2
**(6 ptos)** Suponga que se tiene una clase cuyas instancias corresponden a Threads que están realizando alguna acción. Para poder ejecutar la acción, necesitan de un recurso que se debe compartir entre todos los Threads. Explique cómo implementaría una solución que controle el acceso concurrente al recurso compartido. ¿Dónde debería implementarse dicho control?

#### *Respuesta*


Dicho control debe ser mediante un `Lock` y se debe implementar dentro de la clase. Como las instancias comparten un recurso, al crear un `Lock` para la clase, cada vez que una instancia quiera acceder al recurso se bloqueen las demás instancias y éstas no puedan acceder al mismo tiempo al mismo recurso.

Por ejemplo, si tenemos varios threads que quieren escribir sobre un mismo archivo:

```
import threading


class MiThread(threading.Thread):
    lock = threading.Lock()
    
    def __init__(self, i, archivo):
        super().__init__()
        self.i = i
        self.archivo = archivo
    
    def run(self):
        
        MiThread.lock.acquire() # bloquea la ejecución de los demas threads al intentar escribir en el archivo
        try:
            self.archivo.write('Esta linea fue escrita por el thread # {}\n'.format(self.i))
        finally:
            MiThread.lock.release() # devuelve el control del recurso a los threads en espera

    	# también se puede usar with MiThread.lock en vez de try y finally

```


===================

### Forma 3

**(6 ptos)** Suponga que se tienen instancias de una clase que corresponden a un recurso compartido entre un conjunto de Threads. Explique cómo se podría controlar el acceso concurrente a dichos recursos. ¿Dónde debería implementarse dicho control?

#### *Respuesta*

El control `Lock` se debe crear en el lugar (sea clase o en el programa principal) que contiene al recurso y siempre requiera acceder ese recurso, se tiene que usar el mismo `Lock`.


Por ejemplo, tenemos un thread que tiene un atributo `recurso` que es una lista. Para agregar elementos a esta lista se usa el método `agregar_elemento` y para obtener el último elemento de la lista se utiliza el método `obtener`. Además, se puede traspasar el último elemento de la lista `recurso` a la lista `recurso` de otro thread.


```
class MiClase(threading.Thread):
    # agregaremos los mecanismos de bloqueo para asegurar la sincronización 
    # entre los threads.

    def __init__(self):
    	super().__init__()
        self.lock = threading.Lock() 
        self.recurso = []

    def agregar(self, elemento):
        with self.lock:
            self.recurso.append(elemento)

    def obtener(self):
        with self.lock:
            return self.recursos.pop()

    def traspasar_elemento(self, otro_thread):
    	elemento = self.obtener()
    	otro_thread.agregar(elemento)


```

Entonces, se utiliza el self.lock en el momento que se requiere acceso a `self.recurso` para controlar el acceso a éste. Esto es por que si dos threads utilizan la función `traspasar_elemento` sobre un mismo thread (al mismo tiempo), se sincronizará el acceso al thread evitando errores al agregar elementos en `recurso`.
