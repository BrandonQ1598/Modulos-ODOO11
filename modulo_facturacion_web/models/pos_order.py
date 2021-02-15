# -*- coding: utf-8 -*-

from odoo import models, fields, api
import secrets

class WebSiteSaleFacturationToken(models.Model):
    _inherit = 'pos.order'

    token = fields.Char('Token', required=True,  compute='get_token_facturacion')

    @api.multi
    def get_token_facturacion(self,cliente):
        token = secrets.token_hex(20)
        return token
