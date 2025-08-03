# -*- coding: utf-8 -*-
# from odoo import http


# class JukeMobileService(http.Controller):
#     @http.route('/juke_mobile_service/juke_mobile_service', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/juke_mobile_service/juke_mobile_service/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('juke_mobile_service.listing', {
#             'root': '/juke_mobile_service/juke_mobile_service',
#             'objects': http.request.env['juke_mobile_service.juke_mobile_service'].search([]),
#         })

#     @http.route('/juke_mobile_service/juke_mobile_service/objects/<model("juke_mobile_service.juke_mobile_service"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('juke_mobile_service.object', {
#             'object': obj
#         })

