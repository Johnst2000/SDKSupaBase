# Emulator "device offline" / black screen al ejecutar

## Si Android Studio muestra `emulator-5554 offline`

Eso es un problema de **ADB/emulador**, no del código Kotlin. La app no se instala o no arranca bien.

1. Cierra el emulador y Android Studio (opcional).
2. En una terminal:

```bat
adb kill-server
adb start-server
adb devices
```

Debe aparecer `emulator-5554   device` (no `offline`).

3. En **Device Manager**: menú del AVD → **Cold Boot Now** (o borra datos del AVD y vuelve a iniciar).
4. Vuelve a **Run** en el proyecto.

## Si el emulador es muy antiguo

`minSdk` del proyecto es **26** (Android 8+). Usa un AVD con API 26 o superior (recomendado API 34).

## Ver crash en logcat (cuando el dispositivo está `device`)

```bat
adb logcat -c
adb logcat *:E | findstr /i "uteq AndroidRuntime FATAL"
```

Luego abre la app y revisa `FATAL EXCEPTION`.

## Paquete de la app

- **applicationId / namespace:** `com.uteq.software.app`
- **Launcher:** `MainActivity` (lista de alumnos)
- No debe existir la carpeta `com/example/sdksupabase` en `app/src/main/java` (paquete viejo eliminado).
