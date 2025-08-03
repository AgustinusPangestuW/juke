from odoo import models, fields, api, _
from odoo.exceptions import UserError

class InheritStockMove(models.Model):
    _inherit = 'stock.move'

    mobile_service_request_id = fields.Many2one('mobile_service.service_request', string='Service Request', tracking=True, ondelete='cascade')


class InheritStockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    mobile_service_request_id = fields.Many2one('mobile_service.service_request', string='Mobile Service Request', ondelete='cascade')
    mobile_service_request_line_id = fields.Many2one('mobile_service.service_request_parts', string='Mobile Service Request Parts', ondelete='cascade')