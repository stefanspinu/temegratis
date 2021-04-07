from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django_countries.fields import CountryField
import django.forms.utils
import django.forms.widgets
from django_countries.widgets import CountrySelectWidget
from django.contrib.auth.forms import UserCreationForm

from .models import Freelancer, Client, Work_Type, Work_Category, Language, AcceptedOrder, Feedback, Lesson, Order


BIRTH_YEAR = [x for x in range(1930, 2022)]
AVAILABLE_YEARS = [x for x in range(2021, 2022)]
MONTHS = {
    1: ('1'), 2: ('2'), 3: ('3'), 4: ('4'),
    5: ('5'), 6: ('6'), 7: ('7'), 8: ('8'),
    9: ('9'), 10: ('10'), 11: ('11'), 12: ('12')
}


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


USER_TYEPS = [
    ('client', 'client'),
    ('freelancer', 'freelancer')
]


class ChangeAvatarPictureForm(forms.ModelForm):
    profile_pic = forms.FileField(widget=forms.FileInput())

    class Meta:
        model = Freelancer
        fields = ['profile_pic']


class ChangeAvatarPictureFormClient(forms.ModelForm):
    profile_pic = forms.FileField(widget=forms.FileInput())

    class Meta:
        model = Client
        fields = ['profile_pic']


class ChangeNameForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'settings-input', 'placeholder': 'Prenume'}), label='')
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'settings-input', 'placeholder': 'Nume'}), label='')
    nickname = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'settings-input', 'placeholder': 'Poreclă'}), label='')

    class Meta:
        model = Freelancer
        fields = ['first_name', 'last_name', 'nickname']


class ChangeNameFormClient(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'settings-input', 'placeholder': 'Prenume'}), label='')
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'settings-input', 'placeholder': 'Nume'}), label='')
    nickname = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'settings-input', 'placeholder': 'Poreclă'}), label='')

    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'nickname']


class ChangeDateOfBirthForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        label='', widget=forms.SelectDateWidget(months=MONTHS, years=BIRTH_YEAR, attrs={'class': 'profile__choose-small settings-choose'}))

    class Meta:
        model = Freelancer
        fields = ['date_of_birth']


class ChangeDateOfBirthFormClient(forms.ModelForm):
    date_of_birth = forms.DateField(
        label='', widget=forms.SelectDateWidget(months=MONTHS, years=BIRTH_YEAR, attrs={'class': 'profile__choose-small settings-choose'}))

    class Meta:
        model = Client
        fields = ['date_of_birth']


class ChangeContactForm(forms.ModelForm):
    email = forms.EmailField(label=False, widget=forms.EmailInput(
        attrs={'placeholder': 'Email'}))
    country = CountryField(blank_label='Țara').formfield(widget=CountrySelectWidget(
        attrs={'class': 'settings-choose'}  # doesn't work
    ))
    state = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Orașul'}), label='')
    address = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Adresa'}), label='')

    def __init__(self, *args, **kwargs):
        super(ChangeContactForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'settings-input'

    class Meta:
        model = Freelancer
        fields = ['email', 'country', 'state', 'address']


class ChangeContactFormClient(forms.ModelForm):
    email = forms.EmailField(label=False, widget=forms.EmailInput(
        attrs={'placeholder': 'Email'}))
    country = CountryField(blank_label='Țara').formfield(widget=CountrySelectWidget(
        attrs={'class': 'settings-choose'}  # doesn't work
    ))
    state = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Orașul'}), label='')
    address = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Adresa'}), label='')

    def __init__(self, *args, **kwargs):
        super(ChangeContactFormClient, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'settings-input'

    class Meta:
        model = Client
        fields = ['email', 'country', 'state', 'address']


class ChangePasswordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Parola nouă'}))

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'settings-input'

    class Meta:
        model = Freelancer
        fields = ['password']


class ChangePasswordFormClient(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Parola nouă'}))

    def __init__(self, *args, **kwargs):
        super(ChangePasswordFormClient, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'settings-input'

    class Meta:
        model = Client
        fields = ['password']


class ChangeInfoAboutYourselfForm(forms.ModelForm):
    short_description = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'settings-input', 'placeholder': 'Scurt despre tine'}), label='', required=False)
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'qualification__textarea', "rows": 3, "cols": 30}), label='', required=False)

    class Meta:
        model = Freelancer
        fields = ['short_description', 'description']


