# -*- coding: utf-8 -*-

from odoo import models, fields


class StockPicking(models.Model):
    _inherit = ['stock.picking']

    attendance_id = fields.Many2one("hr.attendance.gaa", string="Lista de asistencia")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: