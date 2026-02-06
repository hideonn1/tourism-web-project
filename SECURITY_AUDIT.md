# 🛡️ Reporte de Auditoría de Seguridad: Explora360 06/02/2026

Este documento detalla las pruebas de penetración y las medidas de mitigación implementadas para asegurar la integridad y disponibilidad de la plataforma Explora360.

## 1. Resumen de Defensas Implementadas

*   **Capa de Aplicación:** Validación estricta de tipos de datos mediante expresiones regulares (Regex).
*   **Capa de Sesión:** Implementación de `EncryptedCookieSessionInterface` con cifrado AES-GCM.
*   **Capa de Red:** Control de flujo y tasa de peticiones mediante `Flask-Limiter` y `ProxyFix`.

## 2. Evidencia de Pruebas (Pentesting)

### A. Mitigación de Fuerza Bruta (Rate Limiting)

Se realizó un ataque coordinado mediante **Hydra v9.6** desde un entorno Arch Linux para estresar el endpoint de autenticación.

**Resultado:** Bloqueo exitoso. El servidor detectó la anomalía y respondió con códigos HTTP 429 (Too Many Requests) tras alcanzar el límite configurado de 5 intentos por minuto.

![Logs de Flask](main/docs/assets/hydra-pentest.png)

*Figura 1: Logs de Flask (derecha) mostrando el rechazo de peticiones una vez activada la defensa.*

### B. Validación de Backend contra Inyección (XSS Bypass)

Se intentó realizar un bypass de las validaciones del frontend (HTML5) enviando un payload de Javascript directamente al servidor mediante `curl`.

**Payload:** `<script>alert("XSS_EXITOSO")</script>`

**Resultado:** Rechazo íntegro. Los filtros del frontend (HTML5) y backend (Regex) bloquearon el payload.

![Validación de Backend](main/docs/assets/register_screenshot.png)

*Figura 2: Respuesta del servidor bloqueando caracteres especiales en el campo 'nombres'.*

### C. Integridad de Sesión e IDOR

Se auditó la arquitectura de acceso a datos personales para prevenir referencias directas inseguras a objetos (IDOR).

**Prueba:** Uso del endpoint `/api/me` para obtener datos basados estrictamente en el contenido de la cookie cifrada.

**Resultado:** Rechazo íntegro. El backend respondió con un 400 Bad Request, validando que los datos persistidos en la base de datos MySQL son seguros y libres de scripts.

![Integridad de Sesión](main/docs/assets/session-integrity.png)
