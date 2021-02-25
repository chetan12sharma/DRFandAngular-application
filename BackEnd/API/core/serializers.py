from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db import models
from django.db.models import fields
from .models import Manager, Plan, SubscribedPlan
from rest_framework import serializers


class UserSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "company",
            "DOB",
            "address",
        ]


class PlanSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = "__all__"


class SubscribedPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscribedPlan
        fields = "__all__"


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        print(attrs)
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        data.update({"id": self.user.id})
        data.update({"first_name": self.user.first_name})
        data.update({"last_name": self.user.last_name})
        return data
