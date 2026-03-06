# Convertidor MP3 - YouTube a MP3 (PWA)

Esta es una Aplicación Web Progresiva (PWA) con un backend en Python que permite descargar el audio de cualquier video de YouTube en formato MP3.

Está diseñada para ejecutarse localmente en tu computadora. Puedes acceder a ella desde tu navegador web en la PC o incluso desde tu teléfono móvil si ambos dispositivos están en la misma red Wi-Fi.

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalados:

1. **Python 3.8+** (Asegúrate de marcar "Add Python to PATH" durante la instalación en Windows).
2. **FFmpeg**: `yt-dlp` requiere FFmpeg para convertir el archivo descargado a MP3.
   - **En Windows**: Descarga los binarios de FFmpeg desde [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) o usa un gestor como `winget`: `winget install "FFmpeg (Essentials)"`. Asegúrate de que `ffmpeg` esté en tu PATH.
   - **En Linux (Ubuntu/Debian)**: `sudo apt install ffmpeg`
   - **En Mac**: `brew install ffmpeg`

## Instalación

1. Clona o descarga este repositorio y abre una terminal en la carpeta `backend`.
2. Opcional pero recomendado: crea un entorno virtual de Python.
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/Mac:
   source venv/bin/activate
   ```
3. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución

1. Inicia el servidor Flask:
   ```bash
   python app.py
   ```
2. El servidor comenzará a escuchar en `http://0.0.0.0:5000`.

### Acceder desde tu PC
Abre tu navegador y entra a:
`http://localhost:5000` o `http://127.0.0.1:5000`

### Acceder desde tu Teléfono (en la misma red Wi-Fi)
1. Busca la dirección IP local de tu PC. (En Windows abre la consola y escribe `ipconfig`, busca "Dirección IPv4").
2. En el navegador de tu teléfono, ingresa esa IP seguida del puerto 5000. Por ejemplo:
`http://192.168.1.50:5000`
3. Como es una PWA, el navegador te ofrecerá "Añadir a la pantalla de inicio" (Instalar aplicación).

## Funcionamiento
- Al ingresar la URL y darle a descargar, el backend usa `yt-dlp` para descargar la mejor calidad de audio y convertirla a `.mp3`.
- El archivo modificado se guarda en la carpeta `downloads` y luego se sirve al usuario de forma automática en el navegador.
- El archivo en el servidor se programa para borrarse luego de 5 minutos, ahorrando espacio en tu disco duro.
