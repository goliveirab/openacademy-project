from openerp import models, fields

'''
Module: To create Course model
'''


class Course(models.Model):
    '''
    Class: Create the Course model
    '''

    _name = 'openacademy.course'

    name           = fields.Char(string="Title", required=True)
    description    = fields.Text(strin="Description")
    responsible_id = fields.Many2one('res.users',
                                      ondelete='set null',
                                      string='Responsible',
                                      index=True)
    session_ids    = fields.One2many('openacademy.session',
                                     'course_id',
                                      string="Sessions") 
