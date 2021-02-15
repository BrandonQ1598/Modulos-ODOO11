# -*- coding: utf-8 -*-

from odoo import models, fields


class StockMove(models.Model):
    _inherit = ['stock.move']

    is_attendance = fields.Boolean(string="Lista de asistencia", readonly=True)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: