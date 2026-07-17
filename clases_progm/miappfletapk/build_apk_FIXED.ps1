# Green-Ampt Pro - Script Compilación APK MEJORADO
# Ejecutar como Administrador en PowerShell
# Uso: .\build_apk_FIXED.ps1

Write-Host "`n" -ForegroundColor White
Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║       🚀 COMPILADOR APK - Green-Ampt Pro v2.0           ║" -ForegroundColor Cyan
Write-Host "║           VERSIÓN CORREGIDA PARA REDMI 13C              ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host "`n"

# ═══════════════════════════════════════════════════════════════════
#  VERIFICAR REQUISITOS
# ═══════════════════════════════════════════════════════════════════

Write-Host "📋 Verificando requisitos..." -ForegroundColor Yellow
Write-Host "`n"

$requisitosOK = $true

# 1. Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✅ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Python NO ENCONTRADO" -ForegroundColor Red
    Write-Host "     Descargalo: https://www.python.org" -ForegroundColor Gray
    $requisitosOK = $false
}

# 2. Java JDK
try {
    $javaVersion = java -version 2>&1
    Write-Host "  ✅ Java JDK: Instalado" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Java JDK NO ENCONTRADO" -ForegroundColor Red
    Write-Host "     Descargalo: https://www.oracle.com/java/technologies/downloads/" -ForegroundColor Gray
    $requisitosOK = $false
}

# 3. Android SDK
if ($env:ANDROID_HOME) {
    Write-Host "  ✅ Android SDK: $env:ANDROID_HOME" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  Android SDK NO CONFIGURADO" -ForegroundColor Yellow
    Write-Host "     Instala Android Studio: https://developer.android.com/studio" -ForegroundColor Gray
    # No es fatal, buildozer puede descargarlo
}

Write-Host "`n"

if (-not $requisitosOK) {
    Write-Host "❌ Faltan requisitos. Instálalos primero." -ForegroundColor Red
    exit
}

# ═══════════════════════════════════════════════════════════════════
#  INSTALAR DEPENDENCIAS
# ═══════════════════════════════════════════════════════════════════

Write-Host "📦 Instalando herramientas de compilación..." -ForegroundColor Yellow
Write-Host "   (Esto puede tardar unos minutos la primera vez)" -ForegroundColor Gray
Write-Host "`n"

pip install --upgrade buildozer cython python-for-android wheel setuptools 2>&1 | Out-Null

Write-Host "  ✅ Herramientas instaladas" -ForegroundColor Green
Write-Host "`n"

# ═══════════════════════════════════════════════════════════════════
#  VERIFICAR ESTRUCTURA DE PROYECTO
# ═══════════════════════════════════════════════════════════════════

Write-Host "🔍 Verificando estructura de proyecto..." -ForegroundColor Yellow
Write-Host "`n"

$archivosNecesarios = @(
    @{"nombre" = "green_ampt_flet_APK_FIXED.py"; "nuevo" = $true},
    @{"nombre" = "buildozer_FIXED.spec"; "nuevo" = $true},
    @{"nombre" = "requirements_APK.txt"; "nuevo" = $false},
    @{"nombre" = "main.py"; "nuevo" = $false}
)

$archivosOK = $true
foreach ($archivo in $archivosNecesarios) {
    if (Test-Path $archivo.nombre) {
        if ($archivo.nuevo) {
            Write-Host "  ✅ $($archivo.nombre) (NUEVO - CORREGIDO)" -ForegroundColor Green
        } else {
            Write-Host "  ✅ $($archivo.nombre)" -ForegroundColor Green
        }
    } else {
        Write-Host "  ❌ $($archivo.nombre) - FALTA" -ForegroundColor Red
        $archivosOK = $false
    }
}

Write-Host "`n"

if (-not $archivosOK) {
    Write-Host "❌ Faltan archivos. Verifica que copiaste todos los archivos." -ForegroundColor Red
    exit
}

# ═══════════════════════════════════════════════════════════════════
#  PREPARAR buildozer.spec
# ═══════════════════════════════════════════════════════════════════

Write-Host "⚙️  Preparando configuración..." -ForegroundColor Yellow
Write-Host "`n"

# Copiar buildozer_FIXED.spec a buildozer.spec
if (Test-Path "buildozer_FIXED.spec") {
    Copy-Item -Path "buildozer_FIXED.spec" -Destination "buildozer.spec" -Force
    Write-Host "  ✅ Configuración preparada (buildozer.spec)" -ForegroundColor Green
}

