# 🌾 Green-Ampt Pro v2.0 - Guía Completa

## 📋 Contenido
1. [Instalación](#instalación)
2. [Configuración](#configuración)
3. [Ejecución](#ejecución)
4. [Escenarios de Conectividad](#escenarios-de-conectividad)
5. [Solución de Problemas](#solución-de-problemas)

---

## 🚀 Instalación

### Requisitos
```bash
Python 3.8+
pip install fastapi uvicorn pydantic httpx flet
```

### Pasos

1. **Descarga todos los archivos:**
   ```
   config.py
   main.py (Backend)
   green_ampt_flet.py (Frontend)
   users.json (usuarios)
   ```

2. **Instala las dependencias:**
   ```bash
   pip install fastapi uvicorn pydantic httpx flet
   ```

---

## ⚙️ Configuración

### Paso 1: Obtén tu IP Local

#### 📍 En Windows:
```bash
ipconfig
```
Busca **"IPv4 Address"** - algo como `192.168.50.155`

#### 📍 En Mac/Linux:
```bash
hostname -I
```
O:
```bash
ifconfig
```

### Paso 2: Edita `config.py`

```python
LOCAL_PC_IP = "192.168.50.155"  # ← Tu IP real
NGROK_URL = "https://xxxx-xxxx-xxxx.ngrok-free.app"  # ← Opcional
PORT = 8001
ENVIRONMENT = "device"
```

---

## 🎯 Ejecución

### Terminal 1: Backend (Servidor)

```bash
python main.py
```

**Output esperado:**
```
╔══════════════════════════════════════════════════════════════════════╗
║  🚀 INICIANDO SERVIDOR GREEN-AMPT API v2.0                          ║
╠══════════════════════════════════════════════════════════════════════╣
║  📍 IP Local         : 192.168.50.155                               ║
║  🔗 URL Local        : http://192.168.50.155:8001                   ║
║  🌐 URL Docs         : http://127.0.0.1:8001/docs                   ║
║  💊 Health Check     : http://127.0.0.1:8001/health                 ║
╚══════════════════════════════════════════════════════════════════════╝
```

### Terminal 2: Frontend (App)

```bash
python green_ampt_flet.py
```

**La app se abrirá automáticamente**

---

## 🌐 Escenarios de Conectividad

### Escenario 1: WiFi Local (Misma Red)

**Situación:** PC y celular en la misma WiFi

**Pasos:**
1. Inicia el backend en tu PC: `python main.py`
2. Abre la app en tu celular: `python green_ampt_flet.py` (si es en emulador)
3. En la app, en el campo **IP del Servidor**, ingresa: `192.168.50.155`
4. En el campo **Puerto**, ingresa: `8001`
5. Presiona **🔗 Conectar**

**Resultado esperado:**
```
✅ Conectado a 192.168.50.155:8001
```

---

### Escenario 2: WiFi Diferente

**Situación:** PC y celular en WiFis diferentes pero con acceso a internet

**Pasos:**

#### Opción A: Via Ngrok (Recomendado)

1. **Descarga Ngrok:**
   - Ve a https://ngrok.com/download
   - Descarga la versión para tu OS

2. **Inicia Ngrok:**
   ```bash
   ngrok http 8001
   ```
   
   **Output:**
   ```
   ngrok by @inconshreveable
   Session Status    online
   Account           (Plan: Free)
   Version           3.3.0
   Region            us (United States)
   Latency           34ms
   Web Interface     http://127.0.0.1:4040
   Forwarding        https://abc12-xyz.ngrok-free.app -> http://localhost:8001
   ```

3. **Copia la URL:** `https://abc12-xyz.ngrok-free.app`

4. **En la app:**
   - Presiona el botón **📡 Usar Ngrok (Datos)**
   - O ingresa manualmente la URL en el campo IP

5. **Presiona 🔗 Conectar**

#### Opción B: IP Pública (Si disponible)

Si tu PC tiene IP pública:
1. Obtén tu IP pública: https://www.cuál-es-mi-ip.com
2. Ingresa en la app como en WiFi local

---

### Escenario 3: Datos Móviles

**Situación:** Celular con datos móviles (sin WiFi)

**Pasos:**

1. **Inicia Ngrok en tu PC:**
   ```bash
   ngrok http 8001
   ```

2. **Copia la URL de Ngrok**

3. **En la app (en el celular):**
   - Presiona **📡 Usar Ngrok (Datos)**
   - O ingresa manualmente la URL de Ngrok

4. **Presiona 🔗 Conectar**

---

## 🔧 Solución de Problemas

### ❌ "No se puede conectar"

**Solución 1: Verifica el firewall**
```bash
# Windows: Desactiva el firewall temporalmente o añade excepciones
# Mac: Sistema → Seguridad y privacidad → Firewall
# Linux: sudo ufw allow 8001
```

**Solución 2: Verifica la IP**
```bash
# La IP debe ser de tu RED LOCAL
# Correctas: 192.168.x.x, 10.0.x.x
# Incorrectas: 127.0.0.1 (solo local)
```

**Solución 3: Prueba la conexión**
```bash
# Desde la app o navegador
# http://192.168.50.155:8001/health
# Deberías ver: {"✅ status": "ok"}
```

---

### 🟡 "Servidor no responde"

**Solución 1: Verifica que el backend está corriendo**
```bash
python main.py
```

**Solución 2: Verifica el puerto**
- Asegúrate de que el puerto `8001` esté libre
- En Windows: `netstat -ano | findstr :8001`
- En Mac/Linux: `lsof -i :8001`

**Solución 3: Prueba localhost primero**
- Ingresa `127.0.0.1` como IP (solo en la misma máquina)

---

### 📡 "Ngrok dice 'command not found'"

**Solución:**
1. Descarga Ngrok: https://ngrok.com/download
2. Extrae el archivo
3. Abre Terminal/CMD en esa carpeta
4. Ejecuta: `ngrok http 8001`

---

### 🔌 "No puedo cambiar la IP desde la app"

**Solución:**
1. Asegúrate de que los campos no están deshabilitados
2. Presiona **🔗 Conectar** después de cambiar la IP
3. Espera el mensaje de estado (✅ o ❌)

---

## 📱 Usuarios de Demo

```
Usuario: david
Contraseña: 123

Usuario: daniel
Contraseña: 1234

Usuario: elisa
Contraseña: 1234
```

---

## 🎯 Flujo de Uso Típico

```
1. Terminal 1 - Inicia Backend
   └─ python main.py

2. Terminal 2 - Inicia Frontend
   └─ python green_ampt_flet.py

3. En la App:
   ├─ Ingresa usuario y contraseña
   ├─ Cambia IP y Puerto si es necesario
   ├─ Presiona 🔗 Conectar
   ├─ Ingresa parámetros
   ├─ Presiona 📐 Bisección o 📏 Falsa Posición
   └─ ✅ Ve los resultados

4. Cambiar conexión:
   ├─ Modifica IP o Puerto
   ├─ Presiona 🔗 Conectar de nuevo
   └─ La app reconecta automáticamente
```

---

## 📊 Arquitectura

```
┌─────────────────────────────────────────────────────┐
│         DISPOSITIVO DEL USUARIO (Celular)          │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │  green_ampt_flet.py (Frontend)               │  │
│  │  • UI moderna                                 │  │
│  │  • Cambio dinámico de IP/Puerto              │  │
│  │  • Autenticación                             │  │
│  │  • Visualización de resultados               │  │
│  └───────────────────┬──────────────────────────┘  │
│                      │ httpx.post()                 │
│                      │                              │
│                      ▼                              │
│      ┌──────────────────────────┐                  │
│      │ http://IP:PUERTO/        │                  │
│      │ • WiFi Local             │                  │
│      │ • WiFi Diferente (Ngrok) │                  │
│      │ • Datos Móviles (Ngrok)  │                  │
│      └──────────────────────────┘                  │
└─────────────────────────────────────────────────────┘
                      │
                      │ (Internet/Red)
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│           SERVIDOR (Tu PC/Laptop)                   │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │  main.py (Backend FastAPI)                   │  │
│  │  • Host: 0.0.0.0 (escucha todas interfaces) │  │
│  │  • Puerto: 8001                              │  │
│  │  • Métodos: Bisección, Falsa Posición       │  │
│  │  • CORS habilitado para cualquier origen    │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │  config.py                                   │  │
│  │  • Configuración centralizada                │  │
│  │  • IP Local, Ngrok, Puerto                   │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## ✅ Checklist Antes de Usar

- [ ] Python 3.8+ instalado
- [ ] Dependencias instaladas (`pip install fastapi uvicorn pydantic httpx flet`)
- [ ] IP local configurada en `config.py`
- [ ] Puerto `8001` disponible
- [ ] Backend iniciado (`python main.py`)
- [ ] Frontend iniciado (`python green_ampt_flet.py`)
- [ ] IP/Puerto correctos en la app
- [ ] Conectividad verificada (✅ estado verde)
- [ ] Firewall permite conexiones en puerto `8001`

---

## 🆘 Soporte

Si tienes problemas:

1. **Verifica los logs del backend** - Muestra errores detallados
2. **Prueba con `http://127.0.0.1:8001/health`** - Desde navegador
3. **Comprueba la conexión a internet** - Si usas Ngrok
4. **Reinicia ambas terminales** - A veces resuelve problemas de conexión

---

## 📞 Contacto

¿Problemas? Verifica:
- IP local correcta
- Puerto disponible
- Firewall deshabilitado/permitiendo puerto 8001
- Ambas terminales (Backend y Frontend) corriendo

---

**¡Listo para usar! 🚀**
