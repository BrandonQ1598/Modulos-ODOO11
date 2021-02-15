# -*- coding: utf-8 -*-

from odoo import models, fields


class ResUsers (models.Model):
    _inherit = "res.users"

    company_hg_id = fields.Many2one("res.company.hg", string="Empresa personalizada", required=True)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: