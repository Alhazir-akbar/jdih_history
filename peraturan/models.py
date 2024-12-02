from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

# Utils import can be adjusted based on actual utility functions
from .utils.utils import extract_pdf_content

class Peraturan(models.Model):
    JENIS_PERATURAN_CHOICES = [
        ('UU', 'Undang-Undang'),
        ('PP', 'Peraturan Pemerintah'),
        ('Perpres', 'Peraturan Presiden'),
        # Add other types if necessary
    ]
    
    STATUS_PRODUK_CHOICES = [
        ('draft', 'Draft'),
        ('final', 'Final'),
        ('revised', 'Revised'),
    ]
    
    BAHASA_CHOICES = [
        ('id', 'Indonesian'),
        ('en', 'English'),
    ]
    
    judul_peraturan = models.TextField()
    tahun_terbit = models.PositiveIntegerField()
    nomor = models.CharField(max_length=50)
    singkatan_jenis = models.CharField(max_length=50)
    tanggal_penetapan = models.DateField()
    tanggal_pengundangan = models.DateField()
    teu_badan = models.CharField(max_length=255)
    sumber = models.CharField(max_length=255)
    tempat_terbit = models.CharField(max_length=255)
    bidang_hukum = models.CharField(max_length=255)
    subjek = models.CharField(max_length=255)
    lokasi = models.CharField(max_length=255)
    urusan_pemerintahan = models.CharField(max_length=255)

    bahasa = models.CharField(max_length=2, choices=BAHASA_CHOICES)  # Adjusted max_length to 2 for language codes
    id_tracking = models.CharField(max_length=255, unique=True)  # Ensure tracking ID is unique
    status_produk = models.CharField(max_length=50, choices=STATUS_PRODUK_CHOICES)  # Added choices for status_produk
    jenis_peraturan = models.CharField(max_length=50, choices=JENIS_PERATURAN_CHOICES)  # Adjusted max_length

    keterangan_status = models.TextField(blank=True, null=True)  # Allow keterangan_status to be optional
    penandatangan = models.CharField(max_length=255, blank=True, null=True)  # Allow penandatangan to be optional
    pemrakarsa = models.CharField(max_length=255, blank=True, null=True)  # Allow pemrakarsa to be optional
    peraturan_terkait = ArrayField(models.CharField(max_length=255), blank=True, null=True)
    dokumen_terkait = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.jenis_peraturan} {self.nomor} Tahun {self.tahun_terbit}"

class PeraturanVersion(models.Model):
    peraturan = models.ForeignKey(Peraturan, related_name='versions', on_delete=models.CASCADE)
    version_number = models.PositiveIntegerField()
    is_final = models.BooleanField(default=False)
    pdf_file = models.FileField(upload_to='peraturan_pdfs/')
    extracted_content = models.JSONField()  # JSONField is now fully supported by Django
    changed_fields = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('peraturan', 'version_number')
        ordering = ['version_number']

    def __str__(self):
        return f"{self.peraturan} - Versi {self.version_number}"