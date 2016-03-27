# Control 1

## Forma 1

### Cada pregunta vale 2 pts

####1. ¿Qué significa que las tuplas sean inmutables? ¿Qué ventaja tiene?
Significa que después de haber sido creadas no se pueden modificar, agregar o eliminar elementos. Una ventaja que tienen es que, a diferencia de las listas, pueden ser usadas como llaves en diccionarios.

#####Repartición del puntaje
- 1 punto si explica que son:
	- No se pueden agregar elementos
	- No se pueden eliminar elementos
	- No se pueden cambiar los elementos que ya se ingresaron
- 1 punto si da una ventaja:
	- Decir que se pueden usar como llaves en diccionarios
	- Que permiten almacenar una estructura de datos fija

No se consideraron buenas ventajas del tipo: "permite guardar datos que serán estáticos"

####2. ¿Qué elementos se seleccionan de las lista 'd' al ejecutar ```d[:-c]```?
Se seleccionan todos los elementos desde el índice 0 hasta el índice ```len(d)-c``` (no inclusive). Por ejemplo:
``` python
a = [1,2,3,4,5]
>>> a[:-1]
[1, 2, 3, 4]
```
#####Repartición del puntaje
- 1 punto por indetificar dónde comienza
- 1 punto por identificar dónde termina

####3. Tiene un archivo de texto (.txt) que contiene los nombres de los alumnos de IIC2233, algunos aparecen duplicados (no necesariamente seguidos). Escriba una línea de comandos que genere un nuevo archivo de testo con una lista de los nombres del curso sin duplicados.

``` sh
uniq file.txt > new_file.txt
```
#####Repartición del puntaje
- 1 punto por usar uniq
- 1 punto escribir el archivo

##Forma 2

### Cada pregunta vale 3 pts

####1. ¿Qué elementos se seleccionan de las lista 'd' al ejecutar ```d[a:b:c]```?
Se seleccionan los elementos desde el índice ```a``` hasta el ```b``` (no inclusive) cada ```c``` índices. Por ejemplo:
``` python
a = [1,2,3,4,5]
>>> a[1:4:2]
[2, 4]
```
#####Repartición de puntaje
- 1 punto por saber dónde empieza
- 1 punto por saber dónde termina
	- menos 0.5 si no dice que no se incluye ```d[b]```
- 1 punto por saber que c es un step

####2. Tiene un archivo de texto con los nombres de los alumnos de IIC2233 de este semestre. Mediante la línea de comandos escriba un nuevo archivo de texto que contenga una lista ordenada con todos los nombres que contengan *Per* en el nombre o apellido, independientemente si está escrito con mayúscula o minúscula

``` sh
grep -i Per file.txt | sort > new_file.txt
```

#####Repartición de puntaje
- 1 punto por ordenar
- 1 punto por usar grep
- 1 punto por usar -i

##Forma 3

### Cada pregunta vale 2 pts

####1. ¿Qué elementos se seleccionan de las lista 'd' al ejecutar ```d[:b]```?
Se seleccionan todos los elementos desde el índice 0 hasta el índice ```b``` (no inclusive). Por ejemplo:
``` python
a = [1,2,3,4,5]
>>> a[:3]
[1,2,3]
```
##### Repartición de puntaje
- 1 por identificar que parte de cero
- 1 por identificar que termina b no inclusive
	- menos 0.5 si no dice que no se incluye ```d[b]```

####2. ¿Cuál es la diferencia entre *Duck Typing* y *Poliformismo*?
El *Poliformismo* es la habilidad de varios tipos de tener una interfaz en común, la cuál debe ser declarada de forma **explícita**. Esto se puede lograr a través de herencia, o interfaces (que no existen en python). En python usamos polimorfismo cuando utilizamos herencia. Aquí podemos hacer que las subclases sobreescriban los métodos de la clase base o que los utilicen y expandan sus funcionalidades. Podríamos tener una clase ```Animal``` y una clase ```Pato``` que hereda de ```Animal```. La clase base tiene un método ```hablar()``` que ```Pato``` sobreescribe, el método ```ganar_energía()``` que es el mismo de ```Animal``` y el método ```volar()``` que el padre no tenía.

Que un lenguaje admita *Duck Typing* significa que el código puede manejar y aceptar cualquier objeto que implemente un método con una firma en particular. La filosofía es "Si se ve como pato, entonces puede actuar como pato". Por ejemplo, en el siguiente código vemos que se puede ejecutar el método ```hablar()``` de cualquiera de las clases, ya que este tiene la misma firma (igual nombre y parámetros).
``` python
lista = [Animal(), Pato(), Libro(), Arbol()]
for item in lista:
	item.hablar()
```
Con ambos se puede lograr tener una interfaz para poder tratar con los objetos de forma homogénea, la diferencia radica en que la interfaz del poliformismo está basada en los tipos y es explícita (heredo los métodos y atributos de una clase), mientras que en duck typing esta interfaz se logra a través de un contrato en común (implemento el método con la misma firma).


##### Repartición de puntajes
- Si explicaron ambos y luego explicaron la diferencia
    - 0.5 punto por explicar polimorfismo
    - 0.5 punto por explicar Duck Typing
    - 1 por la diferencia
- Si solo explicaron la diferencia
	- 2 puntos

Muchos confundieron los conceptos de la pregunta con overriding, overloading y herencia.

####3. Escriba un comando que cree el archivot "Hola Mundo.txt" con el string "Hola Mundo" escrito dentro del archivo

``` sh
echo "Hola Mundo" > Hola\ Mundo.txt
```
#####Repartición de puntaje
- 0.8 punto por escribir al archivo
- 0.2 si escriben bien el nombre del archivo (el espacio)
- 1 si usan echo
