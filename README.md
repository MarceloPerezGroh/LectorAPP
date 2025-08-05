# LectorAPP

**LectorAPP** es una aplicación desarrollada para convertir texto a audio, mostrar archivos PDF o TXT, y controlar la lectura mediante botones de pausa, lectura y detención. Su diseño está enfocado en la simplicidad y la accesibilidad.

## 🖼️ Interfaz

Imagen de la interfaz de LectorAPP:

<p align="center">
  <img src="El Lector - Interface.jpg" alt="Imagen de la interfaz de LectorAPP" width="700">
</p>
## 📖 Ejemplo en uso
A continuación, se muestra cómo luce la aplicación en funcionamiento, cargando un archivo PDF con contenido textual.
Esta vista permite al usuario visualizar el contenido del documento mientras utiliza los controles superiores para convertir a audio, leer la selección, pausar, detener la lectura o cambiar el tamaño del texto.

<p align="center"> <img src="img lectorAPP 2.jpg" alt="Vista de la app en funcionamiento" width="700"> </p>
## 🔧 Funcionalidades

- Convertir texto a audio
- Mostrar contenido de archivos PDF o TXT
- Leer selección de texto
- Pausar, detener y ajustar la lectura

## 📁 Estructura del Proyecto

- `main.py`: archivo principal de la aplicación
- `assets/`: carpeta para imágenes y recursos
- `README.md`: este archivo

## 🚀 Requisitos

- Python 3.9 o superior
- Librerías: `tkinter`, `pyttsx3`, `PyPDF2` (u otras que uses)

## 📦 Instalación

```bash
git clone https://github.com/tuusuario/lectorapp.git
cd lectorapp
pip install -r requirements.txt
python main.py
