from odoo import models, fields, api


class InheritProductTemplate(models.Model):
    _inherit = 'product.template'

    is_part_inventory = fields.Boolean(string='Is Part Inventory', default=False, tracking=True)
    brand_id = fields.Many2one('mobile_service.brand', string='Brand', tracking=True)
    model_id = fields.Many2one('mobile_service.model', string='Model', tracking=True)
    mobile_service_color = fields.Char(string='Color', tracking=True)
    note = fields.Text(string='Note', tracking=True)