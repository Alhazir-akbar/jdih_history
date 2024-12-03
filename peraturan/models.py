from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from .utils.utils import extract_pdf_content

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Profile(AbstractUser):
    """
    Extended user model untuk sistem manajemen peraturan.
    Menambahkan informasi tambahan dan peran spesifik.
    """
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('viewer', 'Pengunjung/Pembaca'),
        
        ('OPD', 'Admin OPD'),
        ('Verikator', 'Kabag PUU'),
        ('Drafter', 'Staf PUU'),
        ('External', 'External'), #Kemenkumham dan  Kemendagri. Perlu dikaji  kemungkinan integrasi


    ]

    nik = models.CharField(
        max_length=20, 
        unique=True, 
        null=True, 
        blank=True, 
        verbose_name='Nomor Induk Pegawai'
    )
    
    phone_number = models.CharField(
        max_length=15, 
        null=True, 
        blank=True, 
        verbose_name='Nomor Telepon'
    )
    
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='viewer',
        verbose_name='Peran Pengguna'
    )
    
    is_active_user = models.BooleanField(
        default=True, 
        verbose_name='Pengguna Aktif'
    )
    
    last_login_at = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name='Terakhir Login'
    )
    
    created_at = models.DateTimeField(
        default=timezone.now, 
        verbose_name='Tanggal Dibuat'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name='Terakhir Diperbarui'
    )

    groups = models.ManyToManyField(
        'GroupProfile', 
        related_name='members', 
        blank=True,
        verbose_name='Keanggotaan Kelompok'
    )

    # Tambahkan method untuk mengelola keanggotaan group
    def bergabung_group(self, group):
        """Metode untuk bergabung ke dalam group"""
        group.members.add(self)
    
    def keluar_group(self, group):
        """Metode untuk keluar dari group"""
        group.members.remove(self)

    def update_last_login(self):
        """
        Metode untuk memperbarui waktu login terakhir
        """
        self.last_login_at = timezone.now()
        self.save(update_fields=['last_login_at'])

    class Meta:
        verbose_name = 'Pengguna Sistem'
        verbose_name_plural = 'Pengguna Sistem'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"

class GroupProfile(models.Model):
    """
    Model untuk mengelompokkan pengguna dalam sistem manajemen peraturan.
    """
    GROUP_TYPE_CHOICES = [
        ('internal', 'Internal'),
        ('external', 'External'),
    ]

    STATUS_CHOICES = [
        ('active', 'Aktif'),
        ('inactive', 'Tidak Aktif')
    ]
    
    nama_group = models.CharField(
        max_length=100, 
        verbose_name='Nama Kelompok',
        unique=True
    )
    
    deskripsi = models.TextField(
        blank=True, 
        null=True, 
        verbose_name='Deskripsi Kelompok'
    )
    
    tipe_group = models.CharField(
        max_length=20, 
        choices=GROUP_TYPE_CHOICES, 
        default='internal',
        verbose_name='Tipe Kelompok'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='Status Kelompok'
    )
    
    created_by = models.ForeignKey(
        Profile, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='groups_created',
        verbose_name='Dibuat Oleh'
    )
    
    created_at = models.DateTimeField(
        default=timezone.now, 
        verbose_name='Tanggal Dibuat'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name='Terakhir Diperbarui'
    )

    class Meta:
        verbose_name = 'Kelompok Pengguna'
        verbose_name_plural = 'Kelompok Pengguna'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.nama_group} ({self.get_tipe_group_display()})"

class Peraturan(models.Model):
    JENIS_PERATURAN_CHOICES = [
        ('UU', 'Undang-Undang'),
        ('PP', 'Peraturan Pemerintah'),
        ('Perpres', 'Peraturan Presiden'),
        
    ]
    
    STATUS_PRODUK_CHOICES = [
        ('draft', 'Draft'),
        ('final', 'Final'),
        ('revised', 'Revised'),
    ]
    
    judul_peraturan = models.TextField()
    tahun_terbit = models.CharField(max_length=50)
    nomor = models.CharField(max_length=50)
    singkatan_jenis = models.CharField(max_length=50)

    tanggal_penetapan = models.CharField(max_length=50)
    tanggal_pengundangan = models.CharField(max_length=50)

    teu_badan = models.CharField(max_length=255)
    sumber = models.CharField(max_length=255)
    tempat_terbit = models.CharField(max_length=255)
    bidang_hukum = models.CharField(max_length=255)
    subjek = models.CharField(max_length=255)
    lokasi = models.CharField(max_length=255)
    urusan_pemerintahan = models.CharField(max_length=255)

    id_tracking = models.CharField(max_length=255, unique=True)  
    status_produk = models.CharField(max_length=50, choices=STATUS_PRODUK_CHOICES)  
    jenis_peraturan = models.CharField(max_length=50, choices=JENIS_PERATURAN_CHOICES)  

    keterangan_status = models.TextField(blank=True, null=True)  
    penandatangan = models.CharField(max_length=255, blank=True, null=True)  
    pemrakarsa = models.CharField(max_length=255, blank=True, null=True)  
    
    peraturan_terkait = ArrayField(models.CharField(max_length=255), blank=True, null=True)
    dokumen_terkait = ArrayField(models.CharField(max_length=255), blank=True, null=True)
    
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=False, null=False)
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
    updated_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('peraturan', 'version_number')
        ordering = ['version_number']

    def __str__(self):
        return f"{self.peraturan} - Versi {self.version_number}"