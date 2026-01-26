# Turismo Web App

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-green)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange)
![HTML5](https://img.shields.io/badge/HTML5-Frontend-orange)
![CSS3](https://img.shields.io/badge/CSS3-Style-blue)
![JavaScript](https://img.shields.io/badge/JavaScript-Frontend-yellow)
![License](https://img.shields.io/badge/License-MIT-purple)

## Descripción General

**Turismo Web App** es una plataforma integral para la gestión de una agencia de viajes moderna. Este sistema permite la administración eficiente de destinos turísticos, paquetes de viaje y reservas de clientes, ofreciendo una experiencia de usuario fluida y segura.

---

## Características Principales

*   **Gestión de Usuarios y Roles**: Sistema robusto de autenticación y autorización con roles diferenciados (Administrador y Cliente).
*   **Catálogo Turístico**: Administración completa (CRUD) de Destinos y Paquetes Turísticos.
*   **Motor de Reservas**: Flujo lógico para la creación de reservas, validando disponibilidad de cupos y fechas en tiempo real.
*   **Panel de Administración**: Herramientas exclusivas para que los administradores gestionen la oferta comercial.
*   **Interfaz Responsiva**: Diseño web limpio y adaptable utilizando HTML5 y CSS3.

---

## Arquitectura de Software

El proyecto ha sido diseñado siguiendo una arquitectura en capas estricta para garantizar la **escalabilidad**, **mantenibilidad** y **testabilidad** del código.

### Capas del Sistema
1.  **Capa de Presentación (Flask Views & Bases)**: Maneja las solicitudes HTTP y renderiza las plantillas HTML. Se comunica únicamente con la capa de servicio.
2.  **Capa de Lógica de Negocio (Services)**: Contiene toda la lógica del dominio. Aquí se ejecutan las validaciones, cálculos y reglas de negocio antes de persistir cualquier dato.
3.  **Capa de Acceso a Datos (Repositories)**: Abstracción pura sobre la base de datos. Se encarga de ejecutar las consultas SQL y mapear los resultados a objetos del dominio (Modelos).

### Patrones de Diseño Implementados
Este proyecto es un ejemplo práctico de patrones de diseño profesionales:

*   **Repository Pattern**: Desacopla la lógica de negocio de la implementación específica de la base de datos, permitiendo cambios futuros en el motor de base de datos con mínimo impacto.
*   **Dependency Injection**: Las dependencias (como los repositorios) se inyectan en los servicios a través de sus constructores. Esto elimina el acoplamiento fuerte y facilita las pruebas unitarias.
*   **Data Transfer Objects (Modelos)**: Uso de clases POJO (Plain Old Python Objects) para transferir datos entre capas de manera estructurada y tipada.

---

## Medidas de Seguridad

La seguridad es un pilar fundamental de esta aplicación:

*   **Protección contra SQL Injection**: Todos los repositorios utilizan **Consultas Parametrizadas** estrictas, previniendo la inyección de código malicioso en la base de datos.
*   **Hashing de Contraseñas**: Las contraseñas nunca se guardan en texto plano. Se utiliza **bcrypt** para el hashing y salting, cumpliendo con los estándares modernos de seguridad.
*   **Validación de Entradas**: Se emplean expresiones regulares (Regex) para validar rigurosamente datos sensibles como RUT, correos electrónicos y teléfonos antes de que lleguen a la base de datos.
*   **Gestión de Sesiones**: Uso seguro de sesiones de Flask para mantener el estado del usuario autenticado.

---

## Stack Tecnológico

*   **Backend**: Python 3.11, Flask
*   **Base de Datos**: MySQL
*   **Librerías**: `mysql-connector-python`, `bcrypt`
*   **Frontend**: HTML5, CSS3, JavaScript
*   **Control de Versiones**: Git

---

## Instalación y Despliegue Local

Sigue estos pasos para ejecutar el proyecto en tu máquina local:

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/proyecto-web-turismo.git
cd proyecto-web-turismo/main
```

### 2. Configurar la Base de Datos
1. Asegúrate de tener un servidor MySQL corriendo (ej. XAMPP).
2. Importa el archivo `sql/bd_pjd.sql` para crear la estructura de la base de datos.
3. Verifica que las credenciales en `config.py` coincidan con tu servidor local.

### 3. Configurar el Entorno Virtual
Para mantener las dependencias aisladas:

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 5. Ejecutar la Aplicación
```bash
python app.py
```
Accede a la aplicación en: `http://localhost:5000`

---

© 2026 - Distribuido bajo la licencia MIT.
