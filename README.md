# Aplicación de Gestión de Productos y Órdenes

Una aplicación web desarrollada con Streamlit para la gestión de productos y órdenes desde la API de Jumpseller.

## 📋 Descripción

Esta aplicación permite:
- Conectar con la API de Jumpseller
- Crear y gestionar una base de datos SQLite local
- Cargar productos y órdenes desde la API
- Visualizar los datos en tablas interactivas
- Consultar información de diferentes entidades

## 🛠️ Tecnologías Utilizadas

- **Python 3.12**
- **Streamlit** - Framework para la interfaz web
- **SQLite** - Base de datos local
- **Pandas** - Manipulación de datos
- **Requests** - Llamadas a la API

## 📊 Modelo de Base de Datos

El sistema maneja las siguientes entidades principales:

### Módulo de Productos
- **Products**: Información principal de productos
- **Categories**: Categorías de productos
- **Images**: Imágenes de productos
- **Variants**: Variantes de productos (diferentes precios, stock, etc.)
- **Options**: Opciones específicas de cada variante

### Módulo de Órdenes  
- **Orders**: Información principal de órdenes
- **Customers**: Datos de clientes
- **ShippingAddresses**: Direcciones de envío
- **BillingAddresses**: Direcciones de facturación
- **OrderProducts**: Productos incluidos en cada orden

### 🔗 Diagrama Entidad-Relación (MER)

Puedes ver el diagrama completo del modelo de datos aquí:
**[Ver Diagrama MER en dbdiagram.io](https://dbdiagram.io/d/685b59a0f413ba3508b88477))**

![Diagrama MER](docs/database-diagram.png)

## 🚀 Instalación y Uso

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/rorocabezas/Datascience--Lili.git
cd TU_REPOSITORIO
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecuta la aplicación:
```bash
streamlit run app.py
```

4. Abre tu navegador en `http://localhost:8501`

## 📱 Uso de la Aplicación

1. **Crear Base de Datos**: Haz clic en "Crear Base de Datos" para inicializar las tablas
2. **Cargar Productos**: Carga los productos disponibles desde la API de Jumpseller
3. **Cargar Órdenes**: Carga las órdenes pagadas desde la API
4. **Consultar Datos**: Selecciona una tabla y visualiza los datos cargados

## 📁 Estructura del Proyecto

```
├── app.py                 # Aplicación principal de Streamlit
├── requirements.txt       # Dependencias del proyecto
├── README.md             # Este archivo
├── docs/                 # Documentación
│   └── database-diagram.png
├── data.db               # Base de datos SQLite (se crea automáticamente)
└── .gitignore           # Archivos ignorados por Git
```

## 🔧 Configuración de la API

La aplicación está configurada para conectarse a la API de Jumpseller. Las credenciales están incluidas en el código para fines de demostración.

**Endpoints utilizados:**
- Productos: `https://api.jumpseller.com/v1/products/status/available.json`
- Órdenes: `https://api.jumpseller.com/v1/orders/status/paid.json`

## 📈 Funcionalidades

- ✅ Creación automática de base de datos SQLite
- ✅ Carga de productos desde API
- ✅ Carga de órdenes desde API  
- ✅ Visualización de datos en tablas
- ✅ Relaciones entre entidades
- ✅ Manejo de errores en las API calls

## 🤝 Contribución

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📝 Notas Técnicas

- La base de datos se crea automáticamente en `data.db`
- Se utiliza `INSERT OR IGNORE` para evitar duplicados
- Las relaciones entre tablas están definidas mediante foreign keys
- La aplicación maneja errores de conexión a la API

## 👥 Equipo de Desarrollo

- **Tu Nombre** - Desarrollador Principal

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.
