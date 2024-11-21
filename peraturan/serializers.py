from rest_framework import serializers
from .models import Peraturan, PeraturanVersion

class PeraturanVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeraturanVersion
        fields = ['version_number', 'is_final', 'pdf_file']


class PeraturanSerializer(serializers.ModelSerializer):
    versions = PeraturanVersionSerializer(many=True, read_only=True)

    class Meta:
        model = Peraturan
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
