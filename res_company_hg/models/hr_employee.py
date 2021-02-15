# -*- coding: utf-8 -*-


from odoo import models, fields


class HrEmployeeCompanyHg(models.Model):
    _inherit = "hr.employee"

    company_hg_id = fields.Many2one("res.company.hg", string="Empresa", required=True)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: