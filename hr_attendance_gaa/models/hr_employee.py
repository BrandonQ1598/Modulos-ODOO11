# -*- coding: utf-8 -*-

from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    employee_type = fields.Many2one("hr.config.order.employee", string="Tipo de empleado", required=True,
                                    help="Campo utilizado para ordenar los empleados en la lista de asistencia, considerando el orden alfabético")


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: