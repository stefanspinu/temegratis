import django_filters
from django_filters import CharFilter, DateFilter, Filter
from django import forms

from .models import *


class OrdersFilter(django_filters.FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains', label='')
    work_types = django_filters.ModelMultipleChoiceFilter(widget=forms.CheckboxSelectMultiple,
                                                          field_name='work_type__name', to_field_name='name', queryset=Work_Type.objects.all(), label='')
    lessons = django_filters.ModelMultipleChoiceFilter(widget=forms.CheckboxSelectMultiple,
                                                       field_name='lessons__name', to_field_name='name', queryset=Lesson.objects.all(), label='')
    date_created = DateFilter(field_name='date_created', lookup_expr='gte')
    limit_date = DateFilter(field_name='limit_date', lookup_expr='lte')
    # contractual = django_filters.BooleanFilter(field_name=, widget=forms.BooleanField)
    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(
        field_name='price', lookup_expr='gte')
    price__lt = django_filters.NumberFilter(
        field_name='price', lookup_expr='lte')

    class Meta:
        model = Order
        exclude = ['lessons', 'files', 'date_created', 'limit_date', 'short_description',
                   'description', 'min_size', 'max_size', 'price', 'client', 'premium', 'work_type']


class FreelancersFileter(django_filters.FilterSet):
    first_name = CharFilter(field_name='first_name',
                            lookup_expr='icontains', label='')
    work_type = django_filters.ModelChoiceFilter(
        field_name='work_type__name', to_field_name='name', queryset=Work_Type.objects.all(), label='')
    work_category = django_filters.ModelMultipleChoiceFilter(widget=forms.CheckboxSelectMultiple,
                                                             field_name='work_category__name', to_field_name='name', queryset=Work_Category.objects.all(), label='')

    class Meta:
        model = Freelancer
        fields = ['first_name', 'work_type', 'work_category']


from django_filters import rest_framework as filters
from django.db.models import Count


class ExcludeCurrentFreelancerFilter(django_filters.Filter):
    def filter(self, qs, value):
        if not value:
            return qs
        return qs.exclude(freelancers=value)

class OrderFilter(filters.FilterSet):
    less_than_x_freelancers = django_filters.NumberFilter(field_name='num_freelancers', lookup_expr='lt')
    exclude_current_freelancer = ExcludeCurrentFreelancerFilter()

    class Meta:
        model = Order
        fields = ['work_type','lessons','limit_date','min_size','max_size','premium','less_than_x_freelancers','exclude_current_freelancer']

    def __init__(self, *args, **kwargs):
        super(OrderFilter, self).__init__(*args, **kwargs)
        self.queryset = self.queryset.annotate(num_freelancers=Count('freelancers'))