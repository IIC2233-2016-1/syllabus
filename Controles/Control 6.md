# Control 6

**NOTA**: en todas las formas, cada pregunta tiene 3 pts.

## Forma 1

##### 1. ¿De qué forma es posible personalizar la deserialización de un objeto cualquiera en Python? Escriba un ejemplo.

Implementando el método `__setstate__` en la clase de la cual el objeto es instancia. Este método recibe el diccionario original, y puede realizar modificaciones a este antes de guardarlo en `self.__dict__`.
Un ejemplo modificado del material de clases:

``` python
class Persona:
    def __init__(self, name):
        self.name = name
        
    def __setstate__(self, state):
        print("Deserializando objeto...")
        state["name"] += " deserializado"
        self.__dict__ = state
```

##### Repartición del puntaje
- 1.5 puntos por mencionar `__setstate__`
- 1.5 puntos por código de ejemplo correcto

**NOTA:** Algunos alumnos utilizaron el argumento `object_hook` en la función `json.loads`. Esto no está completamente correcto, pues el enunciado dice que debe deserializarse un objeto **cualquiera**, y JSON no permite deserializar (directamente) instancias de clases en Python. En este caso, como máximo se asignaron 2 de 3 puntos.


#### 2. ¿Qué tipo de conexión usaría para implementar la transmisión de un partido de fútbol en tiempo real? Justifique su respuesta.

El tipo de conexión recomendable para streaming de video y audio en tiempo real es UDP. Esto es fundamentalmente porque es **más rápido**, debido a que:
- No es necesario establecer una conexión: se envían datos constantemente, y quien desea recibirlos lo hará. En el caso de TCP, si la conexión se cae, hay que volver a inicializarla, lo que toma tiempo.
- No se piden nuevamente los paquetes que hayan llegado en forma errónea.

Si bien con conexión UDP puede haber pérdida de información, en este caso es más crítica la rapidez. Es mejor perder un par de frames, pero continuar viendo la última información enviada, que quedarse esperando a que lleguen correctamente todos los frames, ralentizando la comunicación.


##### Repartición del puntaje
- 1.5 puntos por correcta identificación de la conexión UDP
- 1.5 puntos por justificación de qué es lo que se necesita para dicha transmisión. **NOTA**: si el alumno responde TCP, pero tiene claro que se necesita rapidez sin comprobar recepción de información, estos 1.5 puntos **sí se asignan**, por lo que debiera recibie 1.5 de 3 en la pregunta.



## Forma 2

#### 1. ¿Cómo es posible personalizar la serialización de un objeto cualquiera en Python? Escriba un ejemplo.

Implementando el método `__getstate__` en la clase de la cual el objeto es instancia. Este método recibe el objeto, y retorna el diccionario a ser guardado por pickle. Un ejemplo modificado del material de clases:

``` python
class Persona:
    def __init__(self, name):
        self.name = name
        
    def __getstate__(self):
        state = self.__dict__.copy()
        message = "Ayuda, me seralizan!"
        print(message)
        state["message"] = message
        return state
```

##### Repartición del puntaje
- 1.5 por mencionar `__getstate__`
- 1.5 por código de ejemplo correcto

**NOTA:** Algunos alumnos hicieron override del método `default` en una clase que hereda de `json.JSONEncoder`. Esto no está completamente correcto, pues el enunciado dice que debe deserializarse un objeto **cualquiera**, y JSON no permite serializar (directamente) instancias de clases en Python. En este caso, como máximo se asignaron 2 de 3 puntos.


#### 2. Desde el punto de vista del código, ¿cuáles son las principales diferencias entre la implementación de un cliente y un servidor en Python?

Depende de si la conexión es TCP o UDP, pero a grandes rasgos, en ambos casos es posible decir que:
- El servidor debe estar anclado (vía `bind`) a un cierto par `(host, port)` preestablecido y conocido por los clientes, mientras que el servidor no conoce de antemano la dirección de los clientes, sino que las recibe en el mensaje.
- Difieren también en el flujo del programa. El servidor está escuchando constantemente solicitudes a su dirección (por ejemplo, en un `while True`). Cuando recibe un mensaje, debe conocer el address de quien proviene (es entregada tanto por `accept` en TCP como por `recvfrom` en UDP) y decidir cómo responder (ya sea creando un socket específico para escuchar a dicho cliente en el caso TCP, o simplemente enviando algún paquete de vuelta con `sendto` en UDP). Por otra parte, el cliente tiene un flujo más "libre" en el sentido de que no está forzado a recibir datos en forma continua. Si no necesita nada más del servidor, basta con que nunca más llame nuevamente a `recv`.

##### Repartición de puntaje
1.5 puntos por cada diferencia bien definida y correcta. Si el alumno plantea otra diferencia correcta, también se asigna este puntaje.
**NOTA:** si el alumno expone solo la "segunda" diferencia, pero con el mismo nivel de detalle, se consideró completamente correcto y se asignaron 3 puntos.

## Forma 3

#### 1. Si fuese necesario realizar una acción sobre los elementos del diccionario retornado al deserializar un objeto JSON, ¿de qué manera es posible personalizar el formato retornado? Dé un ejemplo.

Esto puede hacerse con el argumento `object_hook` proporcionado a la función `json.loads`. Este argumento recibe una función (la que a su vez recibe un diccionario), y retorna un objeto deserializado en forma personalizada.

Para el ejemplo, basta con el que se provee en el material de clases, que carga los datos en forma de tupla en lugar de diccionario:

``` python
json_string = '{"nombre": "Jorge", "edad": 34, "estado_civil": "casado"}'
datos = json.loads(
    json_string,
    object_hook=lambda dict_obj: [(i,j) for i,j in dict_obj.items()]
)
```

También es posible hacer un ejemplo un poco más elaborado, como el siguiente:
```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    @staticmethod
    def from_dict(dict):
        if "age" not in dict or "name" not in dict:
            raise TypeError("Could not convert {}".format(dict))
        return Person(dict["name"], dict["age"])

json_string = '{"name": "Jorge", "age": 34, "useless": "sth here"}'
p = json.load(json_string, object_hook=Person.from_dict)
print(p.age)
```


##### Repartición del puntaje
- 1.5 puntos por mencionar el argumento `object_hook`
- 1.5 puntos por algún ejemplo correcto

#### 2. ¿Por qué el método `accept` de un socket no se usa en el protocolo UDP?

Porque el método `accept` se utiliza para establecer una conexión con el cliente (de hecho, retorna un socket creado específicamente para tal efecto) en respuesta a una solicitud de conexión (método `connect`). Lo anterior no es necesario en UDP, pues en este protocolo nunca se establece una conexión formal entre cliente y servidor: simplemente se envían mensajes desde y hacia las respectivas direcciones.

##### Repartición de puntajes
- 1.5 puntos por indicar qué hace `accept`
- 1.5 puntos por justificación de por qué no se utiliza en UDP


