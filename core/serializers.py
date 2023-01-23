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
        exclude = ['country']
    
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

    orders_data = serializers.SerializerMethodField()

    def get_orders_data(self, obj):
        clients_orders = Order.objects.all().filter(client=obj).count()
        in_work_orders = AcceptedOrder.objects.all().filter(
            user=obj.user, paied=False).count()
        finished_orders = AcceptedOrder.objects.all().filter(
            user=obj.user, paied=True).count()
        client_auction_orders = clients_orders - in_work_orders - finished_orders

        data = {
            'clients_orders': clients_orders,
            'in_work_orders': in_work_orders,
            'finished_orders': finished_orders,
            'client_auction_orders': client_auction_orders
        }

        return data

    class Meta:
        model = Client
        # fields = '__all__'
        exclude = ['country']
        
    
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


class ClientWithoutPassSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Client
        exclude = ['country', 'password']
    

class OrderSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(
        queryset=Client.objects.all(),
        slug_field='first_name'
    )

    freelancers = serializers.SlugRelatedField(
        many=True,
        queryset=Freelancer.objects.all(),
        slug_field='first_name'
    )
    work_type = serializers.SlugRelatedField(
        queryset=Work_Type.objects.all(),
        slug_field='name'
    )
    lessons = LessonSerializer()

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
    order = serializers.SlugRelatedField(
        queryset=Order.objects.all(),
        slug_field='title'
    )

    class Meta:
        model = AcceptedOrder
        exclude = ['user']


class FeedbackSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.accepted_order.order.title

    class Meta:
        model = Feedback
        fields = '__all__'

