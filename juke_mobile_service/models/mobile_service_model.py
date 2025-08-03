from odoo import models, fields


class Model(models.Model):
    _name = 'mobile_service.model'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Mobile Model'
    _order = 'create_date desc'

    name = fields.Char(string='Model Name', required=True, tracking=True)
    brand_id = fields.Many2one('mobile_service.brand', string='Mobile Brand', cascade='ondelete', tracking=True)
    active = fields.Boolean(string='Active', default=True, tracking=True)