## Pizzería


#### Parte 1: Modelamiento
Modelar la simulación de una pizzería donde llegan pedidos de pizza cada 7 minutos y las pizzas se demoran 15 minutos en cocinar. Además considere que hay un solo horno.

#### Parte 2: Agregando variabilidad
Ahora, considere que existen dos teléfonos donde a uno le llegan pedidos de manera que el tiempo entre pedidos distribuye exponencialmente con una tasa de 1/10 y al otro teléfono le llegan pedidos que distribuyen exponencialmente con una tasa de 1/13. 
También, la pizzería ahorró, vendió el horno anterior y se compró dos nuevos que se demoran uniform(10, 17) en cocinar la pizza.

#### Parte 3: Estadísticas
  * Sacar el promedio, máximo y mínimo de tiempo entre la llegada del pedido y la salida de éste. 
  * Calcular cantidad de pedidos que no se terminaron.


#### Parte 4: Implementación sistema delivery (propuesto)
Con los ahorros de la pizzería se pudieron comprar una moto y así ofrecer la opción de delivery. Ésta opción cumple con las siguientes características:
   - Aproximadamente la mitad de los pedidos son delivery. 
   - La moto lleva un mínimo de 4 pedidos y un máximo de 6 pedidos. Es decir, si hay de 4-6 pedidos listos la moto parte a repartirlos. 
   - El tiempo de repartición de pedidos se distribuye de forma uniforme(50, 70)