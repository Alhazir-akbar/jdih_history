# Variabel
PYTHON=python3
DJANGO_MANAGE=python3 manage.py

# Menjalankan server development
run:
	$(DJANGO_MANAGE) runserver

# Membantu dengan environment setup
install:
	pip install -r requirements.txt


# Membuat migrasi
makemigrations:
	$(DJANGO_MANAGE) makemigrations

# Menerapkan migrasi ke database
migrate:
	$(DJANGO_MANAGE) migrate

# Membuat superuser
createsuperuser:
	$(DJANGO_MANAGE) createsuperuser

# Membersihkan file pycache
clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

# Menjalankan test
test:
	$(DJANGO_MANAGE) test

# Membuat file statis
collectstatic:
	$(DJANGO_MANAGE) collectstatic --noinput

# Reset database dan mengatur ulang migrasi (gunakan dengan hati-hati)
reset-db:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete
	$(DJANGO_MANAGE) makemigrations
	$(DJANGO_MANAGE) migrate --run-syncdb

# Membantu
help:
	@echo "Command dalam Makefile ini:"
	@echo "  install         - Menginstal dependensi dari requirements.txt"
	@echo "  runserver       - Menjalankan server pengembangan Django"
	@echo "  makemigrations  - Membuat file migrasi"
	@echo "  migrate         - Menerapkan migrasi database"
	@echo "  createsuperuser - Membuat superuser untuk admin Django"
	@echo "  clean           - Membersihkan file pycache"
	@echo "  test            - Menjalankan test"
	@echo "  collectstatic   - Mengumpulkan file statis"
	@echo "  reset-db        - Mengatur ulang database dan migrasi"
