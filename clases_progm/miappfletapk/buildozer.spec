[app]

# (str) Nombre de la aplicación
title = Green-Ampt Pro

# (str) Identificador del paquete
package.name = greenampt

# (str) Dominio del paquete
package.domain = org.greenampt

# (source.dir) Directorio fuente
source.dir = .

# (source.include_exts) Extensiones de archivo a incluir
source.include_exts = py,png,jpg,json

# (source.exclude_exts) Extensiones a excluir
source.exclude_exts = spec

# (version) Versión de la app
version = 2.0.0

# (str) Logo y splash (OPCIONAL - comenta si no tienes archivos)
# presplash.filename = %(source.dir)s/logo.png
# icon.filename = %(source.dir)s/icon.png

# (string) Requisitos Python
requirements = python3,flet==0.21.0,httpx==0.25.2

# (list) Permisos de Android - CRÍTICO para conectar a servidores
android.permissions = INTERNET,ACCESS_NETWORK_STATE,CHANGE_NETWORK_STATE

# (list) Características de Android necesarias
android.features = android.hardware.internet

# (int) API de destino de Android
android.api = 31

# (int) API mínimo de Android (para dispositivos más antiguos)
android.minapi = 21

# (str) Versión de NDK
android.ndk = 25b

# (list) Arquitecturas soportadas
# arm64-v8a: Dispositivos modernos (Redmi 13C)
# armeabi-v7a: Dispositivos más antiguos (retrocompatibilidad)
android.archs = arm64-v8a,armeabi-v7a

# (bool) Orientación - portrait para celular
orientation = portrait

# (bool) Pantalla completa (recomendado para apps)
fullscreen = 0

# (string) Descripción
description = Sistema de Infiltración Green-Ampt con métodos numéricos

# (bool) Copiar archivos de biblioteca
android.copy_libs = 1

# (bool) Usar compresión de archivos
android.release_artifact = apk

# (list) Patrones de archivos que NO se incluirán
android.gradle_dependencies = 

# (str) Versión de Gradle
android.gradle_version = 7.3.1

[buildozer]

# (int) Nivel de log (0 = error, 1 = info, 2 = debug)
log_level = 2

# (int) Mostrar advertencia si se ejecuta como root
warn_on_root = 1

# (str) Ruta al compilador Android NDK (normalmente auto-detectado)
# android.ndk_path = /path/to/android-ndk

# (bool) Usar símbolo de depuración (debug)
android.strip_debug = 1

# (bool) Usar Google Play Store
android.store = 1

# (str) Bootstrap para Android
p4a.bootstrap = sdl2

# (int) Puerto para servidor adb
android.port = 5037

# (bool) Aceptar licencias del SDK automáticamente
android.accept_sdk_license = True

# ════════════════════════════════════════════════════════════════════
# IMPORTANTE PARA ANDROID
# ════════════════════════════════════════════════════════════════════
# 
# Este archivo está optimizado para:
# • Redmi 13C (ARM64)
# • Conexiones HTTP a servidores locales
# • Flet 0.21.0 + httpx 0.25.2
#
# Permisos habilitados:
# ✅ INTERNET: Para conectar al servidor
# ✅ ACCESS_NETWORK_STATE: Para detectar WiFi
# ✅ CHANGE_NETWORK_STATE: Para cambiar de red
#
# ════════════════════════════════════════════════════════════════════
