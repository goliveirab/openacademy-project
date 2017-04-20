from openerp import models, fields

'''
Module: To create Course model
'''


class Course(models.Model):
    '''
    Class: Create the Course model
    '''

    _name = 'openacademy.course'

    name = fields.Char(string="Title", required=True)
    description = fields.Text(strin="Description")
