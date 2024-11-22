import os
import shutil
import pdfplumber
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

def extract_text_from_pdf(pdf_path, output_txt='extracted_text.txt', lang='ind'):
    # Tetapkan TESSDATA_PREFIX sebelum mengimpor pytesseract
    os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract-ocr/5/'

    # Debug: Tampilkan nilai TESSDATA_PREFIX
    print(f"TESSDATA_PREFIX: {os.environ.get('TESSDATA_PREFIX')}")

    # Debug: Tampilkan path Tesseract
    tesseract_path = shutil.which('tesseract')
    print(f"Tesseract path: {tesseract_path}")

    # Buat direktori sementara untuk menyimpan gambar
    image_output_path = 'temp_image'
    if not os.path.exists(image_output_path):
        os.makedirs(image_output_path)

    extracted_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        num_pages = len(pdf.pages)
        print(f"Jumlah halaman: {num_pages}")

        for page_num, page in enumerate(pdf.pages):
            print(f"Memproses halaman {page_num + 1}...")

            # Coba ekstraksi teks menggunakan PDFPlumber
            text = page.extract_text()

            if text and text.strip():
                print("Teks ditemukan, menambahkan ke hasil.")
                extracted_text += text + "\n"
            else:
                print("Tidak ada teks, melakukan OCR pada gambar.")
                # Konversi halaman PDF ke gambar
                images = convert_from_path(pdf_path, first_page=page_num + 1, last_page=page_num + 1)
                for image in images:
                    image_path = os.path.join(image_output_path, f'page_{page_num + 1}.png')
                    image.save(image_path, 'PNG')

                    # Lakukan OCR menggunakan pytesseract
                    config = '--tessdata-dir "/usr/share/tesseract-ocr/5/tessdata/"'
                    try:
                        ocr_text = pytesseract.image_to_string(image, lang=lang, config=config)
                        extracted_text += ocr_text + "\n"
                    except pytesseract.TesseractError as e:
                        print(f"Error saat melakukan OCR pada halaman {page_num + 1}: {e}")

    # Hapus direktori sementara
    shutil.rmtree(image_output_path)

    # Simpan hasil ekstraksi ke file teks
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write(extracted_text)

    print(f"Ekstraksi selesai. Hasil disimpan di '{output_txt}'.")

if __name__ == "__main__":
    # Path ke file PDF yang ingin diekstrak
    pdf_path = '/home/enigmap/aptika/jdih_history/media/peraturan_pdfs/Keputusan_Gubernur_Daerah_Istimewa_Yogyakarta_QrTZyoF.pdf'  # Ganti dengan path PDF Anda

    # Pastikan path Tesseract sudah benar (hanya untuk Windows)
    # Jika Anda menggunakan Windows, uncomment dan sesuaikan path di bawah ini
    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # Panggil fungsi ekstraksi
    extract_text_from_pdf(pdf_path, output_txt='extracted_text.txt', lang='ind')
