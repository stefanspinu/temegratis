from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


def get_user_image_folder(instance, filename):
    return "%s/%s" % (instance.user.id, filename)


class Work_Type(models.Model):
    name = models.CharField(max_length=40, null=True)

    def __str__(self):
        return self.name


class Work_Category(models.Model):
    name = models.CharField(max_length=40, null=True)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=40, null=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=40, null=True)
    work_category = models.ManyToManyField(Work_Category)

    def __str__(self):
        return self.name


class Freelancer(models.Model):

    LEARNING_STATE = [
        ('Student', 'Student'),
        ('Absolvent', 'Absolvent'),
        ('Profesor', 'Profesor')
    ]

    ACADEMIC_DEGREES = [
        ('Nici una', 'Nici una'),
        ('Doctor', 'Doctor'),
        ('Doctorat', 'Doctorat')
    ]

    ACADEMIC_TITLES = [
        ('Fără rang', 'Fără rang'),
        ('Docent', 'Docent'),
        ('Profesor', 'Profesor')
    ]

    profile_pic = models.ImageField(
        default='default-user.jpg', upload_to=get_user_image_folder, null=True, blank=True)
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20)
    email = models.EmailField(max_length=30)
    date_of_birth = models.DateField(
        verbose_name='Date of Birth', null=True, blank=True)
    country = CountryField()
    state = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    password = models.CharField(max_length=30)
    views = models.IntegerField(default=0)
    short_description = models.CharField(max_length=70, null=True, blank=True)
    description = models.CharField(max_length=240, null=True, blank=True)
    educational_institution = models.CharField(
        max_length=70, null=True, blank=True)
    faculty = models.CharField(max_length=70, null=True, blank=True)
    specialty = models.CharField(max_length=70, null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=LEARNING_STATE, default='Student', null=True, blank=True)
    year_of_learning_end = models.DateField(blank=True, null=True,
                                            verbose_name='Year of learning end')
    academic_degree = models.CharField(
        max_length=15, choices=ACADEMIC_DEGREES, default='Nici una', null=True, blank=True)
    academic_title = models.CharField(
        max_length=10, choices=ACADEMIC_TITLES, default='Fără rang', null=True, blank=True)
    desertation_topic = models.CharField(max_length=70, null=True, blank=True)
    additional_education = models.CharField(
        max_length=1000, null=True, blank=True)
    video_consultation = models.BooleanField(
        default=False, null=True, blank=True)
    work_type = models.ManyToManyField(Work_Type)
    work_category = models.ManyToManyField(Work_Category)
    languages = models.ManyToManyField(Language)
    lessons = models.ManyToManyField(Lesson)

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def __str__(self):
        return self.first_name


class Client(models.Model):
    profile_pic = models.ImageField(
        default='default-user.jpg', upload_to=get_user_image_folder, null=True, blank=True)
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20)
    email = models.EmailField(max_length=30)
    date_of_birth = models.DateField(
        verbose_name='Date of Birth', null=True, blank=True)
    country = CountryField()
    state = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    password = models.CharField(max_length=30)

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def __str__(self):
        return self.first_name


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateField(auto_now_add=True)
    limit_date = models.DateField(null=True)
    title = models.CharField(max_length=100)
    short_description = models.CharField(max_length=100)
    description = models.TextField(max_length=1500, null=True, blank=True)
    files = models.FileField(null=True, blank=True,
                             upload_to=get_user_image_folder)
    min_size = models.IntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    max_size = models.IntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    price = models.IntegerField(null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    premium = models.BooleanField(default=None, null=True, blank=True)
    freelancers = models.ManyToManyField(
        Freelancer, blank=True)
    work_type = models.ForeignKey(
        Work_Type, on_delete=models.SET_NULL, null=True, blank=True)
    lessons = models.ForeignKey(
        Lesson, on_delete=models.SET_NULL, null=True, blank=True)
    in_auction = models.BooleanField(default=True)

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def __str__(self):
        return self.title


class FavouriteOrder(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    is_fav = models.BooleanField(default=False)

    def __str__(self):
        return self.order.title


class AcceptedOrder(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, null=True)
    freelancer = models.ForeignKey(
        Freelancer, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(max_length=1500, null=True, blank=True)
    files = models.FileField(null=True, blank=True,
                             upload_to=get_user_image_folder)
    completed = models.BooleanField(default=False)
    delivered_date = models.DateField(null=True, blank=True)
    paied = models.BooleanField(default=False)

    def __str__(self):
        return self.order.title


class Feedback(models.Model):
    accepted_order = models.OneToOneField(
        AcceptedOrder, on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=500)
    rating = models.IntegerField(default=0, validators=[
        MaxValueValidator(5), MinValueValidator(0)])

    def __str__(self):
        return self.accepted_order.order.title
