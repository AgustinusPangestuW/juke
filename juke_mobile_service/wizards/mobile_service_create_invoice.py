from odoo import api, fields, models, http, _
from odoo.exceptions import UserError, ValidationError

class MobileServiceCreateInvoiceWizard(models.TransientModel):
    _name = 'mobile_service.create_invoice_wizard'
    _description = 'Mobile Service Create Invoice Wizard'
        
    method = fields.Selection([("advance","Advance Amount"),("full","Full Amount")], string='Invoice Method', default="advance", required=True)
    amount = fields.Float(string='Amount', required=True)
    mobile_service_id = fields.Many2one('mobile_service.service_request', string='Mobile Service Request', required=True)
    
    def create_invoice(self):
        account_move_id = self.env['account.move'].create({
            'invoice_date': fields.Date.today(),
            'invoice_date_due': fields.Date.today(),
            'partner_id': self.mobile_service_id.customer_id.id,
            'invoice_line_ids': [(0,0,{
                'product_id':i.product_id.id, 
                'quantity': 1, 
                'price_unit': i.price,
                'account_id': i.product_id.property_account_income_id.id,
                'uom_id': i.product_id.uom_id.id,
                'name': i.product_id.name
            }) for i in self.mobile_service_id.service_part_ids],
            'mobile_service_request_id': self.mobile_service_id.id
        })
        