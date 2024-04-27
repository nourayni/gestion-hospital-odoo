# -*- coding: utf-8 -*-
# from cgi import maxlen

from odoo import models, fields, api
from datetime import datetime


class Patient(models.Model):
    _name = "hospital.patient"
    _description = "patient model"
    ###############
    firstname = fields.Char( required=True, string='prenom du patient')
    lastname = fields.Char( required=True, string='nom du patient')
    address = fields.Char( required=True, string='adresse du patient')
    date_of_birth = fields.Date(string='date de naissance', required=True)
    group_sanguin = fields.Char(string='groupe sanguin')
    ''' age compute from date of birth'''
    age = fields.Integer(string='age', compute='_compute_age')
    allergie = fields.Char(string='allergie')

    genre = fields.Selection([
        ('male', 'Homme'),
        ('female', 'Femme'),
        ('other', 'Autre')
    ], string='Genre', required=True, default='male')

    consultation_ids = fields.One2many('hospital.consultation',
                                       'patient_id')
    dossier_medical_id = fields.One2many('hospital.medical',
                                         'patient_id', 'dossier medical')
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', 'rendez vous')

    @api.depends('date_of_birth')
    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                birth_day = datetime.combine(record.date_of_birth, datetime.min.time())
                today = datetime.today()
                age = today.year - birth_day.year
                record.age = age
            else:
                record.age = 0


class Medecin(models.Model):
    _name = "hospital.medecin"
    _description = "medecin model"

    matricule = fields.Char(string='matricule')
    specialite = fields.Char(string='specialite')
    phone_number = fields.Char(string='numero de telephone')
    first_name = fields.Char(string='prenom', required=True)
    last_name = fields.Char(string='nom', required=True)
    service_id = fields.Many2one('hospital.service', 'service')
    consultation_ids = fields.One2many('hospital.consultation',
                                       'medecin_id')


class Consultation(models.Model):
    _name = "hospital.consultation"
    _description = 'hospital consultation'
    date_consultation = fields.Datetime(string='date consultation',
                                        required=True, default=fields.Datetime.now)
    diagnostic = fields.Char(string='diagnostic')
    patient_id = fields.Many2one('hospital.patient', string='patient')
    medecin_id = fields.Many2one('hospital.medecin', string='medecin')


class DossierMedical(models.Model):
    _name = 'hospital.medical'
    _description = 'dossier medical'

    patient_id = fields.Many2one('hospital.patient', 'patient')
    prescription = fields.Char(string='prescription',)


class Appointment(models.Model):
    _name = 'hospital.appointment'
    _description = "Appointment"

    date_appointment = fields.Date()
    patient_id = fields.Many2one('hospital.patient', string='patient')
    rome = fields.Char(string='rome')


class Service(models.Model):
    _name = 'hospital.service'
    _description = 'services medical'

    service_name = fields.Char(string='nom du service', required=True)
    specialite = fields.Char(string='specialite', required=True)
    medecin_ids = fields.One2many('hospital.medecin',
                                  'service_id', string='medecins')

# class hospital(models.Model):
#     _name = 'hospital.hospital'
#     _description = 'hospital.hospital'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
