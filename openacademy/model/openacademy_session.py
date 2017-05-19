# --*-- utf-8 --*--
'''
Create session model
'''
from datetime import timedelta
from openerp import api, exceptions, fields, models, _


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
    end_date = fields.Date(string="End Date", store=True,
                           compute='_get_end_date', inverse='_set_end_date')

    active = fields.Boolean(default=True)
    hours = fields.Float(string="Duration in hours",
                         compute="_get_hours", inverse="_set_hours")
    attendees_count = fields.Integer(string="Attendees count",
                                     compute='_get_attendees_count',
                                     store=True)
    color = fields.Integer()
    state = fields.Selection([
        ('draft', "Draft"),
        ('confirmed', "Confirmed"),
        ('done', "Done"),
    ])
    material_ids = fields.Many2many('account.asset.asset', string="Materials")

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_confirm(self):
        self.state = 'confirmed'

    @api.multi
    def action_done(self):
        self.state = 'done'

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
                    'title': _('Incorrect seats value'),
                    'message': _('Available seats may not be negative'),
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': _('Too many attenddes'),
                    'message': _('Increase seats or remove excess attendees'),
                },
            }

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue
            # Add duration to start_date, but: Monday + 5 days = Saturday, so
            # subtract one second to get on Friday instead
            start = fields.Datetime.from_string(r.start_date)
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = start + duration

    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue
            # Compute the difference between dates,
            # but: Friday - Monday = 4 days,
            # so add one day to get 5 days instead
            start_date = fields.Datetime.from_string(r.start_date)
            end_date = fields.Datetime.from_string(r.end_date)
            r.duration = (end_date - start_date).days + 1

    @api.depends('duration')
    def _get_hours(self):
        # Get duration hours acording to working hours
        for r in self:
            r.hours = r.duration * 8

    def _set_hours(self):
        # Set duration hours acording to working hours
        for r in self:
            r.duration = r.hours / 8

    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for r in self:
            r.attendees_count = len(r.attendee_ids)

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        '''
        Check instructor not in attendees
        list
        '''

        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise exceptions.ValidationError(_("A session's instructor" +
                                                 " can't be an attendee"))

    @api.multi
    def copy(self, default=None):
        '''
        Handle sql constraint: unique session name
        '''
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', _(u'Copy of {}%').format(self.name))])
        if not copied_count:
            new_name = _(u'Copy of {}').format(self.name)
        else:
            new_name = _(u'Copy of {} ({})').format(self.name, copied_count)

        default['name'] = new_name
        return super(Session, self).copy(default)

    _sql_constraints = [
        ('name_session_unique',
         'UNIQUE(name)',
         'The session name must be unique'),
    ]
