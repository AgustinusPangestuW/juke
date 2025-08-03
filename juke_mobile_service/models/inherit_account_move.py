from odoo import models, fields, api, _
from odoo.exceptions import UserError

class InheritAccountMove(models.Model):
    _inherit = 'account.move'

    mobile_service_request_id = fields.Many2one('mobile_service.service_request', string='Mobile Service Request', tracking=True)


class InheritAccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    mobile_service_request_id = fields.Many2one('mobile.service.service_request', string='Mobile Service Request')
    mobile_service_request_line_id = fields.Many2one('mobile_service.service_request_parts', string='Mobile Service Request Parts')