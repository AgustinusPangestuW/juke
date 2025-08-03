from odoo import models, fields


class Brand(models.Model):
    _name = 'mobile_service.brand'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Mobile Brand'
    _order = 'create_date desc'

    name = fields.Char(string='Mobile Brand', required=True, tracking=True)
    active = fields.Boolean(string='Active', default=True, tracking=True)