from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['url', 'username', 'password', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']




class WorkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work_Type
        fields = '__all__'


class WorkCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Work_Category
        fields = '__all__'


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    work_category = serializers.SlugRelatedField(
        many=True,
        queryset=Work_Category.objects.all(),
        slug_field='name'
    )
    class Meta:
        model = Lesson
        fields = '__all__'


class FreelancerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    work_category = serializers.SlugRelatedField(
        many=True,
        queryset=Work_Category.objects.all(),
        slug_field='name'
    )
    work_type = serializers.SlugRelatedField(
        many=True,
        queryset=Work_Type.objects.all(),
        slug_field='name'
    )
    languages = serializers.SlugRelatedField(
        many=True,
        queryset=Language.objects.all(),
        slug_field='name'
    )
    lessons = serializers.SlugRelatedField(
        many=True,
        queryset=Lesson.objects.all(),
        slug_field='name'
    )
    class Meta:
        model = Freelancer
        fields = '__all__'
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()
        group = Group.objects.get(name='freelancers')
        user.groups.add(group)

        return user


class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Client
        fields = '__all__'
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()
        group = Group.objects.get(name='clients')
        user.groups.add(group)

        return user


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    client = ClientSerializer()

    freelancers = serializers.SlugRelatedField(
        many=True,
        queryset=Freelancer.objects.all(),
        slug_field='first_name'
    )
    work_type = serializers.SlugRelatedField(
        many=True,
        queryset=Work_Type.objects.all(),
        slug_field='name'
    )
    lessons = serializers.SlugRelatedField(
        many=True,
        queryset=Lesson.objects.all(),
        slug_field='name'
    )
    class Meta:
        model = Order
        fields = '__all__'


class FavouriteOrderSerializer(serializers.ModelSerializer):
    freelancer = Freelancer()
    order = serializers.SlugRelatedField(
        many=True,
        queryset=Order.objects.all(),
        slug_field='title'
    )

    class Meta:
        model = FavouriteOrder
        fields = '__all__'


class AcceptedOrderSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    freelancer = Freelancer()

    class Meta:
        model = AcceptedOrder
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    accepted_order = AcceptedOrderSerializer()

    class Meta:
        model = Feedback
        fields = '__all__'

