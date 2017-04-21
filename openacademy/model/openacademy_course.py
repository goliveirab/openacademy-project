from openerp import api, models, fields

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
    responsible_id = fields.Many2one('res.users',
                                     ondelete='set null',
                                     string='Responsible',
                                     index=True)
    session_ids = fields.One2many('openacademy.session',
                                  'course_id',
                                  string="Sessions")

    @api.multi
    def copy(self, default=None):
        '''
        Handle sql constraint: unique name
        '''
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u'Copy of {}%'.format(self.name))])    
        if not copied_count:
            new_name = u'Copy of {}'.format(self.name)
        else:
            new_name = u'Copy of {} ({})'.format(self.name, copied_count)

        default['name'] = new_name
        return super(Course, self).copy(default)

    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         'The title of the course should not be the description'),
        ('name_unique',
         'UNIQUE(name)',
         'The course title must be unique'),
    ]
