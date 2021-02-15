# -*- coding: utf-8 -*-


from odoo import models, fields


class StockWarehouse (models.Model):
    _inherit = "stock.warehouse"

    company_hg_id = fields.Many2one("res.company.hg", string="Empresa", required=True)


class StockLocation (models.Model):
    _inherit = "stock.location"

    company_hg_id = fields.Many2one("res.company.hg", string="Empresa")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: