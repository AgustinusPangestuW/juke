# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ServiceRequest(models.Model):
    _name = 'mobile_service.service_request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Service Request'
    _order = 'create_date desc'

    name = fields.Char(string='Service Number', tracking=True)
    is_warranty = fields.Boolean(string='In Warranty', tracking=True)
    is_repair = fields.Boolean(string='Repair', tracking=True)
    customer_id = fields.Many2one('res.partner', string='Customer Name', required=True, tracking=True)
    contact_number = fields.Char(string='Contact Number', tracking=True)
    email = fields.Char(string='Email', tracking=True)
    address = fields.Char(string='Address', tracking=True)
    mobile_brand_id = fields.Many2one('mobile_service.brand',string='Mobile Brand', required=True)
    mobile_model_id = fields.Many2one('mobile_service.model',string='Mobile Model', required=True)
    requested_date = fields.Date(string='Requested Date', default=fields.Date.today(), required=True)
    return_date = fields.Date(string='Return Date', required=True)
    allowed_technicians = fields.Many2many('res.users', string='Allowed Techicians', compute="_compute_allowed_technicians")
    technician_id = fields.Many2one('res.users', string='Technician Name', tracking=True)
    imei = fields.Char(string='IMEI Number', tracking=True)
    warranty_no = fields.Char(string='Warranty No.', tracking=True)
    term_and_condition_id = fields.Many2one('mobile_service.terms_and_conditions', string='Terms and Conditions', tracking=True)
    notes = fields.Text(string='Internal Notes', tracking=True)
    complaint_ids = fields.One2many('mobile_service.service_request_complaint', 'service_id', string='Complaints', tracking=True)
    service_part_ids = fields.One2many('mobile_service.service_request_parts', 'service_id',string='Parts Usage', tracking=True)
    state = fields.Selection([
            ('draft', 'Draft'),
            ('assigned', 'Assigned'),
            ('completed', 'Completed'),
            ('returned', 'Returned'),
            ('not_solved', 'Not Solved'),
        ], string='Service Status', 
        default='draft', 
        tracking=True)
    invoice_ids = fields.Many2many(
        comodel_name='account.move', 
        string='Invoices',
        compute="_compute_invoice_ids")
    count_invoice = fields.Integer(string='Count Invoice', compute="_compute_invoice_ids")
    stock_move_ids = fields.Many2many(
        comodel_name='stock.move', 
        string='Stock Moves',
        compute="_compute_stock_move_ids")
    count_stock_move = fields.Integer(string='Count Stock Moves', compute="_compute_stock_move_ids")
    
    def _compute_stock_move_ids(self):
        for rec in self:
            stock_move_ids = self.env['stock.move'].search([('mobile_service_request_id', '=', rec.id)]).ids
            rec.stock_move_ids = [(4, id) for id in stock_move_ids]
            rec.count_stock_move = len(stock_move_ids)
    
    def _compute_invoice_ids(self):
        for rec in self:
            invoice_ids = self.env['account.move'].search([('mobile_service_request_id', '=', rec.id)]).ids
            rec.invoice_ids = [(4, id) for id in invoice_ids]
            rec.count_invoice = len(invoice_ids)

    def action_see_stock_move(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Stock Moves'),
            'res_model': 'stock.move',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.stock_move_ids.ids)],
            'views':  [[self.env.ref('stock.view_move_tree').id, 'list'], [self.env.ref('stock.view_move_form').id, 'form']],
        }

    def action_see_invoice(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Invoices'),
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.invoice_ids.ids)],
            'views':  [[self.env.ref('account.view_out_invoice_tree').id, 'list'], [self.env.ref('account.view_move_form').id, 'form']],
        }
    
    def _compute_allowed_technicians(self):
        for rec in self:
            users = self.env['res.users'].search([]).filtered(lambda u: u.has_group('juke_mobile_service.group_mobile_service_technician') and not u.has_group('juke_mobile_service.group_mobile_service_manager'))
            rec.allowed_technicians = [(4, id) for id in users.ids]

    @api.onchange('customer_id')
    def _onchange_customer_id(self):
        if self.customer_id:
            self.contact_number = self.customer_id.phone or self.customer_id.mobile or ''
            self.email = self.customer_id.email or ''
            self.address = self.customer_id.street or ''

    def assign_to_tech(self):
        def get_technicians():
            users = self.env['res.users'].search([]).filtered(lambda u: u.has_group('juke_mobile_service.group_mobile_service_technician') and not u.has_group('juke_mobile_service.group_mobile_service_manager'))
            return users
            
        technicians = get_technicians()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Assign To Technician'),
            'res_model': 'mobile_service.assign_wizard',
            'view_mode': 'form',
            'views': [(self.env.ref('juke_mobile_service.mobile_service_assign_wizard_view_form').id, 'form')],
            'context': {
                'default_service_request_id': self.id,
                'default_allowed_technicians': [(4, id) for id in technicians.ids],
            },
            'target': 'new',
        }
    
    @api.onchange('mobile_brand_id')
    def _onchange_mobile_brand_id(self):
        for rec in self:
            if rec.mobile_model_id and rec.mobile_brand_id and rec.mobile_model_id.brand_id.id != rec.mobile_brand_id.id:
                rec.mobile_model_id = False

    def create_stock_move(self):
        def set_to_done(move_id):
            for move in move_id:
                move.write({'state': 'done'})
                move.move_line_ids.write({'state': 'done'})

        for rec in self:
            for line in rec.service_part_ids:

                move_id = rec.env['stock.move'].sudo().create({
                    'name': line.product_id.name + " -  From " + rec._description + " [" + rec.name + "]",
                    'product_id': line.product_id.id,
                    'product_uom': line.uom_id.id or line.product_id.uom_id.id,
                    'product_uom_qty': line.quantity,
                    'location_id': rec.env.ref('stock.stock_location_stock').id,
                    'location_dest_id': rec.env.ref('stock.stock_location_customers').id,
                    # 'picking_type_id': rec.env.ref('stock.picking_type_out').id,
                    'mobile_service_request_id': rec.id,
                    'move_line_ids': [(0, 0, {
                        'product_id': line.product_id.id,
                        'product_uom_id': line.uom_id.id or line.product_id.uom_id.id,
                        'quantity': line.quantity,
                        'location_id': rec.env.ref('stock.stock_location_stock').id,
                        'location_dest_id': rec.env.ref('stock.stock_location_customers').id,
                        # 'picking_type_id': rec.env.ref('stock.picking_type_out').id,
                        'mobile_service_request_id': rec.id,
                        'mobile_service_request_line_id': line.id,
                    })],
                })
                try:
                    move_id.sudo()._action_confirm()
                    move_id.sudo()._action_assign()
                    set_to_done(move_id)
                    move_id.sudo()._action_done()
                except Exception as e:
                    pass
    
    def completed_task(self):
        for rec in self:
            rec.create_stock_move()
            rec.state = 'completed'

    def not_solved(self):
        for rec in self:
            rec.state = 'not_solved'

    def return_customer(self):
        for rec in self:
            rec.state = 'returned'

    def print_ticket(self):
        return self.env.ref('juke_mobile_service.report_mobile_service_request_2').report_action(self)

    def create_invoice(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Create Invoice'),
            'res_model': 'mobile_service.create_invoice_wizard',
            'view_mode': 'form',
            'views': [(self.env.ref('juke_mobile_service.mobile_service_create_invoice_wizard_view_form').id, 'form')],
            'target': 'new',
            'context': {
                'default_service_request_id': self.id,
            },
        }
    

