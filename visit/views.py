from reportlab.lib.pagesizes import HALF_LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Image, Paragraph, Table
from datetime import date
from django.db import models
from django.db import connection
from models import Patient, Visit, Doctor
from django.shortcuts import render
from reportlab.lib.pagesizes import HALF_LETTER, letter

class PresPDF:
	def __init__(self, buffer, pagesize):
		self.buffer = buffer
