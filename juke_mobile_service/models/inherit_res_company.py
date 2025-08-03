from odoo import models, fields, api, _
from odoo.exceptions import UserError

class InheritResCompany(models.Model):
    _inherit = 'res.company'

    product_service_charge = fields.Many2one('product.product', string='Product Service Charge', tracking=True)

    