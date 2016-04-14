# Control 2

*Nota*: en todas las formas, cada pregunta tiene 3 pts.

## Forma 1

##### 1. Escriba una función en python que permita recorrer recursivamente un árbol binario e imprimir el valor de cada nodo partiendo desde las hojas. ¿Cuál sería su complejidad computacional? (*Hint*: Considere que las operaciones corresponden a los `print` que se hacen en cada nodo, y que el tamaño del input corresponde al número de nodos en el árbol).

``` python
def recorrer(self):
    for hijo in (self.hijo_izquierdo, self.hijo_derecho):
        if hijo is not None:
            hijo.recorrer()
    id_padre = None if self.padre is None else self.padre.id
    print("id-padre: {}\t -> id-nodo: {}\t valor: {}".format(
        id_padre,
        self.id,
        self.value
    ))
```

La complejidad computacional, si se considera que el tamaño del input *n* es el número de nodos en el árbol, es *O(n)* pues debe realizarse un `print` por cada nodo.

##### Repartición del puntaje
- 2 puntos por función `recorrer`. Basta con que se imprima el valor del nodo actual en cada print.
- 1 punto por complejidad computacional correcta (no es necesario dar explicación).


#### 2. Escriba el(los) comando(s) de consola que permita(n) desplegar los *c* comandos que ejecutamos anteriormente que contienen el string `sed`

En vista que en la lectura sobre el tema no aparece cómo desplegar los últimos *c* comandos, se considera puntaje completo si el alumno despliega todos los comandos ejecutados que contienen el string `sed`. Esto puede hacerse con:

``` sh
history | grep sed
```

##### Repartición del puntaje
- 1.5 puntos si identifica que debiera usar `history`
- 1.5 puntos por utilización de `grep`


## Forma 2

#### 1. Escriba una función en python que permita recorrer recursivamente un árbol binario e imprimir el valor de cada nodo partiendo desde el nodo raíz. ¿Cuál sería su complejidad computacional? (*Hint*: Considere que las operaciones corresponden a los `print` que se hacen en cada nodo, y que el tamaño del input corresponde al número de nodos en el árbol).

``` python
def recorrer(self):
    id_padre = None if self.padre is None else self.padre.id
    print("id-padre: {}\t -> id-nodo: {}\t valor: {}".format(
        id_padre,
        self.id,
        self.value
    ))
    for hijo in (self.hijo_izquierdo, self.hijo_derecho):
        if hijo is not None:
            hijo.recorrer()
```

La complejidad computacional, si se considera que el tamaño del input *n* es el número de nodos en el árbol, es *O(n)* pues debe realizarse un `print` por cada nodo.

##### Repartición del puntaje
- 2 puntos por función `recorrer`. Basta con que se imprima el valor del nodo actual en cada print.
- 1 punto por complejidad computacional correcta (no es necesario dar explicación).

#### 2. Explique qué se debe hacer en la consola de unix para que cada vez que iniciemos una sesión, quede estipulado que cualquier ejecución futura del comando que muestra los archivos que hay dentro de un directorio, muestre además (sin escribir nada extra) información detallada sobre cada archivo (permisos, usuario, grupo, fecha de creación, etc.)

Basta con:
* Abrir nano con `nano ~/.bash_profile`
* Agregar la opción `-la` al comando `ls` con `alias ls="ls -la"`

###### Nota: Se considera correcto también usar un editor distinto a nano, por ejemplo vim


##### Repartición de puntaje
- 1 punto por indicar que debe abrirse nano
- 1 punto por identificar que debe agregarse `-la` como opción predeterminada a `ls`
- 1 punto por correcta utilización del comando `alias`

## Forma 3

#### 1. Escriba una función en python que recorra un árbol binario en **amplitud**, imprimiendo el valor de cada nodo durante su recorrido. Debe partir desde el nodo raíz. ¿Cuál sería su complejidad computacional? (*Hint*: Considere que las operaciones corresponden a los `print` que se hacen en cada nodo, y que el tamaño del input corresponde al número de nodos en el árbol).

``` python
def recorrer(self):
    por_visitar = deque()       # importado desde collections
    por_visitar.append(self)
    visitados = list()
    
    while por_visitar:
        # Conseguir siguiente nodo a visitar
        nodo_actual = por_visitar.popleft()
        if nodo_actual not in visitados:
            visitados.append(nodo_actual)
            
            # Recorrer el nodo actual
            id_padre = None if self.padre is None else self.padre.id
            print("id-padre: {}\t -> id-nodo: {}\t valor: {}".format(
                id_padre,
                self.id,
                self.value
            ))
            
            # Agregar hijos a la cola
            for hijo in (nodo_actual.hijo_izquierdo, nodo_actual.hijo_derecho):
                if hijo is not None:
                    por_visitar.append(hijo)
```

La complejidad computacional, si se considera que el tamaño del input *n* es el número de nodos en el árbol, es *O(n)* pues debe realizarse un `print` por cada nodo.

##### Repartición del puntaje
- 2 puntos por función `recorrer`. Basta con que se imprima el valor del nodo actual en cada print.
- 1 punto por complejidad computacional correcta (no es necesario dar explicación).

#### 2. Explique qué se debe hacer en la consola de unix para que cada vez que iniciemos una sesión, se cree un directorio llamado `prueba` en el directorio actual y se imprima el mensaje "directorio creado".

Basta con:
* Abrir nano con `nano ~/.bash_profile`
* Crear el directorio con `mkdir prueba`
* Imprimir el mensaje pedido con `echo directorio creado`

###### Nota: Se considera correcto también usar un editor distinto a nano, por ejemplo vim

##### Repartición de puntajes
- 1 punto por indicar que debe abrirse nano
- 1 punto por saber cómo crear el directorio
- 1 punto por saber cómo imprimir el mensaje
