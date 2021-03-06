# -*- encoding: utf-8 -*-
from psycopg2 import IntegrityError
from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError
from openerp.tools import mute_logger


class GlobalTestOpenAcademySession(TransactionCase):
    '''
    Global tests form session
    '''

    def setUp(self):
        super(GlobalTestOpenAcademySession, self).setUp()
        self.session = self.env['openacademy.session']
        self.course = self.env.ref('openacademy.course1')
        self.partner_vauxoo = self.env.ref('base.res_partner_23')
        self.partner_attendee = self.env.ref('base.res_partner_5')

    def test_10_instructor_not_attendee(self):
        '''
        Raise an instructor can not be an
        attendee
        '''
        with self.assertRaisesRegexp(
            ValidationError,
            "A session's instructor can't be an attendee"
        ):
            self.session.create({
                'name': 'Session test 1',
                'seats': 1,
                'instructor_id': self.partner_vauxoo.id,
                'attendee_ids': [(6, 0, [self.partner_vauxoo.id])],
                'course_id': self.course.id,
            })

    def test_20_workflow_done(self):
        '''
        Check workflow works fine
        '''
        session_test = self.session.create({
            'name': 'Session test 1',
            'seats': 50,
            'instructor_id': self.partner_vauxoo.id,
            'attendee_ids': [(6, 0, [self.partner_attendee.id])],
            'course_id': self.course.id,
        })
        # Check initial state
        self.assertEqual(session_test.state, 'draft', 'Initial state'
                         ' should be Draft')
        # Change next state and check it
        session_test.signal_workflow('button_confirm')
        self.assertEqual(session_test.state, 'confirmed', 'Signal confirm'
                         ' do not work')
        # Change next state and check it
        session_test.signal_workflow('button_done')
        self.assertEqual(session_test.state, 'done', 'Signal done do not'
                         ' work')

    @mute_logger('openerp.sql_db')
    def test_30_two_sessions_with_same_name(self):
        '''
        Create two sessions with the same name
        Raise name unique constraint
        '''
        self.session.create({
            'name': 'Session test 1',
            'seats': 50,
            'instructor_id': self.partner_vauxoo.id,
            'attendee_ids': [(6, 0, [self.partner_attendee.id])],
            'course_id': self.course.id,
        })
        with self.assertRaisesRegexp(
            IntegrityError,
            'duplicate key value violates unique'
            ' constraint "openacademy_session_name_session_unique'
        ):
            self.session.create({
                'name': 'Session test 1',
                'seats': 50,
                'instructor_id': self.partner_vauxoo.id,
                'attendee_ids': [(6, 0, [self.partner_attendee.id])],
                'course_id': self.course.id,
            })
