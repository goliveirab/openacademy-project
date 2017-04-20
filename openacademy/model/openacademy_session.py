# --*-- utf-8 --*--
from openerp import fields, models

'''
Create session model
'''


class Session(models.Model):
    '''
    Create a session for a course
    '''

    _name = 'openacademy.session'

    name = fields.Char(required=True)
    start_date = fields.Date()
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
