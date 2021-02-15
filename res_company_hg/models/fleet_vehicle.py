# -*- coding: utf-8 -*-


from odoo import fields, models


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    company_hg_id = fields.Many2one("res.company.hg", string="Empresa", required=True)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: