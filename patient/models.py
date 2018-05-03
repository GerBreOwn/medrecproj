from django.db import models
from django.db import connection
from django.db.models import F
from django.db.models import signals
from django.contrib.auth.models import User
from django.utils import timezone
from django.apps import AppConfig
#from django.urls import reverse
import datetime
from crum import get_current_user
from django.contrib import admin
from versatileimagefield.fields import VersatileImageField

class CommonInfo(models.Model):
    is_active = models.BooleanField(default = True, editable = False)
    created_on = models.DateTimeField(auto_now_add = True, editable = False)
    created_by = models.ForeignKey('auth.User', blank=True, null=True, default = None,editable = False, on_delete=models.SET_DEFAULT, related_name = "+")
    modified_on = models.DateTimeField(auto_now = True, editable = False)
    modified_by = models.ForeignKey('auth.User', blank = True, null = True, default = None, editable = False, on_delete=models.SET_DEFAULT, related_name = '+')

    def get_model_perms(self, *args, **kwargs):
        perms = admin.ModelAdmin.get_model_perms(self, *args, **kwargs)
        perms['list_hide'] = True
        return perms

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(CommonInfo, self).save(*args, **kwargs)

    class Meta:
       abstract = True

class Occupation(CommonInfo):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank = True, null = True, unique = True)
    #counter = CounterField()

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('occup-detail', args=[str(self.id)])

    def __str__(self):
        return '%s' % (self.name)

class Patient(CommonInfo):
    id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=25, db_index = True)
    first_name = models.CharField(max_length=25, db_index = True)
    middle_initial = models.CharField(max_length=1, blank=True, null=True)
    contact_num = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    town = models.ForeignKey('Town', default = None, on_delete=models.SET_DEFAULT)
    date_of_birth = models.DateField(("Date of birth"), default=datetime.date.today)
    pat_pic = VersatileImageField('Pat_Pic', upload_to='images/' ,blank=True, null=True)
    occupation = models.ForeignKey('Occupation', blank=True, null=True, default = None, on_delete=models.SET_DEFAULT)
    email = models.EmailField(blank=True, null=True)

    GENDER = (('F', 'Female'),('M', 'Male'),)
    gender = models.CharField(max_length=1, choices=GENDER,  default = 'F', help_text = 'Select Gender')

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('patient-detail', args=[str(pat.id)])

    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)

class Province(CommonInfo):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    #counter = CounterField()
    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('province-detail', args=[str(self.id)])

    def __str__(self):
        return '%s' % (self.name)

class Town(CommonInfo):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25, blank = False, null = False, unique = True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    prov = models.ForeignKey('Province', default = None,  on_delete=models.SET_DEFAULT)

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('town-detail', args=[str(self.id)])

    def __str__(self):
        return '%s' % (self.name)

class Image(models.Model):
	name = models.CharField(max_length=500)
	picfile = models.ImageField(upload_to = 'images/', null = True, blank = True, verbose_name = "")

	def __str__(self):
		return self.name + ": " + str(self.imagefile)

def pat_count(self, obj):
	return obj.self.patient__set.count()
