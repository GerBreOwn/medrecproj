from django.db import models
from django.db import connection
from django.db.models import F
from django.db.models import signals
from django.contrib.auth.models import User
from django.utils import timezone
from django.apps import AppConfig
import datetime
from crum import get_current_user
from django.contrib import admin
from patient.models import Patient
from doctor.models import Doctor

class CommonInfo(models.Model):
    is_active = models.BooleanField(default = True, editable = False)
    created_on = models.DateTimeField(auto_now_add = True, editable = False)
    created_by = models.ForeignKey('auth.User', blank=True, null=True, editable = False, default = None, on_delete=models.SET_DEFAULT, related_name = "+")
    modified_on = models.DateTimeField(auto_now = True)
    modified_by = models.ForeignKey('auth.User', blank = True, null = True, default = None, editable = False, on_delete=models.SET_DEFAULT)
    #counter = models.IntegerField(blank = True, null = True, default = None, editable = False)

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

    def count_changes(self):
        with connection.cursor() as cursor:
            cursor.execute("update self set counter =+ 1 where self.id = %s", [self.pk])


    class Meta:
        #ordering = [ ]
        abstract = True


class Biopsy(CommonInfo):
    id = models.AutoField(primary_key=True)
    biopsy_name = models.ManyToManyField('BiopsyName',blank = True)
    biopsy_location = models.ManyToManyField('Location', blank = True)
    biopsy_result = models.ManyToManyField('BiopsyResult', blank = True)
    biopsy_text = models.TextField(blank = True, null = True)
    visit = models.ForeignKey('Visit', blank = True, null = True, editable = False, on_delete=models.SET_NULL)

    def get_absolute_url(self):
        return reverse('biopsy-detail', args=[str(self.id)])

    class meta:
        app_label = 'Biopsy'
        #ordering = [ 'biopsy_name', '-counter']

    def __str__(self):
        return '%s' % (self.biopsy_name)

class BiopsyName(CommonInfo):
    id = models.AutoField(primary_key=True)
    biopsy_name = models.CharField(max_length=25, unique = True)

    class meta:
        app_label = 'BiopsyName'
        #ordering = [  'biopsy_name']
        verbose_name = "biopsies"

    def get_absolute_url(self):
        return reverse('biopsy-detail', args=[str(self.id)])

    def __str__(self):
        return '%s' % (self.biopsy_name)


class BiopsyResult(CommonInfo):
    id = models.AutoField(primary_key=True)
    biopsy_result = models.CharField(max_length=25, unique = True)

    class Meta:
        ordering = ['biopsy_result']

    def get_absolute_url(self):
        return reverse('biopsyresult-detail', args=[str(self.id)])

    def __str__(self):
        return '%s' % (self.biopsy_result)

class ComplaintName(CommonInfo):
    id = models.AutoField(primary_key=True)
    complaint_name = models.CharField(max_length=255, unique = True)
    
    # def __str__(self):
        # return '%s' % (self.complaint_name)

    class meta:
        ordering = ["complaint_name",]

    def get_absolute_url(self):
        return reverse('complaintname-detail', args=[str(self.id)])

class Complaint(CommonInfo):
    id = models.AutoField(primary_key=True)
    complaint_name = models.ManyToManyField('ComplaintName')
    complaint_location = models.ManyToManyField('Location')
    finding = models.ManyToManyField('Finding')
    treatment = models.ManyToManyField('Treatment')
    visit = models.ForeignKey('Visit', editable = False,
    on_delete=models.PROTECT, default = 1)

    def get_absolute_url(self):
        return reverse('complaint-detail', args=[str(self.id)])

    def __str__(self):
        return '%s' % (self.complaint_name)

    class meta:
        ordering = [  'complaint_name',]

class Dose(CommonInfo):
    id = models.AutoField(primary_key=True)
    dose_name = models.CharField(max_length=25, unique = True)

    class Meta:
        ordering = ['dose_name']

    def get_absolute_url(self):
        return reverse('dose-detail', args=[str(self.id)])

    def __str__(self):
        return '%s' % (self.dose_name)

#class Drawing(CommonInfo):
    #id = models.AutoField(primary_key=True)
    #patient = models.ForeignKey('Patient', models.DO_NOTHING, blank=True, null=True)
    #drawing_name = models.BinaryField(blank=True, null=True, unique = True)

    ##class Meta:
        ##ordering = [  'patient', 'drawing_name']

    #def get_absolute_url(self):
        #return reverse('drawing-detail', args=[str(self.id)])

    #def __str__(self):
        #return '%s, %s' % (self.dra_name, self.patient)

class ExamName(CommonInfo):
    id = models.AutoField(primary_key = True)
    exam_name = models.CharField(max_length = 25, unique = True,
    default = "")
    visit = models.ForeignKey('Visit', blank = True, null = True,
    editable = False, on_delete=models.SET_NULL, default = 1)

class Exam(CommonInfo):
    id = models.AutoField(primary_key = True)
    exam_name = models.ManyToManyField(ExamName)
    exam_date = models.DateField(blank=True, null=True)
    exam_type = models.ManyToManyField('ExamType')
    exam_result = models.ManyToManyField('ExamResult')
    exam_text = models.TextField(blank=True, null=True)
    visit = models.ForeignKey('Visit', null=True, editable = False, on_delete=models.SET_NULL)

    def get_absolute_url(self):
        return reverse('exam-detail', args=[str(self.id)])

    def __str__(self):
        return '%s, %s' % (self.exam_date, self.exam_name)

