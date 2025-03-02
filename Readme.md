# DJANGO-ADMIN-BOILERPLATE

## Variables de Entorno
| **Nombre**               | **Descripción**                                        | **Required** |
| ------------------------ | ------------------------------------------------------ | ------------ |
| `DJANGO_SETTINGS_MODULE` | Módulo de configuración de Django.                     | `✓`          |
| `SECRET_KEY`             | Clave secreta de Django.                               | `✓`          |
| `DEBUG`                  | Indica si el modo de depuración está activado.         | `✓`          |
| `ALLOWED_HOSTS`          | Lista de hosts permitidos para el servidor.            | `x`          |
| `CSRF_TRUSTED_ORIGINS`   | Lista de orígenes de confianza para CSRF.              | `✓`          |
| `POSTGRES_DB`            | Nombre de la base de datos PostgreSQL.                 | `✓`          |
| `POSTGRES_USER`          | Usuario de la base de datos PostgreSQL.                | `✓`          |
| `POSTGRES_PASSWORD`      | Contraseña del usuario de la base de datos PostgreSQL. | `✓`          |
| `POSTGRES_HOST`          | Host del servidor PostgreSQL.                          | `✓`          |
| `POSTGRES_PORT`          | Puerto del servidor PostgreSQL.                        | `✓`          |
| `LANGUAGE_CODE`          | Código de idioma predeterminado.                       | `✓`          |
| `TIME_ZONE`              | Zona horaria predeterminada.                           | `✓`          |
| `CACHE_REDIS_URL`        | URL de conexión a la caché Redis.                      | `✓`          |
| `CELERY_BROKER_URL`      | URL de conexión al broker de Celery.                   | `✓`          |
| `EMAIL_HOST`             | Host del servidor de correo electrónico.               | `x`          |
| `EMAIL_PORT`             | Puerto del servidor de correo electrónico.             | `x`          |
| `EMAIL_HOST_USER`        | Usuario del servidor de correo electrónico.            | `x`          |
| `EMAIL_HOST_PASSWORD`    | Contraseña del servidor de correo electrónico.         | `x`          |
| `EMAIL_USE_TLS`          | Indica si se usa TLS para el servidor de correo.       | `x`          |
| `EMAIL_USE_SSL`          | Indica si se usa SSL para el servidor de correo.       | `x`          |


## Ejecución del Proyecto con Docker Compose para Desarrollo

Para ejecutar el proyecto sigue estos pasos:

### 1. Configura las Variables de Entorno

1. **Crea un archivo `.env`** basado en el archivo de ejemplo `.env.sample` que se encuentra en el repositorio. Este archivo contiene las variables de entorno necesarias para configurar el proyecto.

    ```bash
    cp .env.sample .env
    ```

2. **Edita el archivo `.env`** para establecer las variables de entorno adecuadas. Asegúrate de proporcionar valores correctos para todas las variables. Puedes usar cualquier editor de texto para editar el archivo.

    ```ini
    # SECURITY
    DJANGO_SETTINGS_MODULE=core.settings.local
    SECRET_KEY=secret-key
    DEBUG=True
    ALLOWED_HOSTS=*

    # DATABASES
    POSTGRES_DB=postgres-db
    POSTGRES_USER=postgres-user
    POSTGRES_PASSWORD=postgres-password
    POSTGRES_HOST=db
    POSTGRES_PORT=5432

    # INTERNATIONALIZATION
    LANGUAGE_CODE=es
    TIME_ZONE=UTC

    # CACHE
    CACHE_REDIS_URL=redis://redis:6379/0

    # CELERY
    CELERY_BROKER_URL=redis://redis:6379/1
    ```

### 2. Ejecuta el Proyecto

1. **Usa Docker Compose para levantar el contenedor.** Asegúrate de que Docker y Docker Compose estén instalados en tu máquina.

    ```bash
    docker-compose up
    ```

    Este comando ejecutará el contenedor con la configuración definida en `docker-compose.yml`, usando el archivo `.env` para las variables de entorno.

### Notas Adicionales

- Si deseas ejecutar el contenedor en segundo plano, añade la opción `-d` al comando de Docker Compose:

    ```bash
    docker-compose up -d
    ```

- Para detener el contenedor, puedes usar:

    ```bash
    docker-compose down
    ```
