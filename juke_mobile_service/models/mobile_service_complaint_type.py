from odoo import models, fields


class ComplaintType(models.Model):
    _name = 'mobile_service.complaint_type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Complain Types'
    _order = 'create_date desc'

    name = fields.Char(string='Complaint Type', required=True, tracking=True)
    active = fields.Boolean(string='Active', default=True, tracking=True)