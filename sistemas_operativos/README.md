## **Unidad 1: Fundamentos de Sistemas Operativos**

### **1.1 Concepto y evolución de los Sistemas Operativos**

Un **Sistema Operativo (SO)** es un software que actúa como intermediario entre los usuarios y el hardware de un computador. Su principal función es gestionar los recursos del sistema (CPU, memoria, almacenamiento, dispositivos de entrada/salida) y proporcionar una interfaz para que los usuarios y aplicaciones interactúen con el hardware de manera eficiente y segura.

#### **Evolución de los Sistemas Operativos**

1.  **Primera generación (1940-1955): Computación sin SO**
    
    -   No existían sistemas operativos.
    -   Los programas se ejecutaban directamente en el hardware mediante interruptores y tarjetas perforadas.
2.  **Segunda generación (1955-1965): Procesamiento por lotes (Batch Systems)**
    
    -   Se introducen los primeros sistemas operativos simples.
    -   Se usaban tarjetas perforadas para cargar programas y los trabajos se procesaban en lotes.
3.  **Tercera generación (1965-1980): Multiprogramación y tiempo compartido**
    
    -   Introducción de la multiprogramación, donde varios programas se ejecutan simultáneamente.
    -   Sistemas de tiempo compartido (como Unix), que permiten que múltiples usuarios utilicen el sistema al mismo tiempo.
4.  **Cuarta generación (1980-presente): Sistemas operativos modernos**
    
    -   Aparición de sistemas operativos gráficos (GUI), como Windows y macOS.
    -   Popularización de los sistemas embebidos y móviles (Android, iOS).
    -   Desarrollo de SO distribuidos y en la nube.

----------

### **1.2 Arquitectura y componentes de un Sistema Operativo**

Los sistemas operativos están estructurados en varias capas que permiten la comunicación entre el hardware y el software de aplicación.

#### **Componentes principales**

1.  **Gestor de procesos**
    
    -   Administra la ejecución de programas.
    -   Implementa la multitarea y controla la asignación de CPU.
2.  **Gestor de memoria**
    
    -   Controla la asignación y liberación de memoria RAM.
    -   Implementa técnicas como paginación y segmentación.
3.  **Gestor de almacenamiento**
    
    -   Maneja el acceso a discos duros, SSD y otros dispositivos de almacenamiento.
    -   Implementa sistemas de archivos (NTFS, ext4, FAT32).
4.  **Gestor de entrada/salida (E/S)**
    
    -   Coordina la comunicación entre el sistema y dispositivos como teclados, ratones, impresoras.
5.  **Gestor de seguridad y control de acceso**
    
    -   Protege el sistema de accesos no autorizados y amenazas.
6.  **Interfaz de usuario**
    
    -   Puede ser una línea de comandos (CLI) o una interfaz gráfica (GUI).

----------

### **1.3 Tipos de Sistemas Operativos**

Los sistemas operativos se pueden clasificar según su funcionalidad y uso:

1.  **Sistemas operativos monousuario vs. multiusuario**
    
    -   **Monousuario:** Solo permite un usuario a la vez (Windows Home).
    -   **Multiusuario:** Varios usuarios pueden acceder simultáneamente (Linux, Unix).
2.  **Sistemas operativos de procesamiento por lotes**
    
    -   Ejecutan tareas en lotes sin intervención del usuario.
3.  **Sistemas operativos de tiempo real**
    
    -   Responden en tiempos predecibles (usados en control de robots, aeronaves).
4.  **Sistemas operativos de red y distribuidos**
    
    -   Permiten compartir recursos en una red (Windows Server, Linux Server).
    -   Los SO distribuidos gestionan múltiples nodos como si fueran un solo sistema.
5.  **Sistemas operativos móviles y embebidos**
    
    -   Diseñados para smartphones (Android, iOS) o dispositivos específicos (SO de automóviles, electrodomésticos).

----------

### **1.4 Interrupciones y System Calls**

#### **Interrupciones**

Las **interrupciones** son señales enviadas al procesador para llamar su atención sobre un evento urgente, permitiendo que el SO responda rápidamente sin esperar que termine la ejecución actual.

Tipos de interrupciones:

1.  **Interrupciones de hardware** (generadas por dispositivos externos como teclado o impresora).
2.  **Interrupciones de software** (por errores o instrucciones del usuario, como una excepción de división por cero).

#### **System Calls**

Las **llamadas al sistema (system calls)** son funciones que permiten a los programas de usuario solicitar servicios del SO, como:

-   **Gestión de procesos:** `fork()`, `exec()`
-   **Gestión de archivos:** `open()`, `read()`, `write()`, `close()`
-   **Gestión de memoria:** `malloc()`, `free()`
-   **Gestión de dispositivos:** `ioctl()`, `read()`, `write()`


> Written with [StackEdit](https://stackedit.io/).