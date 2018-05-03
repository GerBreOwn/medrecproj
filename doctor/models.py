from django.db import models
from crum import get_current_user
from django.contrib import admin
from patient.models import Town
# Create your models here.

class CommonInfo(models.Model):
	is_active = models.BooleanField(default = True, editable = False)
	created_on = models.DateTimeField(auto_now_add = True, editable = False)
	created_by = models.ForeignKey('auth.User', blank=True, null=True, editable = False, default = None, on_delete=models.SET_DEFAULT, related_name = "+")
	modified_on = models.DateTimeField(auto_now = True)
	modified_by = models.ForeignKey('auth.User', blank = True, null = True, default = None, editable = False, on_delete=models.DO_NOTHING, related_name = '+')
	#counter = models.IntegerField(blank = True, null = True, default = None, editable = False)

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
		#ordering = ['-counter',]
		abstract = True

class Doctor(CommonInfo):
	id = models.AutoField(primary_key = True)
	first_name = models.CharField(max_length = 25, blank = False, null = False, default = " ")
	last_name = models.CharField(max_length = 20, blank = False, null = False, default = " ")
	suffix = models.CharField(max_length = 55, blank = False, null = False, default = "M.D.")
	telephone = models.CharField(max_length = 12, blank = True, null = True)
	lic_no = models.CharField(max_length = 25, blank = True, null = True)
	ptr_no = models.CharField(max_length = 25, blank = True, null = True)
	s2_no = models.CharField(max_length = 25, blank = True, null = True)


	def get_absolute_url(self):
		return reverse('doctor-detail', args=[str(self.id)])

	def __str__(self):
		return '%s %s' % (self.first_name, self.last_name)

# class Hospital(CommonInfo):
	# id = models.AutoField(primary_key = True)
	# hosp_name = models.CharField(max_length = 50, blank = True, null = True)
	# hosp_addr = models.CharField(max_length = 50, blank = True, null = True)
	# hosp_city = models.ForeignKey('patient.Town', on_delete = models.CASCADE, default = 1)

	# def get_absolute_url(self):
		# return reverse('hospital_affiliat-detail', args=[str(self.id)])

	# def __str__(self):
		# return '%s' % (self.hosp_name)


# class DrOfficeHour(CommonInfo):
	# id = models.AutoField(primary_key = True)
	# days = models.CharField(max_length = 20, blank = True, null = True)
	# hours_am = models.CharField(max_length = 20, blank = True, null = True)
	# hours_pm = models.CharField(max_length = 20, blank = True, null = True)

	# def get_absolute_url(self):
		# return reverse('officehour-detail', args=[str(self.id)])

	# def __str__(self):
		# return '%s %s %s' % (self.days, self.hours_am, self.hours_pm)
		# return '%s, %s %s' % (self.days, self.hours_am, self.hours_pm)


