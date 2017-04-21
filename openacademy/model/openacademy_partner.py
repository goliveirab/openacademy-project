# -*- coding: utf-8 -*-
from openerp import fields, models

'''
openacademy Partner module
'''


class Partner(models.Model):
    '''
    Partner class
    '''

    _inherit = 'res.partner'

    # Add a new column to the res.partner model, by default partners are not
    # instructors
    instructor = fields.Boolean("Instructor", default=False)
    instructed_session_id = fields.One2many('openacademy.session',
                                            'instructor_id',
                                            string="Sessions as Instructor")
    session_ids = fields.Many2many('openacademy.session',
                                   string="Attended Sessions",
                                   readonly=True)
