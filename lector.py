import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import fitz  # PyMuPDF
from gtts import gTTS  # Google Text-to-Speech
import pygame  # Para reproducir audio dentro de la app
import os
import sys

# Inicializar pygame para reproducir audio
pygame.mixer.init()

audio_reproduciendo = False  # Variable global para el estado del audio

# Configuración de la ventana
ctk.set_appearance_mode("dark")  # Modo oscuro
ctk.set_default_color_theme("dark-blue")  # Tema oscuro azul
ventana = ctk.CTk()  # Crear la ventana principal
ventana.title("ElLector")
ventana.geometry("1000x600")  # Tamaño predeterminado
ventana.resizable(True, True)  # Permite redimensionar la ventana

# Establecer el color de fondo y la transparencia de la ventana
ventana.configure(bg="#1E1E1E")  # Fondo oscuro para la ventana
ventana.attributes("-alpha", 0.99)  # Mantener la transparencia en toda la ventana

# Crear el área de texto con un fondo sólido (sin transparencia)
texto_capitulo = ctk.CTkTextbox(ventana, font=("Helvetica", 14), wrap="word", height=30, fg_color="#2E2E2E")  # Fondo sólido para el área de texto
texto_capitulo.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Configurar para que el área de texto ocupe todo el espacio disponible
ventana.grid_rowconfigure(1, weight=1)  # Hacer que la fila del área de texto sea flexible
ventana.grid_columnconfigure(0, weight=1)  # Hacer que la columna del área de texto sea flexible


# Variables para la geometría de la ventana
pos_x = 100
pos_y = 100

def mover_ventana(event):
    ventana.geometry(f'+{event.x_root - 50}+{event.y_root - 10}')  # Ajustamos la posición relativa

ventana.bind("<B1-Motion>", mover_ventana)

# Crear la variable de lectura lenta después de la inicialización de la ventana
lectura_lenta = ctk.BooleanVar(value=False)  # Velocidad de lectura

# Crear un Frame para los botones
frame_botones = ctk.CTkFrame(ventana, fg_color="#1E1E1E")
frame_botones.grid(row=0, column=0, pady=10, padx=10, columnspan=3)

# --- Crear botones personalizados de la ventana ---
def cerrar():
    ventana.destroy()

def minimizar():
    ventana.iconify()  # Minimiza la ventana

# --- Crear el área de texto ---
texto_capitulo = ctk.CTkTextbox(ventana, font=("Helvetica", 14), wrap="word", height=30, fg_color="#1E1E1E")
texto_capitulo.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")


# Configurar para que el área de texto ocupe todo el espacio disponible
ventana.grid_rowconfigure(1, weight=1)  # Hacer que la fila del área de texto sea flexible
ventana.grid_columnconfigure(0, weight=1)  # Hacer que la columna del área de texto sea flexible

# --- Funciones de la aplicación ---

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # Para aplicaciones empaquetadas con PyInstaller
    except Exception:
        base_path = os.path.abspath(".")  # Si no está empaquetada, usamos el directorio actual
    return os.path.join(base_path, relative_path)

# Función: Convertir PDF o TXT a Audio
def convertir_a_audio():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos PDF y TXT", "*.pdf;*.txt")])
    if not archivo:
        return

    # Leer texto dependiendo del tipo de archivo
    if archivo.endswith(".pdf"):
        texto = leer_texto_pdf(archivo)
    elif archivo.endswith(".txt"):
        texto = leer_texto_txt(archivo)
    
    if texto.strip():
        archivo_salida = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("Archivo MP3", "*.mp3")])
        if archivo_salida:
            tts = gTTS(texto, lang='es', slow=lectura_lenta.get())
            tts.save(archivo_salida)
            messagebox.showinfo("Éxito", f"Audio guardado en: {archivo_salida}")
    else:
        messagebox.showerror("Error", "El archivo no contiene texto legible.")

# Función: Leer texto de un PDF
def leer_texto_pdf(ruta_pdf):
    texto = ""
    try:
        pdf = fitz.open(ruta_pdf)
        for pagina in pdf:
            texto += pagina.get_text()
        pdf.close()
    except Exception as e:
        print(f"Error al leer el PDF: {e}")
    return texto

# Función: Leer texto de un archivo TXT
def leer_texto_txt(ruta_txt):
    texto = ""
    try:
        with open(ruta_txt, "r", encoding="utf-8") as file:
            texto = file.read()
    except Exception as e:
        print(f"Error al leer el archivo TXT: {e}")
    return texto

# Función: Mostrar PDF o TXT en la interfaz
def mostrar_pdf():
    limpiar_texto()
    archivo = filedialog.askopenfilename(filetypes=[("Archivos PDF y TXT", "*.pdf;*.txt")])
    if not archivo:
        return

    # Leer el archivo y mostrar el texto
    if archivo.endswith(".pdf"):
        texto = leer_texto_pdf(archivo)
    elif archivo.endswith(".txt"):
        texto = leer_texto_txt(archivo)
    
    if texto.strip():
        texto_capitulo.insert("0.0", texto)
    else:
        messagebox.showerror("Error", "El archivo no contiene texto legible.")

