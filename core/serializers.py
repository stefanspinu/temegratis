from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import *
from .utils import sidebar_left_helper, getDuplicatesWithCount

from django_countries.serializer_fields import CountryField


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
    country = CountryField()
    user = UserSerializer(read_only=True)
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
    password = serializers.CharField(write_only=True, required=False)
    orders_data = serializers.SerializerMethodField()
    accepted_orders = serializers.SerializerMethodField()
    freelancer_profile_details = serializers.SerializerMethodField()
    
    def get_freelancer_profile_details(self, obj):
        accepted_order = AcceptedOrder.objects.all().filter(freelancer=obj)
        feedbacks = Feedback.objects.all().filter(accepted_order__in=accepted_order)

        data = sidebar_left_helper(
            accepted_order, feedbacks, obj.id)
        positive_rating = data['positive_rating']
        negative_rating = data['negative_rating']
        percentage_positive_raiting = data['percentage_positive_raiting']
        percentage_negative_rating = data['percentage_negative_rating']
        in_time = data['in_time']
        late = data['late']
        percentage_in_time = data['percentage_in_time']
        percentage_late = data['percentage_late']

        orders = []
        for order in accepted_order:
            orders.append(order.order)

        work_types = []
        for order in orders:
            work_types.append(order.work_type.name)

        lessons = []
        for order in orders:
            lessons.append(order.lessons.name)

        dict_of_work_types = getDuplicatesWithCount(work_types)
        dict_of_lessons = getDuplicatesWithCount(lessons)

        data_final = {
            'feedbacks': FeedbackSerializer(feedbacks, many=True, context=self.context).data,
            'positive_rating': positive_rating,
            'negative_rating': negative_rating,
            'percentage_positive_raiting': percentage_positive_raiting,
            'percentage_negative_rating': percentage_negative_rating,
            'in_time': in_time,
            'late': late,
            'percentage_in_time': percentage_in_time,
            'percentage_late': percentage_late,
            'work_types': dict_of_work_types.items(),
            'lessons': dict_of_lessons.items(),
        }

        return data_final

    def get_accepted_orders(self, instance):
        queryset = AcceptedOrder.objects.filter(freelancer=instance)
        return AcceptedOrderSerializer(queryset, many=True, context=self.context).data

    def get_orders_data(self, obj):
        freelancer = Freelancer.objects.get(user=obj.user)
        accepted_order = AcceptedOrder.objects.all().filter(
            freelancer=freelancer)
        feedbacks = Feedback.objects.all().filter(accepted_order__in=accepted_order)

        data = sidebar_left_helper(
            accepted_order, feedbacks, obj.id)
        finished = data['finished']
        working_at = data['working_at']
        total_clients = data['total_clients']
        permament_clients = data['permament_clients']

        data_final = {
            'finished': finished,
            'working_at': working_at,
            'total_clients': total_clients,
            'permament_clients': permament_clients,
        }

        return data_final

    class Meta:
        fields = '__all__'
        model = Freelancer
    
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

    
class FreelancerOnlyNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Freelancer
        fields = ['first_name']


class ClientSerializer(serializers.ModelSerializer):
    country = CountryField()
    user = UserSerializer(read_only=True)
    password = serializers.CharField(write_only=True, required=False)
    orders_data = serializers.SerializerMethodField()
    clients_orders = serializers.SerializerMethodField()
    clients_orders_in_work = serializers.SerializerMethodField()

    def get_clients_orders(self, instance):
        queryset = Order.objects.filter(client=instance)
        return OrderSerializer(queryset, many=True, context=self.context).data

    def get_clients_orders_in_work(self, instance):
        queryset = AcceptedOrder.objects.filter(user=instance.user, completed=False)
        return AcceptedOrderSerializer(queryset, many=True, context=self.context).data

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


class ClientWithoutPassSerializer(serializers.ModelSerializer):
    country = CountryField()
    user = UserSerializer()
    class Meta:
        model = Client
        exclude = ['password']
    

class OrderSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(
        slug_field='first_name',
        read_only=True
    )
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    in_auction = serializers.BooleanField(read_only=True)

    freelancers = serializers.SerializerMethodField()

    def get_freelancers(self, instance):
        dataa = []
        for i in instance.freelancers.all():
            queryset = Freelancer.objects.filter(first_name=i.first_name)
            dataa.append(FreelancerOnlyNameSerializer(queryset, many=True, context=self.context).data)
        return dataa
    work_type = serializers.SlugRelatedField(
        queryset=Work_Type.objects.all(),
        slug_field='name'
    )
    lessons = serializers.SlugRelatedField(
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


# Maybe use validators to allow client to only view and freelancer to post, put and delete files and descriptions fields.
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


class FreelancerAcceptedOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcceptedOrder
        fields = ('files', 'description', 'completed', 'delivered_date')

class UserAcceptedOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcceptedOrder
        fields = ('paied',)