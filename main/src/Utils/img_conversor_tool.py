import os
from PIL import Image

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))

INPUT_FOLDER = os.path.join(ROOT_DIR, "static", "img", "original-photos-web")
OUTPUT_FOLDER = os.path.join(ROOT_DIR, "static", "img")

TARGET_WIDTH = 1200
QUALITY = 85

def optimizar_imagen(input_path, output_folder, target_width):
    """
    Abre una imagen, la redimensiona manteniendo el aspecto, 
    la convierte a WebP y la guarda optimizada.
    """
    try:
        with Image.open(input_path) as img:
            width_percent = (target_width / float(img.size[0]))
            new_height = int((float(img.size[1]) * float(width_percent)))

            print(f"Redimensionando de {img.size} a ({target_width}, {new_height})...")
            img_resized = img.resize((target_width, new_height), Image.Resampling.LANCZOS)

            filename = os.path.basename(input_path)
            name_without_ext = os.path.splitext(filename)[0]
            new_filename = f"{name_without_ext}.webp"
            output_path = os.path.join(output_folder, new_filename)
            img_resized.save(output_path, 'WEBP', quality=QUALITY, optimize=True)
            
            print(f"Éxito: Guardado en {output_path}")
    except Exception as e:
        print(f"Error procesando {input_path}: {e}")

def procesar_todas_las_imagenes():
    """
    Procesa todas las imágenes en la carpeta de entrada y las guarda en la de salida.
    """
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print(f"Creada carpeta de salida: {OUTPUT_FOLDER}")

    if not os.path.exists(INPUT_FOLDER):
        os.makedirs(INPUT_FOLDER)
        print(f"Por favor, coloca tus imágenes originales en la carpeta '{INPUT_FOLDER}'")
        return

    valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    
    files_processed = 0
    print(f"--- Iniciando optimización de imágenes para la web ---")
    print(f"Objetivo: Ancho {TARGET_WIDTH}px, Formato WebP, Calidad {QUALITY}")

    for filename in os.listdir(INPUT_FOLDER):
        if filename.lower().endswith(valid_extensions):
            input_path = os.path.join(INPUT_FOLDER, filename)
            print(f"\\nProcesando: {filename}")
            optimizar_imagen(input_path, OUTPUT_FOLDER, TARGET_WIDTH)
            files_processed += 1
        else:
             if not os.path.isdir(os.path.join(INPUT_FOLDER, filename)):
                 print(f"Saltando archivo no compatible: {filename}")

    print(f"\\n--- Finalizado. Se procesaron {files_processed} imágenes. ---")
    print(f"Revisa la carpeta '{OUTPUT_FOLDER}'")

if __name__ == "__main__":
    procesar_todas_las_imagenes()