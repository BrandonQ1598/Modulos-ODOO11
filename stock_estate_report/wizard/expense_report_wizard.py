# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ExpenseCropReportWizard(models.TransientModel):
    _name = "expense.crop.report.wizard"
    _description = "Reporte de gastos"

    date_from = fields.Date(string="Fecha inicial")
    date_to = fields.Date(string="Fecha final")
    season_id = fields.Many2one("stock.estate.season", string="Temporada", domain=[('state', 'in', ['done', 'open'])], required=True)
    estate_id = fields.Many2one("stock.warehouse", string="Predio", required=True)
    crop_id = fields.Many2one("stock.estate.crop", string="Cultivo", required=True)
    product_type_id = fields.Many2one("product.type", string="Clasificación")

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

            return {'domain': {'estate_id': [('id', 'in', estate_ids), ('active', '=', True)]},
                    'value': {'estate_id': False, 'crop_id': False}}
        else:
            return {'domain': {'estate_id': [('is_estate', '=', True), ('active', '=', True)]},
                    'value': {'estate_id': False, 'crop_id': False}}

    @api.multi
    def get_domain_crop(self, season_id, estate_id):
        if season_id and estate_id:
            return {'domain': {
                'crop_id': [('state', 'in', ['open']), ('season_id', '=', season_id), ('estate_id', '=', estate_id)]},
                'value': {'crop_id': False}}
        else:
            return {'domain': {'crop_id': [('state', 'in', ['open'])]},
                    'value': {'crop_id': False}}

    @api.multi
    def print_report_crop(self):
        data = {'ids': self._ids}
        return self.env['report'].get_action(self, 'stock_estate_report.expense_crop_report_template', data=data)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: