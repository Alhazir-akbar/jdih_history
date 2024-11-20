from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField

from peraturan.utils.utils import extract_pdf_content

class Peraturan(models.Model):
    # Informasi Umum
    jenis_peraturan = models.CharField(max_length=255)
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
    bahasa = models.CharField(max_length=50)
    lokasi = models.CharField(max_length=255)
    urusan_pemerintahan = models.CharField(max_length=255)
    status_produk = models.CharField(max_length=50)
    keterangan_status = models.TextField()
    penandatangan = models.CharField(max_length=255)
    pemrakarsa = models.CharField(max_length=255)
    peraturan_terkait = ArrayField(
        models.CharField(max_length=255),
        blank=True,
        null=True
    )
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
    extracted_content = models.JSONField()
    changed_fields = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('peraturan', 'version_number')
        ordering = ['version_number']

    def __str__(self):
        return f"{self.peraturan} - Versi {self.version_number}"

    def save(self, *args, **kwargs):
        # Ekstraksi PDF
        if self.pdf_file:
            self.pdf_file.seek(0)
            extracted_text = extract_pdf_content(self.pdf_file)
            self.extracted_content = {'text': extracted_text}
        super().save(*args, **kwargs)



