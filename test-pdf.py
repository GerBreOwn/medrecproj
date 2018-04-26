#!/usr/bin/python3
from reportlab.lib.pagesizes import HALF_LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Image, Paragraph, Table
from datetime import date
from django.db import models
from django.db import connection
from models import Patient, Visit, Doctor

def __init__(self, connection):
        self.connection = connection

patient = Patient.objects.all( 
#select visit_date,  visit_dose.dose_name AS dose_name
#,  concat(patient_patient.last_name, " ",patient_patient.first_name) as full_name
#,  patient_patient.middle_initial AS middle_initial
#,  timestampdiff(year,patient_patient.date_of_birth, curdate()) AS age
#,  patient_patient.gender AS gender
#,  visit_prescription.medicine_quantity AS medicine_quantity
#,  visit_reminder.medicine_reminder AS medicine_reminder
#,  visit_medicine.brand_name AS brand_name
#,  visit_medicine.generic_name AS generic_name 
#from 
#(((((visit_prescription  
#join visit_visit  
#on 
#(visit_prescription.visit_id = visit_visit.id)) 
 
#join patient_patient  
#on (visit_visit.patient_id = patient_patient.id))  
#join visit_dose  
#on (visit_prescription.medicine_dose_id = visit_dose.id))
#join visit_reminder  
#on (visit_prescription.medicine_reminder_id = visit_reminder.id))  
#join visit_medicine  
#on (visit_prescription.medicine_id = visit_medicine.id)) 
#where visit_visit.visit_date = curdate()  
#and 
#visit_visit.patient_id = @id

        
dt = curdate()

c = canvas.Canvas("testform.pdf", pagesize=HALF_LETTER)
c.setLineWidth(.3)
c.setFont('Helvetica', 14)

c.setPageSize((396,612))

c.drawString(40, 560, 'SIMON JOHN ERIC T. FLORES, M.D., DPBO-HNS')

c.setFont('Helvetica', 11)
c.drawString(60,540, 'Diplomate - Ears, Nose, Throat - Head and Neck Surgery')

c.drawString(36,510,'SUMC')
c.setFont('Helvetica', 9)
c.drawString(36,500,'Mon. - Fri.:   10:00 A.M. - 12:00 NN')
c.drawString(36,490,'                      2:00 P.M. -  4:00 P.M.')
c.drawString(36,480, 'Saturday  :   10:00 A.M. - 12:00 NN')
c.drawString(36,470, 'Tel. No.    :   420-2217')

c.setFont('Helvetica', 10)
c.drawString(265,490,'HOSPITAL AFFILIATIONS:')
c.drawString(265,480,'NOPH')
c.drawString(265,470,'Holy Child Hospital')

c.line(35,463,378,463)
c.line(35,461,378,461)

c.setFont('Helvetica', 10)
c.drawString(36,440,'Patient')
c.drawString(74,442,'%s' % fullname)
c.drawString(270,440,'Age')
c.drawString(292,442,'%s' % age)
c.drawString(330,440,'Sex')
c.drawString(352,442,'%s' % gender)

c.drawString(36, 420, 'Address')
c.drawString(77, 422, '%s' %  address )
c.drawString(270, 420, 'Date')
c.drawString(303, 422, '%s' % dt)

c.line(72,440,266,440)
c.line(290,440,325,440)
c.line(350,440,378,440)
c.line(72,420,266,420)
c.line(300,420,378,420)

# But first to put in the logo
logo = Image("images.png")
logo.drawHeight = 1*inch
logo.drawWidth = 1*inch
#c.logo.wrap((c,72, 72))
#c.logo.drawOn(36,390)
#c.drawImage(logo, 360,390)

# Now to enter some medicines!!!
pres1 = "Medicine1  20mg  #30 "
c.drawString(72, 396, "%s" % pres1)

# Below is the code for the footer.
c.line(252,54,342,54)
c.drawString(344,55,'M.D.')
c.drawString(252, 43, 'Lic.No.: 0092579')
c.drawString(252, 31, 'PTR No.:')
c.line(292, 31, 360,31)
c.drawString(252,19, 'S2 No.:')
c.line(288, 19,360,19)

c.save()
