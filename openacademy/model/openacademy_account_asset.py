# -*- coding: utf-8 -*-
'''
openacademy Account Asset module
'''

from openerp import fields, models


class AccountAsset(models.Model):
    '''
    Account Asset class
    '''

    _inherit = 'account.asset.asset'

    # Add a sessions into account.asset.asset to display how many
    # times the asset has been used
    session_ids = fields.Many2many('openacademy.session',
                                   readonly=True)
