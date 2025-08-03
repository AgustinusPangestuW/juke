from odoo import models, fields


class ComplaintTemplate(models.Model):
    _name = 'mobile_service.complaint_template'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Complaint Templates'
    _order = 'create_date desc'

    name = fields.Char(string='Complaint Description', required=True, tracking=True)
    complaint_type_id = fields.Many2one('mobile_service.complaint_type', string='Complaint Type', tracking=True)
    active = fields.Boolean(string='Active', default=True, tracking=True)