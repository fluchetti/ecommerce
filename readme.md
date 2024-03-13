# Ecommerce

Este proyecto es una simulacion de una tienda virtual.

La aplicación está desplegada en Netlify. Podes verla e interactuar con ella [aquí](https://ecommercefluch.netlify.app/).

#

## Stack

- Django rest framework
- React
- Bootstrap

#

## Funcionalidades

La aplicacion distingue entre tres tipos de usuarios.

- **Visitantes**
- **Usuarios**
- **Administradores / Staff (no implementado en frontend)**

### Visitantes

Los visitantes pueden interactuar con la aplicacion viendo productos, categorias y vendedores. Ademas pueden iniciar sesion o registrarse.

### Usuarios

Los usuarios, ademas de los permisos ya nombrados, pueden crear, editar y borrar productos (los suyos). Editar y borrar su cuenta. Cambiar su contraseña. "Realizar compras" agregando productos al carrito y haciendo un checkout. Pueden ver sus productos y sus compras.

### Administradores y Staff

Los admin y staff tienen permisos sobre todas las funcionalidades de la aplicacion. Pueden hacer todo lo nombrado anteriormente y ademas administar las categorias.

#

## Aprendizajes

Muchos. Entre ellos:

- JWT: como funcionan y sus limitaciones. Refresh y blacklisting.

- Manejo de imagenes: parsers y FormData.

- Testsing: una introduccion a los unit test. **Aprender sobre Faker y Factory Boy**

#

## Mejoras

Tambien muchas. Algunas que se me ocurren:

- Relacion OneToOne entre cuenta y datos de la cuenta.

- Integrar un sistema de checkout.

- Endpoints y estructura del proyecto: seguir convenciones y mejores practicas.

- Optimizar las respuestas: algunos serializadores retornan datos que luego no son utilizados en el frontend.

- Optimizar consumo de recursos: se almacena demasiada informacion no relevante en estados y contextos, tambien se hacen muchas peticiones.

- Mejorar aspecto de la aplicacion y su responsiveness.

- Agregar mas mensajes/alertas para la interaccion del usuario.
