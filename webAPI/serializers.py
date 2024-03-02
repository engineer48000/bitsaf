from rest_framework import serializers
from rest_framework.exceptions import APIException, ValidationError
from .models import Transactions, AdminHistory


class TransactionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transactions
        fields = '__all__'


class AdminHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = AdminHistory
        fields = '__all__'
