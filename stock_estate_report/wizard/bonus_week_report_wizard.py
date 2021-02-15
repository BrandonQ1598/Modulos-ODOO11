# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockEstateBonusWeekReport(models.TransientModel):
    _name = "stock.estate.bonus.week.report"
    _description = "Reporte para calculo de bonos"

    season_id = fields.Many2one("stock.estate.season", string="Temporada", required=True)
    estate_id = fields.Many2one("stock.warehouse", string="Predio")
    attendance_ids = fields.Many2many("hr.attendance.gaa", "hr_bonus_attendance_rel", "bonus_id",
                                     "attendance_id", string="Listas de asistencia", required=True)
    date_from = fields.Date(string="Fecha inicial", required=True, default=fields.Date.today())
    date_to = fields.Date(string="Fecha final", required=True, default=fields.Date.today())

    @api.multi
    def get_domain_attendance_week(self, season_id):
        """
            Método que permite aplicar un doble filtro, uno a las listas de asistencias y el otro a los predios,
            además, al momento de cambiar la temporada se resetea el valor seleccionado del predio. Se llama un
            segundo método el cual genera el filtro para los predios y este se concatena con el filtro de listas
            de asistencias.
        """
        if season_id:
            estate_domain = self.get_domain_estate(season_id)
            return {'domain': {'attendance_ids': [('state', 'not in', ['draft', 'canceled']),
                                                  ('season_id', '=', season_id)], 'estate_id': estate_domain},
                    'value': {'estate_id': False}}
        else:
            estate_domain = self.get_domain_estate(season_id)
            return {'domain': {'attendance_ids': [('state', 'not in', ['draft', 'canceled'])],
                               'estate_id': estate_domain}, 'value': {'estate_id': False}}

    @api.multi
    def get_domain_estate(self, season_id):
        """ Método que genera el filtro para los predios, ya sea que la temporada tenga 1 o más predios. """
        if season_id:
            season_obj = self.env['stock.estate.season'].search([('id', '=', season_id)])
            estate_ids = []
            for season in season_obj:
                if len(season.estate_id) > 1:
                    for element in season.estate_id:
                        estate_ids += [str(element.id)]
                else:
                    estate_ids = [season.estate_id.id]

            return "[('is_estate', '=', True), ('active', '=', True), ('id', 'in', " + str(estate_ids) + ")]"
        else:
            return "[('is_estate', '=', True), ('active', '=', True)]"

    @api.multi
    def print_bonus_week_report(self):
        """ Método que llama el reporte de la verificación del bono semanal, con el cual, se envían variables
            al reporte, para poder realizar reportes dinámicos de acuerdo a ciertos filtros """
        report_obj = self.env['stock.estate.bonus.week.report'].search([]).ids
        data = {'ids': self._ids}
        return self.env['report'].get_action(self, 'stock_estate_report.bonus_week_report', data=data)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: