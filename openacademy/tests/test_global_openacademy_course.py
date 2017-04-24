# -*- encoding: utf-8 -*-
from openerp.tests.common import TransactionCase


class GlobalTestOpenAcademyCourse(TransactionCase):

    '''
    setUp seudo-contructor method
    ''' 
    def setUp(selft):
        '''
        Define flobal variables for test methos
	'''
	super(GlobalTestOpenAcademyCourse, self).setUp()
	self.variable = "hello world"
        self.course = self.env['openacademy_course']

    '''
    Class methods
    '''
    def create_course(self, 
		      course_name, 
                      course_description,
                      course_responsible_id):
	course_id = self.course.create({
		'name': course_name,
		'description': course_description,
                'responsible_id': course_responsible_id
	})
	return course_id

    '''
    Test method
    begin with: def test_*(self):
    executed by number
    '''
    def test_01_course_same_name_and_description(self):
	'''
        Create a course with same name and description
        Test description does not contain the name 
        '''
	self.create_course('test', 'test', None)
        
