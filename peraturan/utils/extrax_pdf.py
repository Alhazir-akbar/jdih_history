import os
import pdfplumber
from pdf2image import convert_from_path
from PIL import Image, ImageDraw

def extract_text_with_coordinates(pdf_path, output_dir="output", coordinates=[]):
    """
    Ekstrak teks berdasarkan koordinat dan buat validasi kotak area di gambar halaman.
    
    Parameters:
    - pdf_path: Path ke file PDF.
    - output_dir: Direktori untuk menyimpan gambar validasi.
    - coordinates: List koordinat dalam format [(x0, y0, x1, y1), ...].
    """
    # Buat folder output jika belum ada
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Buka file PDF
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            print(f"Memproses halaman {page_num + 1}...")
            
            # Render halaman ke gambar untuk validasi
            image = page.to_image()
            pil_image = image.original
            
            # Salin gambar untuk menggambar kotak
            draw = ImageDraw.Draw(pil_image)
            
            # Ekstraksi teks berdasarkan koordinat
            for idx, bbox in enumerate(coordinates):
                x0, y0, x1, y1 = bbox
                
                # Potong area teks
                cropped = page.within_bbox(bbox)
                text = cropped.extract_text()
                
                print(f"Teks pada koordinat {bbox}:\n{text}")
                
                # Gambar kotak di gambar validasi
                draw.rectangle(bbox, outline="red", width=3)
            
            # Simpan gambar validasi dengan kotak
            output_image_path = f"{output_dir}/page_{page_num + 1}_validation.png"
            pil_image.save(output_image_path)
            print(f"Gambar validasi disimpan di: {output_image_path}")
            break

# Contoh penggunaan
pdf_path = "/home/enigmap/aptika/jdih_history/media/peraturan_pdfs/Keputusan_Gubernur_Daerah_Istimewa_Yogyakarta_RTr2Uu8.pdf"

# Koordinat: [(x0, y0, x1, y1)]
coordinates = [
    #Kiri, Atas, kanan, Bawah
    (100, 140, 520, 235),  # Judul : GUBERNUR DAERAH ISTIMEWA YOGYAKARTA
    (40, 240, 580, 380)   # Misalnya area isi
]

extract_text_with_coordinates(pdf_path, output_dir="output_validation", coordinates=coordinates)
