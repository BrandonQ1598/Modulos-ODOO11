# -*- coding: utf-8 -*-

from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def _get_next_seq(self):
        return int(self.env['hr.employee'].search_count([('active', '=', True)])) + 1

    sequence = fields.Integer('Orden del empleado', default=_get_next_seq)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: