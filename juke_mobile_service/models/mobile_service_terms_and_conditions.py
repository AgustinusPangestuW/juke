from odoo import models, fields, api


class TermsConditions(models.Model):
    _name = 'mobile_service.terms_and_conditions'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Terms and Conditions'
    _order = 'create_date desc'
    _rec_name = 'terms_and_conditions'
    
    terms_and_conditions = fields.Text(string='Terms and Conditions', required=True, tracking=True)
    active = fields.Boolean(string='Active', default=True, tracking=True)