import os

import os

def extract_code_to_txt(base_directory, output_file, prompt, ignore_dirs=None, ignore_files=None):
    if ignore_dirs is None:
        ignore_dirs = []
    if ignore_files is None:
        ignore_files = []

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(f"{prompt} \n\n Berikut adalah perkembangan code dan struktur folder saat ini :  \n\n")
        for root, dirs, files in os.walk(base_directory):
            # Mengabaikan direktori tertentu
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            for file in files:
                # Mengabaikan file tertentu
                if file in ignore_files:
                    print(f"Skipping file (ignored): {os.path.join(root, file)}")
                    continue

                file_path = os.path.join(root, file)
                
                # Pastikan hanya memproses file reguler
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            code = f.readlines()
                    except UnicodeDecodeError:
                        # Jika file tidak dapat didekode dengan utf-8, lewati
                        print(f"Skipping file (encoding issue): {file_path}")
                        continue
                    except Exception as e:
                        # Menangani kesalahan lain
                        print(f"Error reading file {file_path}: {e}")
                        continue
                    
                    # Tulis format sesuai permintaan
                    outfile.write(f"[{file_path}]:\n")
                    outfile.write(f'""" Start isi code [{file}] """\n\n')
                    
                    # Menambahkan indentasi pada setiap baris kode
                    for line in code:
                        outfile.write("\t" + line)

                    outfile.write(f'\n""" End code [{file}] """\n\n')


if __name__ == "__main__":
    # Ganti '/path/to/your/directory' dengan path direktori yang ingin Anda proses
    base_dir = '/home/enigmap/aptika/jdih_history/'
    
    # Ganti 'output.txt' dengan nama file output yang diinginkan
    output_txt = '/home/enigmap/aptika/jdih_history//output.txt'
    
    # Daftar direktori yang akan diabaikan
    ignore_dirs = ['migrations', '.git', '__pycache__', 'node_modules', 'env', 'venv', 'peraturan_pdfs' '/home/enigmap/aptika/jdih_history/peraturan/migrations', '/home/enigmap/aptika/jdih_history/jdih_history/utils', '/home/enigmap/aptika/jdih_history/peraturan/migrations/']  # Tambahkan direktori lain sesuai kebutuhan
    
    # Daftar file yang akan diabaikan
    ignore_files = ['output.txt','Makefile', 'README.md', 'LICENSE', 'manage.py', 'Makefile' 'output', 'generate_project_structure.py', '.gitignore',
                    'requirements.txt',
                    '.env',
                    'wsgi.py',
                    'asgi.py',
                    '__init__.py',
                    'tests.py',
                    'app.py',
                    'admin.py']  # Tambahkan file lain sesuai kebutuhan
    prompt = "Hallo Gaesadass"
    extract_code_to_txt(base_dir, output_txt, prompt, ignore_dirs, ignore_files)
    print(f"Semua kode telah diekstrak ke {output_txt}")