class ChangeEducationForm(forms.ModelForm):
    educational_institution = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'settings-input'}), label='Instituții de învățământ', required=False)
    faculty = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'settings-input education__block-half'}), label='Facultăți', required=False)
    specialty = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'settings-input education__block-half'}), label='Specialitate', required=False)
    status = forms.ChoiceField(choices=LEARNING_STATE, required=False, widget=forms.Select(
        attrs={'class': 'education__choose settings-choose education__block-half'}), label='Statut')
    year_of_learning_end = forms.DateField(label='Anul de terminare a studiilor(luna, ziua, anul)',
                                           widget=forms.DateInput(attrs={'class': 'education__block-half settings-input'}), required=False)
    academic_degree = forms.ChoiceField(label='Gradul academic:',
                                        choices=ACADEMIC_DEGREES, required=False, widget=forms.Select(attrs={'class': 'education__block-half settings-choose'}))
    academic_title = forms.ChoiceField(choices=ACADEMIC_TITLES, required=False, widget=forms.Select(
        attrs={'class': 'education__block-half settings-choose'}), label='Titlul academic:')

    class Meta:
        model = Freelancer
        fields = ['educational_institution', 'faculty', 'specialty', 'status',
                  'year_of_learning_end', 'academic_degree', 'academic_title']


class ChangeAdditionalEducationForm(forms.ModelForm):
    desertation_topic = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'settings-input', 'placeholder': 'Tema aproximativă a disertației'}), label='', required=False)
    additional_education = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'qualification__textarea', "rows": 3, "cols": 30}), label='Informații suplimentare despre educație', required=False)

    class Meta:
        model = Freelancer
        fields = ['desertation_topic', 'additional_education']


class ChangeVideoConsultationForm(forms.ModelForm):
    video_consultation = forms.BooleanField(
        label='Gata pentru a efectua consultări video', initial=False, required=False)

    class Meta:
        model = Freelancer
        fields = ['video_consultation']


class ChangeWorkTypeForm(forms.ModelForm):

    class Meta:
        model = Freelancer
        fields = ['work_type']

    work_type = forms.ModelMultipleChoiceField(
        queryset=Work_Type.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )


class ChangeWorkCategoryForm(forms.ModelForm):

    class Meta:
        model = Freelancer
        fields = ['work_category', 'lessons']

    work_category = forms.ModelMultipleChoiceField(
        queryset=Work_Category.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )

    lessons = forms.ModelMultipleChoiceField(
        queryset=Lesson.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )


class ChangeLanguagesForm(forms.ModelForm):

    class Meta:
        model = Freelancer
        fields = ['languages']

    languages = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )


class CreateUserForm(UserCreationForm):
    user_type = forms.ChoiceField(
        choices=USER_TYEPS, widget=forms.RadioSelect())

    class Meta:
        model = User
        fields = ['username', 'user_type', 'email', 'password1', 'password2']


class AcceptedOrderForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'qualification__textarea', "rows": 30, "cols": 30, 'placeholder': 'Descripția'}), label='')
    files = forms.FileField(
        widget=forms.FileInput(attrs={'': ''}), label='', required=False)

    class Meta:
        model = AcceptedOrder
        fields = '__all__'
        exclude = ['user', 'freelancer', 'order',
                   'completed', 'delivered_date', 'paied']


class FeedbackForm(forms.ModelForm):
    rating = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'review-profile__star fa fa-star fa-2x'}))

    class Meta:
        model = Feedback
        fields = '__all__'
        exclude = ['accepted_order']


class OrderForm(forms.ModelForm):
    premium = forms.BooleanField(
        label='Premium', initial=False, required=False)
    files = forms.FileField(widget=forms.FileInput(), required=False)

    class Meta:
        model = Order
        fields = ['limit_date', 'title', 'short_description', 'description', 'files',
                  'min_size', 'max_size', 'price', 'premium', 'work_type', 'lessons']
