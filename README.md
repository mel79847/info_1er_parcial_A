# Infografia - Universidad Privada Boliviana 1er parcial A

## Descripción

Este repositorio contiene el código base para el proyecto de tipo A.

Este proyecto implementa la funcionalidad base del videojuego Angry Birds. El proyecto contiene código para la mecánica fundamental y los objetos necesarios. Usted deberá completar el código fuente e implementar funcionalidades adicionales.

## Instrucciones

Para ejecutar el programa de arcade:

1. Clone (o forkee) el repositorio en un directorio local.
2. Abra la carpeta completa con Visual Studio code.
3. Ejecute el archivo main.py.

Siga las instrucciones para la implementación de la evaluación.

### Implementación de mecánicas faltantes

La primera parte refiere a la implementación de mecánicas faltantes, en específico, usted deberá implementar las siguientes funciones en el archivo `game_logic.py`:

 - `get_angle_radians`: Esta funcion recibe 2 puntos (Point2D) y devuelve el ángulo entre los mismos en radianes.
 - `get_distance`: Esta función recibe 2 puntos y devuelve la distancia en pixeles entre ambos puntos.
 - `get_impulse_vector`: Usando las funciones anteriores, esta función recibe 2 puntos y devuelve un vector de impulso (ImpulseVector) con el ángulo y el valor del impulso.

La implementación de las funciones restantes completa la mecánica básica del lanzamiento de un angry bird. Una vez terminada la implementación pruebe y valide el funcionamiento del proyecto. Luego de validar el funcionamiento, pase a la siguiente sección.

### Implementación de características adicionales

Una vez completada la implementación de la mecánica principal, usted deberá implementar las siguientes características como nuevas clases en el archivo `game_object.py`:

#### Yellow bird

Si el usuario hace clic izquierdo mientras el Yellow Bird está en vuelo, el mismo incrementará su impulso en la dirección en la que está apuntando por un multiplicador aplicado al impulso inicial. El multiplicador estará definido como un argumento al método de inicialización y deberá tener un valor de 2 por defecto.

#### Blue bird

Si el usuario hace clic izquierdo mientras el blue bird está en vuelo, éste se convertirá en 3 blue birds instantáneamente, cada uno con una separación de dirección de 30 grados. Por ejemplo, si en el momento del clic el blue bird tiene una dirección de -10 grados, los 3 blue birds resultantes deberán tener direcciones de 20, -10 y -40 grados respectivamente. La velocidad deberá mantenerse para los 3 pájaros.

#### (Extra) Implementación de niveles

La lógica de lanzamiento y destrucción de objetos está implementada en el código base. Como un extra, usted podrá implementar la lógica de gestión de niveles en base a un puntaje mínimo a alcanzar.

### Envío del código

Usted deberá enviar un enlace a un repositorio de github que solamente contendrá el código del proyecto en cuestión. Se recomienda que, para salvar inconvenientes con GIT, usted realice un fork de este repositorio en su propia cuenta, y luego clone el fork a su directorio local. 

Una vez finalizadas las tareas, se deberá enviar un email por grupo con los siguientes datos:

 - Destinatario: eduardo.laruta+tareas@gmail.com
 - Asunto: 1era Evaluacion parcial Infografia
 - Contenido: Nombres y códigos de los integrantes y el enlace al repositorio de GitHub

#IMPORTANTE PARA EL PROYECTO
El pryecto se encuentra en la rama de feat/power-niveles


