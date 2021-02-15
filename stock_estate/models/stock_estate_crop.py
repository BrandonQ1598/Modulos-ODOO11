# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockEstateCrop (models.Model):
    _name = "stock.estate.crop"
    _description = "Cultivos"
    _inherit = ['mail.thread']

    # Metodo que filtra los predios de acuerdo a la temporada seleccionada
    @api.multi
    def get_domain_estate(self, season_id):
        if season_id:
            season_obj = self.env['stock.estate.season'].search([('id', '=', season_id)])
            estate_ids = []
            for season in season_obj:
                if len(season.estate_id) > 1:
                    for element in season.estate_id:
                        estate_ids += [str(element.id)]
                else:
                    estate_ids = [season.estate_id.id]

            return {'domain': {'estate_id': [('is_estate', '=', True), ('id', 'in', estate_ids), ('active', '=', True)]},
                    'value': {'estate_id': False}}
        else:
            return {'domain': {'estate_id': [('is_estate', '=', True), ('active', '=', True)]},
                    'value': {'estate_id': False}}

    READONLY_STATES = {
        'closed': [('readonly', True)],
        'canceled': [('readonly', True)],
    }
    # OCC = Open, Close, Canceled
    READONLY_STATES_OCC = {
        'open': [('readonly', True)],
        'closed': [('readonly', True)],
        'canceled': [('readonly', True)],
    }

    name = fields.Char(string="Nombre de cultivo", required=True, states=READONLY_STATES)
    season_id = fields.Many2one("stock.estate.season", string="Temporada", required=True, domain=[('state', 'in', ['open'])], states=READONLY_STATES_OCC)
    estate_id = fields.Many2one("stock.warehouse", string="Predio", required=True, domain=[('is_estate', '=', True), ('active', '=', True)], states=READONLY_STATES_OCC)
    start_date = fields.Date(string="Fecha de inicio", required=True, states=READONLY_STATES)
    end_date = fields.Date(string="Fecha de termino", required=True, states=READONLY_STATES)
    active = fields.Boolean(string='Activo', default=True)
    notes = fields.Text(string="Notas")
    state = fields.Selection([
        ('draft', "Borrador"),
        ('open', "Abierto"),
        ('closed', "Cerrado"),
        ('canceled', "Cancelado"),
    ], 'Estado', default='draft')

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_open(self):
        self.state = 'open'

    @api.multi
    def action_closed(self):
        self.state = 'closed'

    @api.multi
    def action_canceled(self):
        self.state = 'canceled'


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: