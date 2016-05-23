# Control 4

### Forma 1

#####(6 pts.) Cuando queremos hacer override del método `__init__` en una metaclase personalizada, ¿qué significa el primer argumento que recibe el método? ¿Para qué se una en general este argumento? Justifique

El primer argumento es la clase que acaba de ser creada por el método `__new__`. Se utiliza cuando necesitamos modificar la clase después de que fue creada.

----------

### Forma 2
#####(6 pts.) Cuando queremos hacer override del método `__new__` en una metaclase personalizada, ¿qué significa el primer argumento que recibe el método? ¿Es necesario retornar algo? Justifique

El primer argumento es la metaclase que va a modificar la clase que será creada. El método `__new__` **debe** retornar la clase creada por `type` (la clase padre de la metaclase). Esta clase retornada es la que luego recibe el método `__init__` para ser inicializada (después de haber sido creada).

----------

### Forma 3
#####(6 pts.) Cuando queremos hacer override del método `__call__` en una metaclase personalizada, ¿qué significa cada uno de los argumentos que recibe el método? ¿Qué es lo que controla este método? Justifique

El primer argumento es la clase que fue creada y moficada por `__new__` e `__init__` respectivamente. Los otros argumentos son los necesarios para inicializar un objeto de la clase creada, es decir, son los argumentos de del `__init__` de la clase creada.

Este método controla la creación de un nuevo objeto de la clase que fue creada con la metaclase.