class ServiceRequestComplaint(models.Model):
    _name = 'mobile_service.service_request_complaint'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Service Request Complaint'
    _rec_name = 'complaint_type_id'

    service_id = fields.Many2one('mobile_service.service_request', string='Service Request', tracking=True)
    complaint_type_id = fields.Many2one('mobile_service.complaint_type', string='Complaint Type', tracking=True)
    complaint_template_id = fields.Many2one('mobile_service.complaint_template', string='Description', tracking=True)


class serviceRequestParts(models.Model):
    _name = 'mobile_service.service_request_parts'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Service Request Parts'
    _rec_name = 'product_id'

    service_id = fields.Many2one('mobile_service.service_request', string='Service Request', tracking=True)
    product_id = fields.Many2one('product.template', string='Product', domain=[('is_part_inventory', '=', True)], tracking=True)
    quantity = fields.Float(string='Quantity', default=1.0, tracking=True)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', tracking=True)
    price = fields.Float(string='Unit Price', compute='_compute_unit_price', store=True, tracking=True)
    stock = fields.Float(string='Stock Moved', compute="_compute_stock")
    invoice = fields.Float(string='Invoiced Qty', compute="_compute_invoiced_qty")
    total_price = fields.Float(string='Price', compute='_compute_total_price', store=True, tracking=True)

    def _compute_invoiced_qty(self):
        for rec in self:
            invoice_ids = self.env['account.move.line'].search([('mobile_service_request_line_id', '=', rec.id)])
            rec.invoice = sum([i.quantity for i in invoice_ids])

    @api.depends('product_id')
    def _compute_unit_price(self):
        for rec in self:
            rec.price = 0.0
            if rec.product_id:
                rec.price = rec.product_id.list_price if rec.product_id.list_price else 0.0
                rec.uom_id = rec.product_id.uom_id if 'uom_id' in rec.product_id._fields else False
    
    def _compute_stock(self):
        for rec in self:
            rec.stock = 0.0
            move_line_ids = self.env['stock.move.line'].search([('mobile_service_request_line_id', '=', rec.id), ('state', '=', 'done')])
            rec.stock = sum([i.quantity_product_uom for i in move_line_ids])

    @api.depends('price', 'quantity')
    def _compute_total_price(self):
        for rec in self:
            rec.total_price = 0.0
            if rec.price and rec.quantity:
                rec.total_price = rec.price * rec.quantity