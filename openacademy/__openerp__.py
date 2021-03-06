# -*- coding: utf-8 -*-
{
    'name': "Open Academy",

    'summary': """Manage trainings""",

    # 'description': """
    # Open Academy module for managing trainings:
    # - training courses
    # - training sessions
    # - attendees registration

    'author': "Vauxoo",
    'website': "http://www.vauxoo.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'board', 'account_asset'],

    # always loaded
    'data': [
        'security/openacademy_security.xml',
        'security/ir.model.access.csv',
        'view/openacademy_course_view.xml',
        'view/openacademy_session_view.xml',
        'view/openacademy_partner_view.xml',
        'workflow/openacademy_session_workflow.xml',
        'report/openacademy_session_report.xml',
        'view/openacademy_session_board.xml',
        'view/openacademy_account_asset_view.xml',
        # 'security/ir.model.access.csv',
        # 'templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True
}
