# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class WebSiteFacturacion(http.Controller):

    @http.route(['/facturacion'], auth='public', website=True)
    def facturacion(self):
        return request.render('modulo_facturacion_web.index')

    @http.route(['/datosfactura'], auth='public', website=True)
    def datosfactura(self, **post):
        return request.render('modulo_facturacion_web.datosfactura',{
            'token': post['token']
        })

    @http.route(['/datosfacturacion'], auth='public', website=True)
    def datosfacturacion(self):
        return request.render('modulo_facturacion_web.datosfacturacion')
