# peraturan/serializers.py

from rest_framework import serializers
from django.utils import timezone
from .models import Peraturan, PeraturanVersion

class PeraturanVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeraturanVersion
        fields = ['id', 'version_number', 'is_final', 'pdf_file', 'extracted_content', 'changed_fields', 'created_at', 'updated_at', 'updated_by']
        read_only_fields = ['id', 'version_number', 'extracted_content', 'changed_fields', 'created_at', 'updated_at', 'updated_by']

    def validate_peraturan_terkait(self, value):
        if value:
            if not isinstance(value, list):
                raise serializers.ValidationError("Peraturan terkait harus berupa daftar.")
            for item in value:
                if not isinstance(item, str):
                    raise serializers.ValidationError("Setiap peraturan terkait harus berupa string.")
        return value
    
    def validate_pdf_file(self, value):
        if not value.name.endswith('.pdf'):
            raise serializers.ValidationError("Lampiran harus berupa file PDF.")
        return value
    
class PeraturanSerializer(serializers.ModelSerializer):
    versions = PeraturanVersionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Peraturan
        fields = [
            'id',
            'jenis_peraturan',
            'judul_peraturan',
            'tahun_terbit',
            'nomor',
            'singkatan_jenis',
            'tanggal_penetapan',
            'tanggal_pengundangan',
            'teu_badan',
            'sumber',
            'tempat_terbit',
            'bidang_hukum',
            'subjek',
            'bahasa',
            'lokasi',
            'urusan_pemerintahan',
            'status_produk',
            'keterangan_status',
            'penandatangan',
            'pemrakarsa',
            'peraturan_terkait',
            'dokumen_terkait',
            'created_at',
            'updated_at',
            'versions'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'versions']
    
    # Field-level validation
    def validate_tahun_terbit(self, value):
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError("Tahun terbit tidak boleh di masa depan.")
        return value
    
    def validate_nomor(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Nomor peraturan harus berupa angka.")
        return value
    
    def validate_tanggal_penetapan(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("Tanggal penetapan tidak boleh di masa depan.")
        return value
    
    def validate_tanggal_pengundangan(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("Tanggal pengundangan tidak boleh di masa depan.")
        return value
    
    # Object-level validation
    def validate(self, data):
        tanggal_penetapan = data.get('tanggal_penetapan')
        tanggal_pengundangan = data.get('tanggal_pengundangan')
        
        if tanggal_pengundangan and tanggal_penetapan:
            if tanggal_pengundangan < tanggal_penetapan:
                raise serializers.ValidationError("Tanggal pengundangan tidak boleh sebelum tanggal penetapan.")
        
        return data

class PeraturanListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Peraturan
        fields = ['id', 'jenis_peraturan', 'status_produk', 'created_at', 'updated_at']


class PeraturanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Peraturan
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    