from rest_framework import serializers
from .models import Deals, Bonds


class DealsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deals
        fields = '__all__'
        read_only_fields = ('user', 'price_at_the_time')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        bond = Bonds.objects.get(id=validated_data['bonds'].id)
        validated_data['price_at_the_time'] = bond.price
        return super().create(validated_data)


class BondsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bonds
        fields = '__all__'
