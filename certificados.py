from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
from io import BytesIO

# === CONFIGURACIÓN ===
PLANTILLA = "Certificado de Reconocimiento Elegante Azul y blanco.pdf"
CARPETA_SALIDA = "Certificados"
FUENTE = "Helvetica-Bold"
TAMANO_TEXTO = 22
COLOR_TEXTO = (0, 0, 0)  # negro

# Coordenadas (x, y) donde se escribirá el nombre
# 🔧 Ajusta según tu plantilla — puedes mover más arriba o abajo
POSICION_NOMBRE = (300, 330)

# === LISTA DE ESTUDIANTES ===
nombres = [
    "nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn"
]

# === FUNCIÓN PARA CAPITALIZAR ===
def formatear_nombre(nombre):
    return " ".join(p.capitalize() for p in nombre.split())

# === CREAR CARPETA DE SALIDA ===
os.makedirs(CARPETA_SALIDA, exist_ok=True)

# === PROCESAR CERTIFICADOS ===
for nombre in nombres:
    nombre_fmt = formatear_nombre(nombre)

    # Crear PDF temporal con el nombre
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont(FUENTE, TAMANO_TEXTO)
    can.setFillColorRGB(*COLOR_TEXTO)

    # Centrar texto horizontalmente (ajustable)
    x, y = POSICION_NOMBRE
    can.drawCentredString(x, y, nombre_fmt)
    can.save()

    # Volver al inicio del buffer
    packet.seek(0)

    # Cargar PDFs
    existing_pdf = PdfReader(open(PLANTILLA, "rb"))
    overlay_pdf = PdfReader(packet)
    output = PdfWriter()

    page = existing_pdf.pages[0]
    page.merge_page(overlay_pdf.pages[0])
    output.add_page(page)

    # Guardar PDF resultante
    nombre_archivo = f"Certificado_{nombre_fmt.replace(' ', '_')}.pdf"
    ruta_salida = os.path.join(CARPETA_SALIDA, nombre_archivo)
    with open(ruta_salida, "wb") as outputStream:
        output.write(outputStream)

    print(f"✅ Generado: {nombre_fmt}")

print("\n🎉 Todos los certificados fueron creados en la carpeta 'Certificados'.")
