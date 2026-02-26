from rest_framework import serializers
from .models import Analysis


class AnalysisSerializer(serializers.ModelSerializer):
    about_display = serializers.CharField(source='get_about_display', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Analysis
        fields = [
            'id', 'about', 'about_display', 'type', 'type_display','period_start',
            'period_end', 'description', 'result_image', 'created_at'
        ]

        read_only_fields = ['id', 'result_image', 'created_at']