class ExamResult(CommonInfo):
    id = models.AutoField(primary_key=True)
    exam_result = models.CharField(max_length=25, unique = True,
    default = "")

    def get_absolute_url(self):
        return reverse('examresult-detail', args=[str(self.id)])

    def __str__(self):
        return '%s' % (self.exam_result)

class ExamType(CommonInfo):
    id = models.AutoField(primary_key=True)
    exam_type = models.CharField(max_length=25, unique = True, default
    = "")

    def get_absolute_url(self):
        return reverse('examtype-detail', args=[str(self.id)])

    def __str__(self):
        return '%s' % (self.exam_type)

class Finding(CommonInfo):
    id = models.AutoField(primary_key=True)
    finding_name = models.CharField(max_length=255, unique = True,
    default ="")
    visit = models.ForeignKey('Visit', blank = True, null = True, editable = False, on_delete=models.SET_NULL)

    class Meta:
        ordering = [  'finding_name']

    def get_absolute_url(self):
        return reverse('finding-detail', args=[str(self.id)])

    def __str__(self):
        return '%s' % (self.finding_name)

class Hearing(CommonInfo):
    id = models.AutoField(primary_key=True)
    hearing_test = models.ManyToManyField('HearingTest')
    hearing_result = models.ManyToManyField('HearingResult')
    hearing_text = models.TextField(blank=True, null=True)
    visit = models.ForeignKey('Visit', blank = True, null = True, editable = False, on_delete=models.SET_NULL)

class HearingTest(CommonInfo):
    id = models.AutoField(primary_key=True)
    hearing_name = models.CharField(max_length = 50, unique = True,
    default = "")

    class Meta:
        ordering = [  'hearing_name']

    def get_absolute_url(self):
        return reverse('hearing-detail', args=[str(self.id)])

    def __str__(self):
        return '%s' % (self.hearing_name)

class HearingResult(CommonInfo):
    id = models.AutoField(primary_key=True)
    hearing_result = models.CharField(max_length=25, unique = True)

    class Meta:
        ordering = [  'hearing_result']

    def __str__(self):
        return '%s' % (self.hearing_result)

class Location(CommonInfo):
    id = models.AutoField(primary_key = True)
    location = models.CharField(max_length = 25, unique = True)

    class Meta:
        ordering = [  'location']

    def get_absolute_url(self):
        return reverse('location-detail', args=[str(self.id)])

    def __str__(self):
        return '%s' % (self.location)

class Medicine(CommonInfo): #14
    id = models.AutoField(primary_key=True)
    brand_name = models.CharField(max_length=50, unique=True, default =
    "")
    generic_name = models.CharField(max_length = 50, unique = True,
    default = "")
    medicine_dose = models.ForeignKey('Dose', on_delete=models.PROTECT, default = "")
    medicine_reminder = models.ForeignKey('Reminder',
    on_delete=models.PROTECT, default = "")

    class Meta:
        ordering = [  'brand_name']

    def get_absolute_url(self):
        return reverse('medication-detail', args=[str(self.id)])

    def __str__(self):
        return '%s' % (self.brand_name)


class Prescription(CommonInfo):
    id = models.AutoField(primary_key=True)
    medicine = models.ForeignKey('Medicine', on_delete=models.PROTECT,
    default = "")
    medicine_quantity = models.IntegerField(default = 0)
    visit = models.ForeignKey('Visit', blank = True, null = True, editable = False, on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse('prescription-detail', args=[str(self.id)])

class Reminder(CommonInfo):
    id = models.AutoField(primary_key=True)
    prescription_reminder = models.CharField(max_length=50, unique =
    True, default ="")

    class Meta:
        ordering = [  'prescription_reminder']

    def get_absolute_url(self):
        return reverse('reminder-detail', args=[str(self.id)])

    def __str__(self):
        return '%s' % (self.prescription_reminder)


class Treatment(CommonInfo):
    id = models.AutoField(primary_key=True)
    treatment_name = models.CharField(max_length=255, unique = True,
    default = "" )
    visit = models.ForeignKey('Visit', blank = True, null = True, editable = False, on_delete=models.PROTECT)

    class Meta:
        ordering = ['treatment_name']

    def get_absolute_url(self):
        return reverse('treatment-detail', args=[str(self.id)])

    def __str__(self):
        return '%s' % (self.treatment_name)

class Visit(CommonInfo):
    id = models.AutoField(primary_key=True)
    #patient_prescpt = models.ForeignKey('patient.Patient',     on_delete=models.PROTECT)#, default=1)
    medicine = models.ForeignKey('Medicine', blank=True, null=True, on_delete=models.PROTECT)
    medicine_dose = models.ForeignKey('Dose', blank=True, null=True, on_delete=models.PROTECT)
    prescription_reminder = models.ForeignKey('Reminder', blank=True, null=True, on_delete=models.PROTECT)
    medicine_quantity = models.IntegerField(blank=True, null=True)
    visit = models.ForeignKey('Visit', blank = True, null = True, editable = False, on_delete=models.PROTECT)
    
    def get_absolute_url(self):
        return reverse('prescription-detail', args=[str(self.id)])

def visit_count(self, obj):
    return obj.visit__set.count()
