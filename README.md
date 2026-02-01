# Turismo Web App

![HTML5](https://img.shields.io/badge/HTML5-Frontend-orange)
![CSS3](https://img.shields.io/badge/CSS3-Style-blue)
![JavaScript](https://img.shields.io/badge/JavaScript-Frontend-yellow)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=flat&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-green?style=flat&logo=flask)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue?style=flat&logo=docker)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?style=flat&logo=mysql)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat)

## Descripción General

Este proyecto es una aplicación web de turismo moderna y segura, diseñada con una **arquitectura Cloud Native** basada en **Microservicios**. El sistema está orquestado mediante **Docker**, garantizando portabilidad, escalabilidad y un entorno de desarrollo consistente.

El núcleo de la aplicación utiliza **Flask** para la lógica de negocio y **MySQL** para la persistencia de datos, implementando prácticas avanzadas de seguridad como el cifrado de sesiones autenticadas.

---

## Tecnologías y Arquitectura

### Stack Tecnológico
*   **Backend**: Flask (Python 3.11+) - Ligero y eficiente.
*   **Base de Datos**: MySQL 8.0 - Robusta y escalable.
*   **Frontend**: HTML5, CSS3, JavaScript - Interfaz responsiva y elegante.
*   **Orquestación**: Docker Compose - Gestión de microservicios aislados.

### Arquitectura de Microservicios
La aplicación se compone de servicios desacoplados que corren en contenedores independientes dentro de una red virtual privada:
1.  **Servicio Web (Flask)**: Maneja las peticiones HTTP, la lógica de negocio y la renderización de vistas.
2.  **Servicio de Datos (MySQL)**: Persistencia de datos aislada en su propio contenedor.

### Características de Seguridad (Security by Design)
Este proyecto prioriza la seguridad desde su concepción:
*   **Aislamiento de Red**: Los servicios se comunican internamente; solo se exponen los puertos estrictamente necesarios.
*   **Cifrado de Sesión Avanzado**: Implementación de sesiones personalizadas mediante **AES-GCM (Advanced Encryption Standard - Galois/Counter Mode)**. Esto garantiza no solo la confidencialidad de la cookie de sesión, sino también su integridad y autenticidad, previniendo ataques de manipulación o falsificación.
*   **Gestión de Secretos**: Uso estricto de variables de entorno (`.env`) para manejar credenciales, evitando el *hardcoding* de información sensible en el código fuente.
*   **Protección contra Inyecciones SQL**: Uso de consultas parametrizadas en todas las interacciones con la base de datos.
*   **Hashing de Contraseñas**: Almacenamiento seguro de credenciales utilizando **bcrypt**.

---

## Instalación y Despliegue

Sigue estos pasos para levantar el entorno completo en tu máquina local utilizando Docker.

### 1. Requisitos Previos
*   [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y corriendo.
*   [Git](https://git-scm.com/) instalado.

### 2. Clonar el Repositorio
```bash
git clone https://github.com/hideonn1/tourism-web-project.git
cd tourism-web-project/main
```

### 3. Configuración de Variables de Entorno
Crea un archivo llamado `.env` en la carpeta `main` basado en el ejemplo proporcionado.

```bash
cp .env.example .env
```
> [!IMPORTANT]
> **Nota de Seguridad**: Abre el archivo `.env` creado y asegúrate de configurar una `SECRET_KEY` segura y las credenciales de la base de datos. Este archivo es crítico y está excluido de Git para proteger tus secretos.

### 4. Levantar Servicios con Docker
Ejecuta el siguiente comando para construir las imágenes y levantar los contenedores en segundo plano:

```bash
docker-compose up --build -d
```
Docker descargará las imágenes necesarias (Python, MySQL), instalará las dependencias y configurará la base de datos automáticamente.

---

## Uso de la Aplicación

Una vez que los contenedores estén en estado "Up" (corriendo), puedes acceder a los servicios:

*   **Web App**: [http://localhost:5000](http://localhost:5000)
*   **Base de Datos**: Accesible internamente por la app, o externamente en el puerto `3306` si necesitas conectar un cliente SQL local.

### Credenciales de Acceso (Demo)
El sistema puede incluir datos de prueba (si se cargó el script SQL inicial). Prueba con:
*   **Administrador**: `admin@admin.cl` / `Administrador123?`
*   **Cliente**: `cliente@cliente.cl` / `Cliente123?`

O regístrate como un nuevo usuario desde la interfaz.

---

## Comandos Útiles de Docker

*   **Ver Logs en tiempo real**:
    ```bash
    docker-compose logs -f web
    ```
*   **Detener los servicios**:
    ```bash
    docker-compose stop
    ```
*   **Eliminar contenedores y red** (para reiniciar limpio):
    ```bash
    docker-compose down
    ```
    *(Nota: Esto no borra los datos de la base de datos si el volumen está persistente).*

---

## © Licencia
Distribuido bajo la licencia MIT.
