# --*-- utf-8 --*--
from openerp import api, fields, models

'''
Create session model
'''


class Session(models.Model):
    '''
    Create a session for a course
    '''

    _name = 'openacademy.session'

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    instructor_id = fields.Many2one('res.partner',
                                    string="Instructor",
                                    domain=["|",
                                            ("instructor", "=", True),
                                            ("category_id.name",
                                             "ilike", "Teacher")
                                            ])
    course_id = fields.Many2one('openacademy.course',
                                ondelete='cascade',
                                string="Course",
                                required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")
    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')
    active = fields.Boolean(default=True)

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        '''
        Calculate the taken seats %
        '''

        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats

    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        '''
        Check seat value
        '''

        if self.seats < 0:
            return {
                'warning': {
                    'title': 'Incorrect seats value',
                    'message': 'Available seats may not be negative',
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': 'Too many attenddes',
                    'message': 'Increase seats or remove excess attendees',
                },
            }
