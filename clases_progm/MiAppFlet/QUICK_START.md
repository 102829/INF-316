# 🚀 QUICK START - Green-Ampt Pro v2.0

## ⚡ 5 Minutos para Empezar

### 1️⃣ INSTALACIÓN (1 minuto)

```bash
# Instala las dependencias
pip install -r requirements.txt
```

---

### 2️⃣ OBTENER TU IP LOCAL (1 minuto)

```bash
# Ejecuta este comando para obtener tu IP automáticamente
python get_ip.py
```

**Output esperado:**
```
🎯 IP Local Detectada    : 192.168.50.155
🔗 URL Local             : http://192.168.50.155:8001
```

---

### 3️⃣ ACTUALIZAR CONFIGURACIÓN (1 minuto)

Edita `config.py` y reemplaza:

```python
LOCAL_PC_IP = "192.168.50.155"  # ← Tu IP (del paso anterior)
NGROK_URL = "https://xxxx-xxxx-xxxx.ngrok-free.app"  # Opcional
```

---

### 4️⃣ EJECUTAR EL BACKEND (Terminal 1)

**Windows:**
```bash
start_server.bat
```

**Mac/Linux:**
```bash
chmod +x start_server.sh
./start_server.sh
```

**O manualmente:**
```bash
python main.py
```

**Verifica que ves:**
```
🚀 INICIANDO SERVIDOR GREEN-AMPT API v2.0
📍 IP Local         : 192.168.50.155
🔗 URL Local        : http://192.168.50.155:8001
```

---

### 5️⃣ EJECUTAR LA APP (Terminal 2)

**Windows:**
```bash
start_app.bat
```

**Mac/Linux:**
```bash
chmod +x start_app.sh
./start_app.sh
```

**O manualmente:**
```bash
python green_ampt_flet.py
```

**La app se abrirá automáticamente ✅**

---

## 📱 USAR LA APP

### Usuarios de Demo:
```
Usuario: david
Contraseña: 123

Usuario: daniel / elisa
Contraseña: 1234
```

### Dentro de la App:

1. **Ingresa usuario y contraseña**
2. **En el campo "IP del Servidor" ingresa:** `192.168.50.155` (tu IP)
3. **En el campo "Puerto" ingresa:** `8001`
4. **Presiona:** 🔗 **Conectar**
5. **Espera:** ✅ **Conectado a 192.168.50.155:8001**
6. **Ingresa parámetros y presiona:** 📐 **Bisección** o 📏 **Falsa Posición**

---

## 🌐 ESCENARIOS

### WiFi Local (PC y Celular misma Red)
```
✅ USA: 192.168.50.155:8001 (tu IP)
```

### WiFi Diferente
```
1. Descarga Ngrok: https://ngrok.com/download
2. Ejecuta: ngrok http 8001
3. En la app presiona: 📡 Usar Ngrok (Datos)
```

### Datos Móviles
```
1. Ejecuta: ngrok http 8001
2. En la app presiona: 📡 Usar Ngrok (Datos)
```

---

## ❌ Problemas Comunes

### "No se puede conectar"
```
✅ Solución: Verifica firewall permitiendo puerto 8001
   Windows: Control Panel → Windows Defender Firewall → Allow an app
   Mac: System Preferences → Security & Privacy → Firewall
```

### "Servidor no responde"
```
✅ Solución: 
   1. Backend corriendo? (python main.py)
   2. IP correcta? (python get_ip.py)
   3. Firewall bloqueando?
```

### "La IP no funciona"
```
✅ Solución:
   • NO USES 127.0.0.1 en otro dispositivo
   • USA la IP real (192.168.x.x)
   • O USA Ngrok para funciones cruzadas
```

---

## 📊 Componentes

| Archivo | Qué es | Ejecuta |
|---------|--------|---------|
| `main.py` | Backend API | `python main.py` |
| `green_ampt_flet.py` | App Frontend | `python green_ampt_flet.py` |
| `config.py` | Configuración | Editar manualmente |
| `get_ip.py` | Obtener IP | `python get_ip.py` |
| `users.json` | Usuarios | Se crea automáticamente |
| `requirements.txt` | Dependencias | `pip install -r requirements.txt` |

---

## ✅ Checklist

- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] IP configurada (`python get_ip.py` → edita `config.py`)
- [ ] Backend corriendo (`python main.py`)
- [ ] Frontend corriendo (`python green_ampt_flet.py`)
- [ ] App muestra login
- [ ] Ingresa usuario y contraseña
- [ ] Conecta a servidor (🔗 Conectar)
- [ ] Estado muestra ✅ Conectado

---

## 🎯 Próximo Paso

```bash
# En Terminal 1
python main.py

# En Terminal 2
python green_ampt_flet.py

# ¡Listo! 🚀
```

---

## 📖 Documentación Completa

Ver `README.md` para:
- Instalación detallada
- Configuración avanzada
- Solución de problemas
- Guías de conectividad
- FAQ

---

**¿Preguntas? 🤔**

1. Verifica los logs en la terminal del backend
2. Abre http://127.0.0.1:8001/docs para ver la API
3. Ejecuta `python get_ip.py` para verificar tu IP

**¡Disfruta Green-Ampt Pro! 🌾💧**
