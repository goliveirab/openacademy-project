# -*- encoding: utf-8 -*-
from psycopg2 import IntegrityError
from openerp.tests.common import TransactionCase
from openerp.tools import mute_logger


class GlobalTestOpenAcademyCourse(TransactionCase):

    '''
    setUp seudo-contructor method
    '''
    def setUp(self):
        '''
        Define flobal variables for test methos
        '''
        super(GlobalTestOpenAcademyCourse, self).setUp()
        self.course = self.env['openacademy.course']

    '''
    Class methods
    '''
    def create_course(self, course_name,
                      course_description,
                      course_responsible_id):
        course_id = self.course.create({
            'name': course_name,
            'description': course_description,
            'responsible_id': course_responsible_id,
        })
        return course_id

    '''
    Test method
    begin with: def test_*(self):
    executed by number
    '''
    @mute_logger('openerp.sql_db')
    def test_10_course_same_name_and_description(self):
	'''
        Create a course with same name and description
        Test description does not contain the name
        '''
        with self.assertRaisesRegexp(
            IntegrityError,
            'new row for relation "openacademy_course" violates check'
            ' constraint "openacademy_course_name_description_check"'
        ):
            self.create_course('test', 'test', None)
    
    @mute_logger('openerp.sql_db')
    def test_20_two_courses_with_same_name(self):
        '''
        Create two courses with the same name
        Raise name unique constraint
        '''
        new_id = self.create_course('test_name', 'test_description', None)
        print "new_id", new_id
        with self.assertRaisesRegexp(
            IntegrityError,
            'duplicate key value violates unique constraint'
            ' "openacademy_course_name_unique"'
        ):
            new_id2 = self.create_course('test_name', 'test_description', None)
            print "new_id2", new_id2

    def test_30_execute_duplicate_course(self):
        '''
        Test duplicate function
        '''
        course = self.env.ref('openacademy.course0')
        course_id = course.copy()
        print "course_id", course_id