# Copiar main.py (frontend APK) a buildozer
if (Test-Path "green_ampt_flet_APK_FIXED.py") {
    Copy-Item -Path "green_ampt_flet_APK_FIXED.py" -Destination "main.py.bak" -Force
    Write-Host "  ℹ️  Respaldo de frontend: main.py.bak" -ForegroundColor Cyan
}

Write-Host "`n"

# ═══════════════════════════════════════════════════════════════════
#  MENÚ DE OPCIONES
# ═══════════════════════════════════════════════════════════════════

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  SELECCIONA TIPO DE COMPILACIÓN" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "`n"
Write-Host "  1️⃣  Debug APK (para pruebas - rápido)" -ForegroundColor White
Write-Host "       ✅ Recomendado para Redmi 13C" -ForegroundColor Green
Write-Host "       Tiempo: 10-20 minutos" -ForegroundColor Gray
Write-Host "`n"
Write-Host "  2️⃣  Release APK (para Google Play - requiere firma)" -ForegroundColor White
Write-Host "       ⚠️  Más lento, para distribución oficial" -ForegroundColor Yellow
Write-Host "       Tiempo: 15-25 minutos" -ForegroundColor Gray
Write-Host "`n"
Write-Host "  3️⃣  Limpiar y compilar Debug (si hay errores)" -ForegroundColor White
Write-Host "       Tiempo: 20-30 minutos" -ForegroundColor Gray
Write-Host "`n"

$choice = Read-Host "Ingresa opción (1-3)"

switch ($choice) {
    "1" {
        $buildType = "debug"
        Write-Host "`n🔨 Compilando Debug APK..." -ForegroundColor Yellow
    }
    "2" {
        $buildType = "release"
        Write-Host "`n🔨 Compilando Release APK..." -ForegroundColor Yellow
    }
    "3" {
        Write-Host "`n🧹 Limpiando compilaciones anteriores..." -ForegroundColor Yellow
        buildozer android clean 2>&1 | Out-Null
        Write-Host "✅ Limpieza completada" -ForegroundColor Green
        $buildType = "debug"
        Write-Host "`n🔨 Compilando Debug APK..." -ForegroundColor Yellow
    }
    default {
        Write-Host "❌ Opción inválida" -ForegroundColor Red
        exit
    }
}

Write-Host "`n"
Write-Host "⏳ Compilando... Esto puede tardar 10-30 minutos" -ForegroundColor Yellow
Write-Host "   (Descargando dependencias, compilando, etc.)" -ForegroundColor Gray
Write-Host "`n"
Write-Host "─────────────────────────────────────────────────────────" -ForegroundColor Gray

# ═══════════════════════════════════════════════════════════════════
#  EJECUTAR COMPILACIÓN
# ═══════════════════════════════════════════════════════════════════

if ($buildType -eq "debug") {
    buildozer android debug
} else {
    buildozer android release
}

Write-Host "─────────────────────────────────────────────────────────" -ForegroundColor Gray

