from django.utils import timezone
from rest_framework import serializers

from discounts.models import Store, PromoCode


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = '__all__'

    def validate_likes(self, value):
        if value < 0:
            raise serializers.ValidationError('Количество лайков должно быть неотрицательным.')
        return value

    def validate_dislikes(self, value):
        if value < 0:
            raise serializers.ValidationError('Количество дизлайков должно быть неотрицательным.')
        return value

    def validate_discount_percent(self, value):
        if not (0 <= value <= 100):
            raise serializers.ValidationError('Процент скидки должен быть от 0 до 100.')
        return value

    def validate_expiration_date(self, value):
        if value and value <= timezone.now().date():
            raise serializers.ValidationError('Дата окончания должна быть в будущем.')
        return value