def leer_en_voz_alta():
    global audio_reproduciendo

    # Detener y liberar recursos si ya hay audio en reproducción
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

    # Verificar si hay un archivo temporal previo y eliminarlo
    if os.path.exists("temp_audio.mp3"):
        try:
            pygame.mixer.quit()  # Liberar cualquier recurso asociado
            pygame.mixer.init()  # Reiniciar el mixer
            os.remove("temp_audio.mp3")
        except Exception as e:
            print(f"Error al eliminar el archivo temporal: {e}")
            messagebox.showerror("Error", "No se pudo eliminar el archivo temporal anterior.")
            return

    texto_seleccionado = texto_capitulo.get("sel.first", "sel.last")  # Obtener el texto seleccionado
    if texto_seleccionado.strip():  # Verificar que no esté vacío
        tts = gTTS(texto_seleccionado, lang='es', slow=lectura_lenta.get())  # Usamos el valor de lectura_lenta
        tts.save("temp_audio.mp3")
        pygame.mixer.music.load("temp_audio.mp3")
        pygame.mixer.music.play()  # Reproducir el audio dentro de la app
        audio_reproduciendo = True
    else:
        messagebox.showwarning("Aviso", "No has seleccionado texto para leer.")

# Función: Pausar o reanudar la lectura
def pausar_lectura():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        btn_pausar.configure(text="Reanudar")
    else:
        pygame.mixer.music.unpause()
        btn_pausar.configure(text="Pausar")

# Función: Detener la lectura
def detener_lectura():
    pygame.mixer.music.stop()
    btn_pausar.configure(text="Pausar")

# Función: Limpiar contenido del texto
def limpiar_texto():
    texto_capitulo.delete(0.0, "end")

# Función para ajustar la velocidad de lectura
def ajustar_velocidad(val):
    lectura_lenta.set(val == "4")
# Variables para controlar el tamaño del texto
tamano_texto = 14  # Tamaño inicial del texto

# Función para aumentar el tamaño del texto
def aumentar_tamano():
    global tamano_texto
    tamano_texto += 2
    texto_capitulo.configure(font=("Helvetica", tamano_texto))

# Función para disminuir el tamaño del texto
def disminuir_tamano():
    global tamano_texto
    if tamano_texto > 10:  # Para evitar que el texto se haga demasiado pequeño
        tamano_texto -= 2
        texto_capitulo.configure(font=("Helvetica", tamano_texto))

# --- Botones --- 

# Botones de aumentar y disminuir el tamaño del texto
btn_aumentar = ctk.CTkButton(frame_botones, text="+", command=aumentar_tamano, width=30, height=30)
btn_aumentar.grid(row=0, column=5, padx=10, pady=5)

btn_disminuir = ctk.CTkButton(frame_botones, text="-", command=disminuir_tamano, width=30, height=30)
btn_disminuir.grid(row=0, column=6, padx=10, pady=5)


# Rediseñamos el grid de los botones para centrarlos
btn_pdf_a_audio = ctk.CTkButton(frame_botones, text="Convertir a Audio", command=convertir_a_audio)
btn_pdf_a_audio.grid(row=0, column=0, padx=10, pady=5)

btn_mostrar_pdf = ctk.CTkButton(frame_botones, text="Mostrar PDF/TXT", command=mostrar_pdf)
btn_mostrar_pdf.grid(row=0, column=1, padx=10, pady=5)

btn_leer_voz = ctk.CTkButton(frame_botones, text="Leer Selección", command=leer_en_voz_alta)
btn_leer_voz.grid(row=0, column=2, padx=10, pady=5)

btn_pausar = ctk.CTkButton(frame_botones, text="Pausar", command=pausar_lectura)
btn_pausar.grid(row=0, column=3, padx=10, pady=5)

btn_detener = ctk.CTkButton(frame_botones, text="Detener", command=detener_lectura)
btn_detener.grid(row=0, column=4, padx=10, pady=5)
try:
    # Cargar y redimensionar el logo al tamaño deseado
    logo = Image.open(resource_path("lectorlogo.png"))
    logo = logo.resize((45, 45), Image.Resampling.LANCZOS)  # Ajusta los valores (ancho, alto) según lo necesario
    logo_imagen = ImageTk.PhotoImage(logo)  # Convertimos la imagen para usarla en Tkinter
    
    # Crear el label solo con la imagen
    label_logo = ctk.CTkLabel(ventana, image=logo_imagen, text="")  # text="" asegura que no muestre texto
    label_logo.image = logo_imagen  # Mantén la referencia a la imagen para evitar problemas de garbage collection
    label_logo.place(x=25, y=10)  # Ajusta la posición del logo si es necesario
except Exception as e:
    print(f"No se pudo cargar el logo: {e}")


ventana.mainloop()