# ═══════════════════════════════════════════════════════════════════
#  VERIFICAR RESULTADO
# ═══════════════════════════════════════════════════════════════════

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n"
    Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║          ✅ ¡COMPILACIÓN EXITOSA!                        ║" -ForegroundColor Green
    Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host "`n"
    
    Write-Host "📱 Tu APK está listo:" -ForegroundColor Cyan
    Write-Host "`n"
    
    if ($buildType -eq "debug") {
        $apkPath = "bin\greenampt-2.0.0-debug.apk"
        
        Write-Host "  📂 Ubicación: $apkPath" -ForegroundColor White
        Write-Host "  📊 Tamaño: $(if (Test-Path $apkPath) { [math]::Round((Get-Item $apkPath).length / 1MB, 1) }MB)" -ForegroundColor Gray
        
        Write-Host "`n"
        Write-Host "─────────────────────────────────────────────────────────" -ForegroundColor Gray
        Write-Host "  📲 PRÓXIMOS PASOS PARA INSTALAR EN REDMI 13C:" -ForegroundColor Cyan
        Write-Host "─────────────────────────────────────────────────────────" -ForegroundColor Gray
        Write-Host "`n"
        
        Write-Host "  OPCIÓN A - Instalación por Cable USB (recomendado):" -ForegroundColor Yellow
        Write-Host "  ─────────────────────────────────────────────────────" -ForegroundColor Gray
        Write-Host "  1. Conecta Redmi 13C por USB" -ForegroundColor White
        Write-Host "  2. Activa Depuración USB en el celular:" -ForegroundColor White
        Write-Host "     Settings > Acerca de > Versión MIUI (toca 7 veces)" -ForegroundColor Gray
        Write-Host "     Settings > Sistema > Opciones desarrollador > Depuración USB" -ForegroundColor Gray
        Write-Host "  3. Ejecuta en PowerShell:" -ForegroundColor White
        Write-Host "     adb install $apkPath" -ForegroundColor Cyan
        Write-Host "`n"
        
        Write-Host "  OPCIÓN B - Transferencia Manual:" -ForegroundColor Yellow
        Write-Host "  ───────────────────────────────" -ForegroundColor Gray
        Write-Host "  1. Copia el archivo: $apkPath" -ForegroundColor White
        Write-Host "  2. Pégalo en Google Drive, Email o Telegram" -ForegroundColor White
        Write-Host "  3. Descargalo en tu Redmi 13C" -ForegroundColor White
        Write-Host "  4. Abre el archivo desde el explorador" -ForegroundColor White
        Write-Host "  5. Presiona Instalar" -ForegroundColor White
        Write-Host "`n"
        
        Write-Host "─────────────────────────────────────────────────────────" -ForegroundColor Gray
        Write-Host "  🚀 PARA USAR LA APP:" -ForegroundColor Cyan
        Write-Host "─────────────────────────────────────────────────────────" -ForegroundColor Gray
        Write-Host "`n"
        Write-Host "  EN TU PC:" -ForegroundColor Yellow
        Write-Host "  1. Abre Command Prompt en esta carpeta" -ForegroundColor White
        Write-Host "  2. Ejecuta: python main.py" -ForegroundColor Cyan
        Write-Host "  3. Anota la IP que muestra (ej: 192.168.1.100)" -ForegroundColor White
        Write-Host "`n"
        
        Write-Host "  EN TU REDMI 13C:" -ForegroundColor Yellow
        Write-Host "  1. Abre Green-Ampt Pro" -ForegroundColor White
        Write-Host "  2. Usuario: david  |  Contraseña: 123" -ForegroundColor Cyan
        Write-Host "  3. IP: (la que anotaste, ej: 192.168.1.100)" -ForegroundColor Cyan
        Write-Host "  4. Puerto: 8001" -ForegroundColor Cyan
        Write-Host "  5. Presiona: 🔗 Conectar" -ForegroundColor White
        Write-Host "  6. Si dice '✅ Conectado' → ¡LISTO!" -ForegroundColor Green
        Write-Host "`n"
        
    } else {
        Write-Host "  📂 Ubicación: bin\greenampt-2.0.0-release.apk" -ForegroundColor White
        Write-Host "  ✅ Lista para subir a Google Play Store" -ForegroundColor Green
    }
    
    Write-Host "`n"
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
    Write-Host "  ¿Problemas? Lee: GUIA_SETUP_REDMI_13C.txt" -ForegroundColor Cyan
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
    Write-Host "`n"
    
} else {
    Write-Host "`n"
    Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Red
    Write-Host "║            ❌ LA COMPILACIÓN FALLÓ                       ║" -ForegroundColor Red
    Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Red
    Write-Host "`n"
    
    Write-Host "🔍 POSIBLES SOLUCIONES:" -ForegroundColor Yellow
    Write-Host "`n"
    Write-Host "  1️⃣  Verifica requisitos (Java, Android SDK):" -ForegroundColor White
    Write-Host "     java -version" -ForegroundColor Gray
    Write-Host "`n"
    Write-Host "  2️⃣  Intenta limpiar y compilar:" -ForegroundColor White
    Write-Host "     buildozer android clean" -ForegroundColor Gray
    Write-Host "     buildozer android debug" -ForegroundColor Gray
    Write-Host "`n"
    Write-Host "  3️⃣  Actualiza buildozer:" -ForegroundColor White
    Write-Host "     pip install --upgrade buildozer cython" -ForegroundColor Gray
    Write-Host "`n"
    Write-Host "  4️⃣  Revisa los logs:" -ForegroundColor White
    Write-Host "     buildozer android debug -v" -ForegroundColor Gray
    Write-Host "`n"
    
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Red
    Write-Host "  ¿Sigue sin funcionar? Lee: GUIA_SETUP_REDMI_13C.txt" -ForegroundColor Yellow
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Red
    Write-Host "`n"
}

Write-Host "`n"
