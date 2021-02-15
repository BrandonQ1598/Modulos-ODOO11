# -*- coding: utf-8 -*-

from odoo import models


class StockEstateReport(models.TransientModel):
    _name = "stock.estate.report"


    def _get_test(self, date_from):
        print (date_from)
        return "Prueba exitosa"

    def _get_expense_crop_report(self, season_id, estate_id, crop_id, date_from, date_to, product_type_id):
        if product_type_id:
            # Reporte considerando el tipo de producto
            move_obj = self.env['stock.move'].search(
                [('season_id', '=', season_id), ('estate_id', '=', estate_id), ('crop_id', '=', crop_id)])

            return "Reporte de gastos de cultivos"
        else:
            # Generar reporte sin aplicar filtro del tipo de producto
            return "Reporte de gastos de cultivos"


class AbstractBonusWeekReport(models.AbstractModel):
    _name = "report.stock_estate_report.bonus_week_report"
    _template = "stock_estate_report.bonus_week_report"
    #_wrapped_report_class = ReportEstate


class AbstractExpenseCropReport(models.AbstractModel):
    _name = "report.stock_estate_report.expense_crop_report_template"
    _template = "stock_estate_report.expense_crop_report_template"
    #_wrapped_report_class = ReportEstate

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: