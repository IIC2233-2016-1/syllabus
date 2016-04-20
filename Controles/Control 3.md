# Control 3

### Forma 1

##### (3 pts.) Dado el siguiente código escriba el output, justifique su respuesta:
```python
def mi_dec(p):
    def _mi_dec(f):
        def __mi_dec(*args, **kwargs):
            if p:
                f(args[0])
            else:
                print("Chao " + args[0])
        return __mi_dec
    return _mi_dec

@mi_dec(True)
def function(name):
    print("Hola " + name)

function("Pedro")
```

El output del código es `Hola Pedro` (la función retorna `None` pero imprime `Hola Pedro`). Al llamar `function("Pedro")` se invoca al decorador `mi_dec` con parámetro `True`, lo que invoca a la función `_mi_dec` en lugar de `function`, la cual invoca con los parámetros entregados a `function` al método `__mi_dec`. Como el valor de `p` es `True` (el parámetro entregado al decorador) se ejecuta `f(args[0])`, lo que equivale a llamar directamente a `function("Pedro")` (ya que `f` es `function` y `args[0]` es `"Pedro"`), imprimiendo `"Hola Pedro"`.

#### Repartición de puntaje:
* (1.0 pts.) Output correcto
* (2.0 pts.) Justificación correspondiente 

##### (3 pts.) Escriba en una línea el ciclo del siguiente código (desde `r = 1`) usando `filter`, `reduce` y funciones `lambda`:
```python
lista = [i for i in range(1, 10)]

r = 1
for p in lista:
    if p % 2 == 0:
        r *= p
```

Como podemos notar, tenemos que acumular valores en una variable (`r *= p`) y operar solo con algunos valores de la lista (`if p % 2 == 0:`), por que tenemos que usar `reduce` y `filter` respectivamente:

```python
reduce(								# Tenemos que acumular valores ...
	lambda x, y: x * y, 			# ... multiplicandolos
	filter(							# Y queremos usar solo algunos valores ...
		lambda x: not x % 2, lista)	# ... aquellos que son pares
	)
```

#### Repartición de puntaje:
* (1.0 pts.) Orden correcto
* (1.0 pts.) Función `lambda` en `reduce` bien definida
* (1.0 pts.) Función `lambda` en `filter` bien definida

----------

### Forma 2

##### (3 pts.) Dado el siguiente código escriba el output, justifique su respuesta:
```python
def mi_dec(p):
    def _mi_dec(f):
        l = {}
        def __mi_dec(*args, **kwargs):
            l.update({k: v for k, v in zip(args, f(*args)) if v > 5})
            return list(l)
        return __mi_dec
    return _mi_dec

@mi_dec(5)
def function(*words):
    return list(map(len, words))

function("Pedro", "Gustavo")
```

El output del código es `['Gustavo']` (la función retorna `[Gustavo]` pero no imprime). Al llamar `function("Pedro", "Gustavo")` se invoca al decorador `mi_dec` con parámetro `5`, lo que invoca a la función `_mi_dec` en lugar de `function`, la cual invoca con los parámetros entregados a `function` al método `__mi_dec`. Al diccionario `l` (inicialmente vacío) le agregamos como keys los parámetros y como valores los largos de estos, pero solo aquellos cuyo largo sea mayor que 5 (`v > 5`). Como `"Gustavo"` es el único de los inputs cuyo `len` es mayor que 5, al hacer `list(l)` obtenemos `["Gustavo"]`.

#### Repartición de puntaje:
* (1.0 pts.) Output correcto
* (2.0 pts.) Justificación correspondiente 

##### (3 pts.) Escriba en una línea el ciclo del siguiente código (desde la sentencia `m = float("Inf")`) usando solo `reduce` y `map`:
```python
lista = ["Pedro", "Alejandro"]

m = float("Inf")
for p in lista:
    m = min(m, len(p))
```

Como podemos notar, tenemos que acumular valores en una variable (`m = min(m, len(p))`) y vamos aplicando una función a todos los elementos de la lista (`len(p)`), por que tenemos que usar `reduce` y `map` respectivamente:

```python
reduce(					# Tenemos que acumular valores ...
	min, 				# ... acumulando el minimo
	map(				# Y queremos aplicar una funcion sobre todos los elementos ...
		len, lista))	# ... len
```

#### Repartición de puntaje:
* (1.0 pts.) Orden correcto y no usar `lambda`
* (1.0 pts.) Función en `reduce` correcta
* (1.0 pts.) Función en `map` correcta

----------

### Forma 3

##### (3 pts.) Dado el siguiente código escriba el output, justifique su respuesta:
```python
def mi_dec(p):
    def _mi_dec(f):
        def __mi_dec(*args, **kwargs):
            print("Chao " + args[0] + " " + p)
            return True
        return __mi_dec
    return _mi_dec

@mi_dec("ABC")
def function(name):
    print("Hola " + name)
    return True

function("Pedro")
```

El output del código es `Chao Pedro ABC` (la función retorna `True` e imprime `Chao Pedro ABC`). Al llamar `function("Pedro")` se invoca al decorador `mi_dec` con parámetro `"ABC"`, lo que invoca a la función `_mi_dec` en lugar de `function`, la cual invoca con los parámetros entregados a `function` al método `__mi_dec`. Aquí se imprime la línea `"Chao Pedro ABC"`, ya que el primer argumento dado a la función `function` fue `"Pedro"` y `p` (el valor dado al decorador) es `"ABC"`. Luego, retorna `True`, al igual que en `function`.

#### Repartición de puntaje:
* (1.0 pts.) Output correcto
* (2.0 pts.) Justificación correspondiente 

##### (3 pts.) Escriba la segunda línea del siguiente código usando `filter`y una función `lambda`:
```python
lista = [i for i in range(100)]
p1 = [p for p in lista if p % 2 == 0]
```

Como podemos notar, tenemos que filtrar valores (quedarnos con los pares) y al final quedarnos con una lista, por lo que tenemos que usar `filter` y, al final, `list`:

```python
list(								# Tenemos que obtener una lista ...
	filter(							# ... con solo algunos valores ...
		lambda x: not x % 2, lista)	# ... aquellos que son pares
	)
```

#### Repartición de puntaje:
* (1.0 pts.) Orden correcto
* (1.0 pts.) Función `lambda` en `filter` bien definida
* (1.0 pts.) Retornar una lista (usar `list`)
