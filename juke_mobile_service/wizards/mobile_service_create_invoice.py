from odoo import api, fields, models, http, _


class MobileServiceCreateInvoiceWizard(models.TransientModel):
    _name = 'mobile_service.create_invoice_wizard'
    _description = 'Mobile Service Create Invoice Wizard'
        
    method = fields.Selection([("advance","Advance Amount"),("full","Full Amount")], string='Invoice Method', default="advance", required=True)
    amount = fields.Float(string='Amount', required=True)
    service_request_id = fields.Many2one('mobile_service.service_request', string='Mobile Service Request', required=True)
    
    def create_invoice(self):
        def get_product_service():
            service_charge = False
            try:
                service_charge = self.env.company.product_service_charge or self.env.ref('juke_mobile_service.product_product_service_charge')
            except:
                pass
            if not service_charge:
                return []
            return [(0, 0, {
                'product_id': service_charge.id,
                'quantity': 1,
                'price_unit': self.amount,
                'tax_ids': [(6, 0, service_charge.taxes_id.ids)] if service_charge.taxes_id else [],
                'mobile_service_request_id': self.service_request_id.id,
            })]

        def get_lines():
            return [(0, 0, {
                'product_id': i.product_id.id,
                'quantity': 1,
                'price_unit': i.price,
                # 'account_id': i.product_id.property_account_income_id.id,
                # 'uom_id': i.product_id.uom_id.id,
                # 'name': i.product_id.display_name,
                'tax_ids': [(6, 0, i.product_id.taxes_id.ids)] if i.product_id.taxes_id else [],
                'mobile_service_request_line_id': i.id,
                'mobile_service_request_id': self.service_request_id.id
            }) for i in self.service_request_id.service_part_ids]

        line_ids = get_product_service() + get_lines()
        acc_move_id = self.env['account.move'].sudo().create({
            'invoice_date': fields.Date.today(),
            'invoice_date_due': fields.Date.today(),
            'move_type': 'out_invoice',
            'partner_id': self.service_request_id.customer_id.id,
            'mobile_service_request_id': self.service_request_id.id,
            'invoice_line_ids': line_ids
        })
