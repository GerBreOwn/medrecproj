from django.contrib import admin
from djangoql.admin import DjangoQLSearchMixin

admin.site.site_title = 'Medical Records Administration'
admin.site.site_header = 'Medical Records Doctor Administration'
# Register your models here.

from .models import Doctor # , Hospital, DrOfficeHour

# def register_hidden_models(*model_names):
    # for m in model_names:
        # ma = type(
            # str(m)+'Admin',
            # (admin.ModelAdmin,),
            # {
                # 'get_model_perms': lambda self, request: {}
            # })
        # admin.site.register(m, ma)

# register_hidden_models(mymodels)

@admin.register(Doctor)
#@admin.register(Hospital)
#@admin.register(DrOfficeHour)

class DoctorAdmin(admin.ModelAdmin):
	pass
	#list_display = ('first_name', 'last_name', 'suffix',  'telephone', 'lic_no', 'ptr_no','s2_no')#'dr_off_hour',
	#fields = [('first_name', 'last_name', 'suffix'), ('telephone'), ('lic_no', 'ptr_no', 's2_no')] #'dr_off_hour',

# class OfficeHourAdmin(admin.ModelAdmin):
	# list_display = ('hours_am', 'hours_pm')
	# fields = [('hours_am'), ('hours_pm')]

# class HospitalAdmin(admin.ModelAdmin):
	# list_display = ('hosp_name', 'hosp_addr', 'hosp_city')
