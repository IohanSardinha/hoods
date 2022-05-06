from rest_framework import serializers

class TestSerializer(serializers.Serializer):
   responseCode = serializers.IntegerField()
   responseText = serializers.CharField()