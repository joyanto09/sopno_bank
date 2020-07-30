# -*- coding: utf-8 -*-
from odoo import http

# class SopnobankmangModel(http.Controller):
#     @http.route('/sopnobankmang_model/sopnobankmang_model/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sopnobankmang_model/sopnobankmang_model/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sopnobankmang_model.listing', {
#             'root': '/sopnobankmang_model/sopnobankmang_model',
#             'objects': http.request.env['sopnobankmang_model.sopnobankmang_model'].search([]),
#         })

#     @http.route('/sopnobankmang_model/sopnobankmang_model/objects/<model("sopnobankmang_model.sopnobankmang_model"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sopnobankmang_model.object', {
#             'object': obj
#         })