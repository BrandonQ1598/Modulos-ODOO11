# -*- coding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2015 HG Consulting - http://www.holocorp.com.mx
#    All Rights Reserved.
#    info HG Consulting (info@holocorp.com.mx)
############################################################################
#    Coded by: ltorres (ltorres@holocorp.com.mx)
#    Financed by: http://www.holocorp.com.mx (info@holocorp.com.mx)
############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api
from odoo.exceptions import Warning


class StockEstateSeason(models.Model):
    _name = "stock.estate.season"
    _inherit = ["mail.thread"]
    _description = "Temporada"

    READONLY_STATES = {
        'closed': [('readonly', True)],
        'canceled': [('readonly', True)],
    }

    READONLY_STATES_OCC = {
        'open': [('rea-donly', True)],
        'closed': [('readonly', True)],
        'canceled': [('readonly', True)],
    }

    name = fields.Char(string="Nombre", required=True, states=READONLY_STATES)
    estate_id = fields.Many2many("stock.warehouse", "stock_warehouse_season", "season_id", "warehouse_id",
                                 string="Predios", domain=[('is_estate', '=', True), ('active', '=', True)],
                                 states=READONLY_STATES)
    start_date = fields.Date(string="Fecha de inicio", required=True, states=READONLY_STATES)
    end_date = fields.Date(string="Fecha de termino", required=True, states=READONLY_STATES)
    notes = fields.Text(string="Notas")
    state = fields.Selection([
        ('draft', "Borrador"),
        ('open', "Abierta"),
        ('closed', "Cerrada"),
        ('canceled', "Cancelada")
    ], 'Estado', default='draft')

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_open(self):
        self.state = 'open'

    @api.multi
    def action_closed(self):
        crop_obj = self.env['stock.estate.crop'].search(
            [('season_id', '=', self.id), ('state', 'not in', ['closed', 'canceled'])])
        if len(crop_obj) > 0:
            raise Warning("No se puede cerrar la temporada ya que existen aún cultivos sin cerrar.")
        self.state = 'closed'

    @api.multi
    def action_canceled(self):
        self.state = 'canceled'

    @api.multi
    def get_domain_estate(self, company_hg_id):
        if company_hg_id:
            return {'domain': {
                'estate_id': [('company_hg_id', '=', company_hg_id), ('is_estate', '=', True), ('active', '=', True)]},
                    'value': {'estate_id': False}}
        else:
            return {'domain': {'estate_id': [('is_estate', '=', True), ('active', '=', True)]},
                    'value': {'estate_id': False}}

    # Prueba para revisar si se puede contrar el no poder quitar un predio si ya tuvo movimientos
    @api.multi
    def write(self, vals):
        return super(StockEstateSeason, self).write(vals)

    # @api.multi
    # def action_reopen(self):
    #    self.state = 'draft'
    #    for id in self.ids:
    #        workflow.trg_delete(self._uid, 'stock.estates.season', id, self.env.cr)

# class StockEstate(models.Model):
#    _inherit = "stock.warehouse"

#    season_id = fields.One2many("stock.estate.season", "estate_id", string="Temporada")


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: