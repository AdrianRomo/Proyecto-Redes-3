# Repositorio con scripts importantes

## Colaboradores

[![Elias Muñoz Primero](https://avatars.githubusercontent.com/u/42790148?v=4&s=244)](https://github.com/elias160299)  | [![Nicolas Sanchez](https://avatars.githubusercontent.com/u/22784404?v=4&s=244)](https://github.com/NicolasSaG) | [![Adrian González Pardo](https://avatars.githubusercontent.com/u/33945793?v=4&s=244)](https://github.com/AdrianPardo99)
---|---|---|
[Elias Muñoz Primero](https://github.com/elias160299) |[Nicolas Sanchez](https://github.com/NicolasSaG) |[Adrian González Pardo](https://github.com/AdrianPardo99)

Scripts que se utilizaron y desarrollaron por el equipo La Pandilla Mantequilla, a la hora de realizar el proyecto de Administración de Servicios en Red (ASR)

Como nota importante las pruebas fueron realizadas en un OS Linux, Fedora revisar pruebas o expresiones utilizadas para OS Windows

# Notas importantes de GNS3

# Virtualización de alguna VM
Para algunos casos o topologías es necesario virtualizar un sistema operativo el cual pueda trabajarse en la misma topología para brindar algún servicio en caso de que este sea un servidor o en su defecto este sea un cliente el cual consumirá cierto servicio en el entorno de red.

En muchos casos y muchos tutoriales se leerá que es muy fácil usar VmWare o Virtualbox, los cuales indirectamente son software de licencia y muchas veces nos daremos de topes a la hora de instalar o de realizar nuestras tareas, por ello mejor usaremos el confiable Qemu/KVM el cual aprovecha al menos en un 100\% en Linux todo nuestro hardware el cual puede incluso virtualizar arquitecturas de otro ensamblador, ya sea ARM, i386 u otro tipo de ensamblador.

__Linux__

Instalación de algunos paquetes y libs que son necesarios:

* libvirt
* kvm
* qemu-system
* virt-manager
* virt-tools

# Configuración de Routers Cisco
Muchas veces nos veremos en la necesidad de configurar no solo a nivel de enrutamiento estático, de levantar alguna interfaz de red, muchas veces vamos a tener que decirle a nuestros routers, donde se encuentran nuestros servidores y en muchas otras ocasiones tendremos que administrar usuarios que tengan acceso a nuestros dispositivos vía protocolos como:
* SSH
* Telnet

## Un repaso rápido de IP y Mascaras de Red
Muchas veces tendremos que hacer uso Variable Length Subnet Mask (Mascara de Subred de Tamaño Variable) (VLSM), con IPs de distintas clases, pero inicialmente debemos conocer la tabla de direcciones IP para saber el rango disponible y el como se puede trabajar.

| Clase | Rango | Rango en binario | Prefijo de mascara de red | Mascara de Red |
| ----- | ----- | ---------------- | ------------------------- | -------------- |
|  A    | 1 - 126 | 0xxxxxxx - 01111110 | 8 | 255.0.0.0 |
|  B    | 128.0 - 191.255 | 10xxxxxx - 10111111 | 16 | 255.255.0.0 |
|  C    | 192.0.0 - 223.255.255 | 110xxxxx - 11011111 | 24 | 255.255.255.0 |

El resto de Clases no se utilizan debido a que funcionan como clases de IPs para Multicast o para otro fin.

Por ello pensemos que en la Clase A no se incluye el grupo de IPs 127 ya que este es usado directamente para el loopback o el localhost de nuestros mismo equipos.

Por otro lado un ejemplo de como hacer uso de clases es el siguiente:

Tenemos la IP 10.10.0.5 de la clase A, por ello obtendremos los siguientes datos:

| IP | ID de Red | Primer IP | Ultima IP | Dirección de Broadcast | Mascara de Red | Clase |
| -- | --------- | --------- | --------- | ---------------------- | -------------- | ----- |
| 10.10.0.5 | 10.0.0.0 | 10.0.0.1 | 10.255.255.254 | 10.255.255.255.255 | 255.0.0.0 | A |

Al obtener esto debemos destacar lo siguiente para trabajar y encontrar esta tabla de forma rápida, por ello primero debemos conocer inicialmente la clase de IP que es, a lo cual en este caso es inicialmente una clase A por lo cual la mascara de red es de 8 bits, con ello convertiremos nuestra IP que nos dan a binario y la mascara de red la convertiremos de igual manera a binario:

__10.10.0.5__ es equivalente a binario __00001010.00001010.00000000.00000101__

__255.0.0.0__ es equivalente a binario __11111111.00000000.00000000.00000000__

Con esto primero haremos la operación a nivel de bits como _AND_ la cual nos devolvera lo siguiente

__10.0.0.0__ siendo equivalente de la operación and __00001010.00000000.00000000.00000000__ que es nuestro ID de Red

Para obtener la dirección de Broadcast haremos uso de la operación _NOT_ en la mascara de red, lo cual nos otorga lo siguiente:

__0.255.255.255__ es equivalente a binario __00000000.11111111.11111111.11111111__

Obteniendo esto haremos uso de la compuerta _OR_ en el ID de Red

__10.255.255.255__ es equivalente a binario __00001010.11111111.11111111.11111111__

Y para obtener finalmente la primer y última IP solo haremos uso de la suma de 1 bit al último octeto del ID de red y la resta de 1 bit al último octeto de la dirección de Broadcast

__10.0.0.1 hasta 10.255.255.254__ siendo este nuestro rango util de IPs

Finalmente esto es para el caso de las IPs por clases, por ello es necesario pensar que son muchas direcciones IPs las que se quedan sin uso, por lo cual se puede crear una subred la cual tendrá una mascara de red distinta, la cual permitirá el ahorro de IPs y podrá reusar estas otras direcciones IP en muchos más dispositivo, un ejemplo de ello puede ser:

Se tiene el conjunto de direcciones IP de clase C __192.168.100.0/24__ En la cuales se plantea solo realizar uso de las primeras 5 IPs para un área local mientras que 15 IPs se harán uso para conectar y crear otra área de trabajo, la solución a este ejemplo sería hacer lo siguiente:

* Primero debemos preguntar si este número de IPs que vamos a usar consideran ya el uso de Gateway y por otro lado si ya se considera así mismo las direcciones de Broadcast y de ID de Red, en caso de que no se consideren esto es sumas 1 host más por cada elemento faltante para construir la subred

* Convertir el número de host a utilizar a binario por ejemplo: __5 hosts más los 3 elementos (Gateway, Broadcast e Identificador)__ que es igual a hacer uso de __8 hosts__ por ello su conversión a octeto sería __00001000__, mientras que haciendo lo mismo para el caso de los __18 hosts__ sería __00010010__ a lo cual nos daremos cuenta que para este caso se ven 2 bits del rango en 1, por lo cual esto no es factible para realizar el subneteo de nuestras direcciones, por ello recoreremos 1 bit a la izquiera y eliminaremos el bit más cercano de la derecha para realizar el subneteo quedando de forma decimal como __32 hosts__ siendo su equivalente en binario como __00100000__ de modo que los bits con cero a la derecha despues del 1 es lo que utilizaremos para trabajar y asignar direcciones IP, por ello sabemos que para las mascaras de red son 4 octetos por lo cual son 32 bits para trabajar, tomando en cuenta lo mencionado para el subneteo para los casos:

* __32 hosts__ se necesitan __5 bits__ por ello haremos la operación _32-5=27 bits_
* __8 hosts__ se necesitan __3 bits__ por ello haremos la operación _32-3=29 bits_

Por tanto nuestras direcciones quedaran como __192.168.100.x/27 y 192.168.100.y/29__, pero como seleccionaremos o asignaremos los valores para _x_ o _y_, pensemos de forma sencilla asignaremos el primer ID de Red a aquella subred que tenga el prefijo más pequeño, por lo cual tendremos que elegir primero a la que tiene la variable _x_, quedando como:

* __192.168.100.0/27__
  * ID de Red: 192.168.100.0 = 11000000.10101000.01100100.00000000
  * Mascara de Red: 255.255.255.224 = 11111111.11111111.11111111.11100000
  * Aplicando las operaciones pertinentes tendremos
    * Primer IP: 192.168.100.1
    * Ultima IP: 192.168.100.30
    * IP de Broadcast: 192.168.100.31
  * Cubriendo totalmente la demanda de 18 hosts teniendo 14 hosts que podemos usar más tarde en esa subred

Para el caso y deseo de que las direcciones de subneteo sean contiguas usaremos la IP que sigue después de la IP de Broadcast de la subred que ya construimos __192.168.100.0/27__:

* __192.168.100.32/29__
  * ID de Red: 192.168.100.32 = 11000000.10101000.01100100.00100000
  * Mascara de Red: 255.255.255.248 = 11111111.11111111.11111111.11111000
  * Aplicando las operaciones pertinentes tendremos
    * Primer IP: 192.168.100.33
    * Ultima IP: 192.168.100.38
    * IP de Broadcast: 192.168.100.39
  * Cubriendo el total de hosts deseados sin desperdiciar ningún hosts de modo que esta subred es la exacta para el conjunto de direcciones

Y de esta forma hemos concluido con el subneteo de las demas direcciones IP, de modo en que el resto de Hosts por el momento son resguardados, en caso de que se desee hacer una nueva subred con más hosts es necesario rehacer las operaciones pertinentes para que de este modo no se desperdicien IPs.

### Valores decimales dependiendo del prefijo de mascara de red

* _0_ = _0.0.0.0_
* _1_ = _128.0.0.0_
* _2_ = _192.0.0.0_
* _3_ = _224.0.0.0_
* _4_ = _240.0.0.0_
* _5_ = _248.0.0.0_
* _6_ = _252.0.0.0_
* _7_ = _254.0.0.0_
* _8_ = _255.0.0.0_
* _9_ =  _255.128.0.0_
* _10_ =  _255.192.0.0_
* _11_ =  _255.224.0.0_
* _12_ =  _255.240.0.0_
* _13_ =  _255.248.0.0_
* _14_ =  _255.252.0.0_
* _15_ =  _255.254.0.0_
* _16_ =  _255.255.0.0_
* _17_ =  _255.255.128.0_
* _18_ =  _255.255.192.0_
* _19_ =  _255.255.224.0_
* _20_ =  _255.255.240.0_
* _21_ =  _255.255.248.0_
* _22_ =  _255.255.252.0_
* _23_ =  _255.255.254.0_
* _24_ =  _255.255.255.0_
* _25_ =  _255.255.255.128_
* _26_ =  _255.255.255.192_
* _27_ =  _255.255.255.224_
* _28_ =  _255.255.255.240_
* _29_ =  _255.255.255.248_
* _30_ =  _255.255.255.252_
* _31_ =  _255.255.255.254_
* _32_ =  _255.255.255.255_

La cual estos prefijos representan la cantidad de bits que utilizan para la mascara, mientras para que saber cuantos hosts puede utilizar cada mascara es tan sencillo como _2^{32-prefijo de red}_ tomando en cuenta que es necesario recalcar que en la cantidad de hosts es necesario considerar la IP del Gateway, el ID de Red y la dirección de Broadcast para que no exista ningún problema a la hora de realizar el subneteo.

## Levantando interfaces de red con una IP
Para esto tomaremos de ejemplo un Router 1 cuya IP contiene los datos: __192.168.0.0/24__ a traves de la interfaz __FastEthernet 0/0__ lo cual es abreviada en GNS3 como __f0/0__

Para ello debemos hacer lo siguiente:
```bash
  # Para este punto debemos estar en el modo exec del router es decir que aparezca
  #   el mismo simbolo con el que estoy realizando este comentario "#" y no ">"
  conf t
    int f0/0
      ip add 192.168.0.1 255.255.255.0
      no sh
      end
  wr
```
Con esto finalmente podemos resaltar y hacer que las instrucciones a seguir para levantar cualquier interfaz y dirección como:
```bash
  conf t
    int <aquí_va_la_interfaz_con_su_identificador>
      ip add <IP_util_dentro_del_rango_de_IPs_primera_o_ultima_disponible> <Mascara_de_Red>
      no sh
      end
  wr
```
Para el caso de que se configuren múltiples interfaces en 1 router cambiar la palabra __end__ por un __exit__ para no repetir sentencias de comandos innecesariamente
## Creando Enrutamientos
Muchas veces necesitaremos el hacer uso de redireccionar el flujo de información hacia el exterior de nuestra red, por ello es que existe el enrutamiento  de la información, que no es pasar sencillamente de un punto a otro, en la cual el mismo dispositivo (Router) realiza una serie de operaciones para redireccionar el flujo de datos y de la misma manera conocer el como el mismo dispositivo conoce hacia donde mandar los datos sin necesidad de conocer todo el camino que recorre hasta llegar al destino.

### Enrutamiento estático
Este tipo de enrutamiento tiene una mayor prioridad sobre el resto de protocolos de enrutamiento, por lo cual es de suma utilidad y es muy rápido, una desventaja a su vez de este protocolo esta hecho para que su enrutamiento y configuración sea en redes pequeñas, por ello si existiese una topología muy grande este enrutamiento no sera una opción factible para trabajar.

Para crear un enrutamiento pondremos el siguiente ejemplo:

Tenemos 3 routers los cuales nombraremos:

* R1:
  * f0/0 cuya red es 192.168.0.0/25
  * f0/1 cuya red es 10.10.0.128/30 que interconecta con f0/1 de R2 (10.10.0.129)
* R2:
  * f0/1 cuya red es 10.10.0.128/30 que interconecta a f0/1 de R1 (10.10.0.130)
  * f1/0 cuya red es 10.10.0.132/30 que interconecta a f1/0 de R3 (10.10.0.133)
* R3:
  * f1/0 cuya red es 10.10.0.132/30 que interconecta a f1/0 de R2 (10.10.0.134)
  * f0/0 cuya red es 192.168.0.128/25

Para poder comunicar toda esta red solo haremos uso del comando _ip route_ descrito de la siguiente manera para enrutar el trafico de datos entre los dispositivos:

```bash
  # Para la tabla de enrutamiento de R1 seria:
  conf t
    ip route 192.168.0.128 255.255.255.128 10.10.0.130
    # En este caso se hara un enrutamiento generalizado que engloba las subredes
    #   que va del identificador 10.10.0.128/30 y 10.10.0.132/30 generalizado con
    #   10.10.0.128/29
    ip route 10.10.0.128 255.255.255.248 10.10.0.130
    end
  wr

  # Para la tabla de enrutamiento de R2 seria:
  conf t
    ip route 192.168.0.0 255.255.255.128 10.10.0.129
    ip route 192.168.0.128 255.255.255.128 10.10.0.134
    ip route 10.10.0.128 255.255.255.248 10.10.0.129
    ip route 10.10.0.128 255.255.255.248 10.10.0.134
    end
  wr

  # Para la tabla de enrutamiento de R3 seria:
  conf t
    ip route 192.168.0.0 255.255.255.128 10.10.0.133
    ip route 10.10.0.128 255.255.255.248 10.10.0.133
    end
  wr
```

Como podemos ver los pasos a seguir de forma general son:
```bash
  # Si alguna interfaz esta conectada a otra interfaz de red (router-router)
  conf t
    ip route <id_red_unknown> <netmask> <ip_de_donde_puedo_redireccionar>
    # ip_de_donde_puedo_redireccionar es la ip del otro router por el cual
    #   esta conectado de forma directa a nuestro router
    #   y asi llegaran los paquetes
    end
  wr
```

### Enrutamiento dinámico
El enrutamiento dinámico muchas veces funciona a la hora de crear tablas dinámicas y que estas a su vez estas se intercambien con los routers vecinos para tener un conocimiento total de toda la topología de red aledaña, para ello existen varios protocolos que te ayudan a comunicar los dispositivos con el exterior, por ello te presento los siguientes.

#### RIP
Este protocolo funciona como es un protocolo para enrutamiento dinámico el cual tiene la característica de ser un protocolo de vector distancia, este protocolo trabaja con datagrama y bajo el puerto 520, de este protocolo existen tres versiones de este protocolo los cuales a groso modo se caracterizan por:

* __RIPv1__: Es la primer versión de este protocolo, el cual tiene como característica el realizar enrutamiento por clases de IP's lo cual como ya vimos anteriormente el hacer uso de clases es útil cuando existe una cantidad extensa de equipos de cómputo a trabajar, pero en caso contrario esta versión no es tan funcional
* __RIPv2__: A diferencia de la versión anterior esta versión funciona para hacer uso de VLSM el cual permite crear tablas de enrutamiento dinámicas con subneteo necesario para que los otros dispositivos puedan trabajar
  * En este caso para habilitarlo en nuestro router solo haremos uso de lo siguiente:
```bash
  conf t
    router rip
    ver 2
    net <id_red_de_las_interfaces_del_mismo_router>
    # En caso de que se desee eliminar los posibles bucles de los routers
    no auto-summary
    end
  wr
```
* __RIPng__: Este tipo funciona para direcciones IPv6

#### OSPF
Este protocolo funciona al igual que RIP como un protocolo de enrutamiento dinámico el cual tiene la característica de ser un protocolo de Enrutamiento de Estado de Enlace (LSR), pero con la diferencia de que este protocolo trabaja con wildcards y con áreas de red, de modo en que un conocimiento rapido de wildcards es como la escritura inversa de la mascara de red, pero a diferencia de todo en este se especifica la cantidad de hosts que cubre en el rango de IPs que van a poder ser enrutadas, un ejemplo de wildcard puede ser lo siguiente:

* Tengamos dos subredes 192.168.1.0/25 y 192,168.0.0/25, en el cual encontramos el rango de IP de las subredes:
  * 192.168.1.1 - 192.168.1.126 con Broadcast 192.168.1.127
  * 192.168.0.1 - 192.168.0.126 con Broadcast 192.168.0.127
  * La cual una wildcard se debe hacer lo siguiente:
    * Convertir las IP's a nivel de bits
      * 11000000.10101000.00000001.00000001 hasta 11000000.10101000.00000001.01111110 y Broadcast 11000000.10101000.00000001.01111111
      * 11000000.10101000.00000000.00000001 hasta 11000000.10101000.00000000.01111110 y Broadcast 11000000.10101000.00000000.01111111
    * Por lo cual podemos ver que los primeros dos octetos no cambian por tanto esa parte de la Wildcart va marcada con 0's, y del otros dos octetos es necesario ver cuales bits son los que cambian, y los que van marcados con 1's es lo que vamos a escribir en la Wildcard, por tanto quedaría como:
    * 0.0.1.127 que esto puede enrutar ambas redes con el conjunto de direcciones disponibles incluyendo el Broadcast de ambos routers
Al momento de escribir este ejemplo en el router considerando que ambas redes estan en el mismo router solo es necesario escribir lo siguiente:

```bash
  conf t
    # Encender una interfaz de loopback para que el mismo protocolo no tenga
    #   ningun problema y definir una IP que no se utilizara
    int loop0
      ip add 210.0.0.x 255.255.255.255
      no sh
      exit
    # Asignar un identificador distinto en cada router
    router ospf 1
      v 2
      # Al definir un area de red es necesario pensar que estos dispositivos
      #   cercanos y pueden variar
      net 192.168.0.0 0.0.1.127 area 0
      end
  wr
```

Entonces generalizando esto quedaria:
```bash
  conf t
    int loop0
      ip add <IP_no_utilizada> 255.255.255.255
      no sh
      exit
    router ospf <x>
      v 2
      net <id_de_red_generalizado_normal> <wildcard> area <y>
      end
  wr
```

## Compartiendo protocolos de enrutamiento dinámico
En algunos casos o en modelos de desarrollo practico sera necesario el poder trabajar con distintos tipos de enrutamiento en nuestros dispositivos, los cuales al enfrentarse con otro protocolo, no prodran comunicarse, para ello solo es necesario, reconfigurar el protocolo principal e indicar que vamos a utilizar redireccionamiento con otros protocolos:

### OSPF
Para que el protocolo OSPF pueda detectar y trabajar con enrutamientos por RIP y estatico, se debe escribir lo siguiente:
```bash
  conf t
    router ospf <id>
      redistribute static metric 200 subnets
      redistribute rip metric 200 subnets
      end
```
### RIP
Para que el protocolo RIP pueda detectar y trabajar con enrutamientos por OSPF y estatico, se debe escribir lo siguiente:
```bash
  conf t
    router rip
    redistribute static
    redistribute ospf 1
    default-metric 1
    end
```
## Configurando para servicios de CLI remoto (Telnet/SSH)
Muchas veces y en lo laboral, se verán con la necesidad de acceder a un equipo que aun este en otro lado del mundo, se necesitara acceder de forma remota a dicho equipo, con esto presentaremos los siguientes pasos para habilitar el acceso por ssh o por telnet al router.

```bash
  conf t

    enable secret <escribir_aqui_la_contraseña_para_pasar_al_modo_exec>
    # Se habilita el servicio de cifrado para que los password
    #   no se vean en texto plano
    service password-encryption
    ip domain-name <escribir_aqui_el_nombre_de_dominio>
    ip ssh rsa keypair-name <key_para_generar_las_llaves>
    crypto key generate rsa usage-keys label <key_para_generar_las_llaves> modulus 1024

    ip ssh v 2
    ip ssh time-out 30
    ip ssh authentication-retries 3
    line vty 1 15
      password <password_cuando_no_hay_user>
      login local
      # en transport se habilita para el uso de telnet y ssh
      transport input ssh telnet
      exit
    # Aqui se crea el modelo para que entre al router y por default entra al modo >
    aaa new-model
    aaa authentication login default local
    aaa authentication enable default enable
  end
  wr
```

Y de esta manera ya esta la configuración para ingresar de forma remota al router

## Creación de usuarios administradores
Ahora bien el poder habilitar una conexión remota se puede hacer uso de usuarios con distintos niveles de privilegio para configurar o conectarse sencillamente al router, por ello se seguirá la siguiente serie de instrucciones:
```bash
  conf t
    username <user> privilege 15 password <pass>
    end
  wr
```

Como podemos ver a lado de la sentencia _privilege_ vemos un 15 el cual representa el nivel máximo de acceso y configuración para acceso al router, pero por otro lado también existen los niveles de permiso como:

* _0_ Predefinido para privilegios de acceso a nivel de usuario. Rara vez se usa, pero incluye cinco comandos: deshabilitar, habilitar, salir, ayudar y cerrar sesión.
* _1_ El nivel predeterminado para iniciar sesión con el indicador del enrutador Router>. Un usuario no puede realizar ningún cambio ni ver el archivo de configuración en ejecución.
* _2-14_ Puede personalizarse para privilegios de nivel de usuario. Los comandos de niveles inferiores se pueden mover a otro nivel superior, o los comandos de niveles superiores se pueden mover a un nivel inferior.
* _15_ Reservado para los privilegios del modo de habilitación (comando de habilitación). Los usuarios pueden cambiar configuraciones y ver archivos de configuración.
