from odoo import api, fields, models, http, _
from odoo.exceptions import UserError, ValidationError

class MobileServiceWizard(models.TransientModel):
    _name = 'mobile_service.assign_wizard'
    _description = 'Mobile Service Assign Wizard'
        
    service_request_id = fields.Many2one('mobile_service.service_request', string='Service Request')
    technician_id = fields.Many2one('res.users', string='Technician Name')
    allowed_technicians = fields.Many2many(
        comodel_name='res.users', 
        string='Allowed Techicians',
        store=True)
    
    def _compute_allowed_technicians(self):
        for rec in self:
            allowed_technicians = self.env['res.users'].search([('has_group', '=', 'juke_mobile_service.group_mobile_service_technician')])
            if allowed_technicians:
                rec.allowed_technicians = [(4, id) for id in allowed_technicians.ids]

    def add_technician(self):
        if not self.service_request_id:
            raise UserError("No Service Request Selected")
        self.service_request_id.write(
        {
            'state': 'assigned',
            'technician_id': self.technician_id.id
        })