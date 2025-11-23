
# 🚗 Proyecto Concesionaria AutoVentas

Este proyecto es una aplicación web desarrollada con Django para la gestión de una concesionaria de autos. Permite administrar el inventario de automóviles, gestionar usuarios y realizar operaciones de compra, venta y contacto.

- ✨ Características principales

## 🧑‍💻 Tecnologías utilizadas
- 🐍 Python 3
- 🕸️ Django 5
- 🗄️ SQLite3
- 🎨 Bootstrap 5
- 💻 JavaScript (ES6)
- 🖌️ CSS3
- ⚙️ HTML5
- 📋 Catálogo de automóviles con imágenes y detalles.
- 🛠️ Panel de administración para CRUD de autos.
- 👤 Registro y autenticación de usuarios personalizados.
- 📨 Formulario de contacto y mensajes.
- 📦 Inventario con exportación e impresión.
- 🎨 Interfaz moderna con Bootstrap y JS personalizado.

## 🗂️ Estructura del proyecto
```
concesionaria/
├── db.sqlite3
├── manage.py
├── requirements.txt
├── concesionaria/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── myapp_conces/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── templates/
│   └── ...
├── myapp_login/
│   ├── models.py
│   ├── views.py
│   ├── templates/
│   └── ...
├── static/
│   ├── css/
│   ├── js/
│   └── ...
```

## ⚙️ Instalación y ejecución
1. 📝 Clona el repositorio:
   ```
   git clone https://github.com/Matiaslagost7/Modulo6.Concesionaria.git
   ```
2. 📦 Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```
3. 🗄️ Realiza las migraciones:
   ```
   python manage.py migrate
   ```
4. 🚀 Ejecuta el servidor:
   ```
   python manage.py runserver
   ```

## 🔐 Usuarios y autenticación
- El sistema utiliza un modelo de usuario personalizado (`CustomUser`).
- Registro, login y logout disponibles desde la interfaz web.

## 🛡️ Panel de administración
- Acceso a través de `/admin` para usuarios con permisos.
- Gestión de automóviles y usuarios.

## 📬 Contacto y soporte
Para dudas o soporte, contacta a Matiaslagost7 vía GitHub.

---
**Desarrollado en Bootcamp II - Módulo 6** 🏫
