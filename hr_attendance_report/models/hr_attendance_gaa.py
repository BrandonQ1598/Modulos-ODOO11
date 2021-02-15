# -*- coding: utf-8 -*-

import datetime
import xlsxwriter
import base64
import io
from odoo.exceptions import ValidationError
from odoo import models, fields, api


class HrAttendanceGaaReport(models.TransientModel):
    _name = 'hr.attendance.gaa.report'

    xlxs_report = fields.Binary(string='Reporte')
    xlxs_report_filename = fields.Char(string='Reporte excel', size=64)


class HrAttendanceGaa(models.Model):
    _inherit = 'hr.attendance.gaa'

    @api.multi
    def generate_daily_report(self):
        """ @total_pro: total de procesos
            @total_emp: total de empaques
            @toal_he: total de horas extras
            :return: None """

        self.ensure_one()

        filename = self.name.replace('/', '_') + '.xlsx'
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)

        # Estilos
        center_fmt = workbook.add_format({'align': 'center', 'font_size': 9, 'border': 1, 'border_color': '#000000'})
        currency_fmt = workbook.add_format({'align': 'center', 'font_size': 9, 'border': 1, 'border_color': '#000000', 'num_format': '$#,##0.00'})
        left_fmt = workbook.add_format({'align': 'left', 'font_size': 9, 'border': 1, 'border_color': '#000000'})
        asistencia_fmt = workbook.add_format({'align': 'center', 'font_size': 9, 'border': 1, 'border_color': '#000000'})

        worksheet1 = workbook.add_worksheet('Lista de asistencia')
        # HEADER
        self.generate_header_report(workbook, worksheet1)

        # CONTENT
        employee_num = 1
        row = 5
        for item in self.thursday_employees_ids:
            # Get contract
            asistencias, total_emp, total_pro, total_he = 0, 0, 0, 0
            contract = self.env['hr.payslip'].get_contract(item.name, self.date_from, self.date_to)
            if not contract:
                raise ValidationError('El empleado: %s, no tiene definido un contrato con sueldo diario.' % item.name.name)

            contract_data = self.env['hr.contract'].search_read(
                [('id', '=', contract[0])],
                ['wage', 'salary_per_box_rasp', 'salary_per_box_straw', 'salary_per_pot_rasp', 'salary_per_pot_straw', 'salary_per_hour', 'salary_per_extra_hour']
            )

            worksheet1.write('A' + str(row), str(employee_num), center_fmt)
            worksheet1.write('B' + str(row), item.name.name, left_fmt)
            worksheet1.write('C' + str(row), str(contract_data[0].get('wage')), currency_fmt)
            
            # Jueves
            asistencias += 1 if item.attended else 0
            total_emp_dia = item.boxes_rasp1 + item.boxes_straw1 + item.boxes_rasp2 + item.boxes_straw2 + item.boxes_rasp3 + item.boxes_straw3
            total_emp += total_emp_dia
            total_pro_dia = item.pots_rasp1 + item.pots_straw1 + item.pots_rasp2 + item.pots_straw2 + item.pots_rasp3 + item.pots_straw3
            total_pro += total_pro_dia
            total_he += item.extra_hours
            worksheet1.write('D' + str(row), 'SI' if item.attended else 'NO', asistencia_fmt)
            worksheet1.write('E' + str(row), str(total_emp_dia), center_fmt)
            worksheet1.write('F' + str(row), str(total_pro_dia), center_fmt)
            worksheet1.write('G' + str(row), str(item.extra_hours), center_fmt)
            worksheet1.write('H' + str(row), str(''), center_fmt)
            worksheet1.write('I' + str(row), str(''), center_fmt)

            # Viernes
            employee = self.friday_employees_ids.filtered(lambda x: x.name == item.name)
            asistencias += 1 if employee.attended else 0
            total_emp_dia = employee.boxes_rasp1 + employee.boxes_straw1 + employee.boxes_rasp2 + employee.boxes_straw2 + employee.boxes_rasp3 + employee.boxes_straw3
            total_emp += total_emp_dia
            total_pro_dia = employee.pots_rasp1 + employee.pots_straw1 + employee.pots_rasp2 + employee.pots_straw2 + employee.pots_rasp3 + employee.pots_straw3
            total_pro += total_pro_dia
            total_he += employee.extra_hours
            worksheet1.write('J' + str(row), 'SI' if employee.attended else 'NO', asistencia_fmt)
            worksheet1.write('K' + str(row), str(total_emp_dia), center_fmt)
            worksheet1.write('L' + str(row), str(total_pro_dia), center_fmt)
            worksheet1.write('M' + str(row), str(employee.extra_hours), center_fmt)
            worksheet1.write('N' + str(row), str(''), center_fmt)
            worksheet1.write('O' + str(row), str(''), center_fmt)

            # Sabado
            employee = self.saturday_employees_ids.filtered(lambda x: x.name == item.name)
            asistencias += 1 if employee.attended else 0
            total_emp_dia = employee.boxes_rasp1 + employee.boxes_straw1 + employee.boxes_rasp2 + employee.boxes_straw2 + employee.boxes_rasp3 + employee.boxes_straw3
            total_emp += total_emp_dia
            total_pro_dia = employee.pots_rasp1 + employee.pots_straw1 + employee.pots_rasp2 + employee.pots_straw2 + employee.pots_rasp3 + employee.pots_straw3
            total_pro += total_pro_dia
            total_he += employee.extra_hours
            worksheet1.write('P' + str(row), 'SI' if employee.attended else 'NO', asistencia_fmt)
            worksheet1.write('Q' + str(row), str(total_emp_dia), center_fmt)
            worksheet1.write('R' + str(row), str(total_pro_dia), center_fmt)
            worksheet1.write('S' + str(row), str(employee.extra_hours), center_fmt)
            worksheet1.write('T' + str(row), str(''), center_fmt)
            worksheet1.write('U' + str(row), str(''), center_fmt)

            # Domingo
            employee = self.sunday_employees_ids.filtered(lambda x: x.name == item.name)
            asistencias += 1 if employee.attended else 0
            total_emp_dia = employee.boxes_rasp1 + employee.boxes_straw1 + employee.boxes_rasp2 + employee.boxes_straw2 + employee.boxes_rasp3 + employee.boxes_straw3
            total_emp += total_emp_dia
            total_pro_dia = employee.pots_rasp1 + employee.pots_straw1 + employee.pots_rasp2 + employee.pots_straw2 + employee.pots_rasp3 + employee.pots_straw3
            total_pro += total_pro_dia
            total_he += employee.extra_hours
            worksheet1.write('V' + str(row), 'SI' if employee.attended else 'NO', asistencia_fmt)
            worksheet1.write('W' + str(row), str(total_emp_dia), center_fmt)
            worksheet1.write('X' + str(row), str(total_pro_dia), center_fmt)
            worksheet1.write('Y' + str(row), str(employee.extra_hours), center_fmt)
            worksheet1.write('Z' + str(row), str(''), center_fmt)
            worksheet1.write('AB' + str(row), str(''), center_fmt)

            # Lunes
            employee = self.monday_employees_ids.filtered(lambda x: x.name == item.name)
            asistencias += 1 if employee.attended else 0
            total_emp_dia = employee.boxes_rasp1 + employee.boxes_straw1 + employee.boxes_rasp2 + employee.boxes_straw2 + employee.boxes_rasp3 + employee.boxes_straw3
            total_emp += total_emp_dia
            total_pro_dia = employee.pots_rasp1 + employee.pots_straw1 + employee.pots_rasp2 + employee.pots_straw2 + employee.pots_rasp3 + employee.pots_straw3
            total_pro += total_pro_dia
            total_he += employee.extra_hours
            worksheet1.write('AB' + str(row), 'SI' if employee.attended else 'NO', asistencia_fmt)
            worksheet1.write('AC' + str(row), str(total_emp_dia), center_fmt)
            worksheet1.write('AD' + str(row), str(total_pro_dia), center_fmt)
            worksheet1.write('AE' + str(row), str(employee.extra_hours), center_fmt)
            worksheet1.write('AF' + str(row), str(''), center_fmt)
            worksheet1.write('AG' + str(row), str(''), center_fmt)

            # Martes
            employee = self.tuesday_employees_ids.filtered(lambda x: x.name == item.name)
            asistencias += 1 if employee.attended else 0
            total_emp_dia = employee.boxes_rasp1 + employee.boxes_straw1 + employee.boxes_rasp2 + employee.boxes_straw2 + employee.boxes_rasp3 + employee.boxes_straw3
            total_emp += total_emp_dia
            total_pro_dia = employee.pots_rasp1 + employee.pots_straw1 + employee.pots_rasp2 + employee.pots_straw2 + employee.pots_rasp3 + employee.pots_straw3
            total_pro += total_pro_dia
            total_he += employee.extra_hours
            worksheet1.write('AH' + str(row), 'SI' if employee.attended else 'NO', asistencia_fmt)
            worksheet1.write('AI' + str(row), str(total_emp_dia), center_fmt)
            worksheet1.write('AJ' + str(row), str(total_pro_dia), center_fmt)
            worksheet1.write('AK' + str(row), str(employee.extra_hours), center_fmt)
            worksheet1.write('AL' + str(row), str(''), center_fmt)
            worksheet1.write('AM' + str(row), str(''), center_fmt)

            # Miercoles
            employee = self.tuesday_employees_ids.filtered(lambda x: x.name == item.name)
            asistencias += 1 if employee.attended else 0
            total_emp_dia = employee.boxes_rasp1 + employee.boxes_straw1 + employee.boxes_rasp2 + employee.boxes_straw2 + employee.boxes_rasp3 + employee.boxes_straw3
            total_emp += total_emp_dia
            total_pro_dia = employee.pots_rasp1 + employee.pots_straw1 + employee.pots_rasp2 + employee.pots_straw2 + employee.pots_rasp3 + employee.pots_straw3
            total_pro += total_pro_dia
            total_he += employee.extra_hours
            worksheet1.write('AN' + str(row), 'SI' if employee.attended else 'NO', asistencia_fmt)
            worksheet1.write('AO' + str(row), str(total_emp_dia), center_fmt)
            worksheet1.write('AP' + str(row), str(total_pro_dia), center_fmt)
            worksheet1.write('AQ' + str(row), str(employee.extra_hours), center_fmt)
            worksheet1.write('AR' + str(row), str(''), center_fmt)
            worksheet1.write('AS' + str(row), str(''), center_fmt)

            # Totales
            # Descuentos sacados del resumen
            employee = self.resume.filtered(lambda x: x.name == item.name)
            worksheet1.write('AT' + str(row), str(employee.loan_discount), currency_fmt)

            total_a_pagar = 0
            if contract_data[0].get('wage'):
                total_a_pagar += (asistencias * contract_data[0].get('wage'))
            if contract_data[0].get('salary_per_box_rasp'):
                total_a_pagar += (total_emp * contract_data[0].get('salary_per_box_rasp'))
            if contract_data[0].get('salary_per_pot_rasp'):
                total_a_pagar += (total_pro * contract_data[0].get('salary_per_pot_rasp'))
            if contract_data[0].get('salary_per_extra_hour'):
                total_a_pagar += (total_he * contract_data[0].get('salary_per_extra_hour'))

            worksheet1.write('AU' + str(row), str(total_a_pagar), currency_fmt)
            worksheet1.write('AV' + str(row), '', center_fmt)

            row += 1
            employee_num += 1

        workbook.close()
        record_id = self.env['hr.attendance.gaa.report'].create({'xlxs_report': base64.encodestring(output.getvalue()), 'xlxs_report_filename': filename})
        output.close()
        return {'view_mode': 'form',
                'res_id': record_id.id,
                'res_model': 'hr.attendance.gaa.report',
                'view_type': 'form',
                'type': 'ir.actions.act_window',
                'target': 'new',
                }

    def generate_header_report(self, workbook, worksheet):
        # Estilos
        header_fmt = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#C6EFCE', 'font_size': 12, 'border': 2, 'border_color': '#000000'})
        subtitle_bg_fmt = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#C6EFCE', 'font_size': 9, 'border': 1, 'border_color': '#000000'})
        subtitle_fmt = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'font_size': 9, 'border': 1, 'border_color': '#000000'})
        wid_15, wid_10, wid_5 = 15, 10, 5

        bold_fmt = workbook.add_format({'bold': True})
        center_fmt = workbook.add_format(({'align': 'center'}))
        currency_fmt = workbook.add_format({'num_format': '$#,##0.00'})
        currency_bold_fmt = workbook.add_format({'num_format': '$#,##0.00', 'bold': True})
        date_fmt = workbook.add_format({'num_format': 'dd/mm/yyyy'})
        percentage_fmt = workbook.add_format({'num_format': '0.00##\\%;[Red](0.00##\\%)'})
        percentage_bold_fmt = workbook.add_format({'num_format': '0.00##\\%;[Red](0.00##\\%)', 'bold': True})
        number_format = workbook.add_format({'num_format': '#,##0.00'})
        number_format_bold = workbook.add_format({'num_format': '#,##0.00', 'bold': True})

        worksheet.set_row(0, 24, header_fmt)
        worksheet.merge_range('A1:AV1', self.name.replace('/', '_'))
        worksheet.set_column('A:A', wid_5)
        worksheet.merge_range('A2:A4', 'No.', subtitle_fmt)
        worksheet.set_column('B:B', 30)
        worksheet.merge_range('B2:B4', 'NOMBRE', subtitle_fmt)
        worksheet.set_column('C:C', 8)
        worksheet.merge_range('C2:C4', 'SUELDO', subtitle_fmt)
        # JUEVES
        if self.thursday_date:
            worksheet.merge_range('D2:I2', datetime.datetime.strptime(self.thursday_date, '%Y-%m-%d').strftime('%d-%m-%Y'), subtitle_bg_fmt)
            worksheet.merge_range('D3:I3', 'JUEVES', subtitle_fmt)
            worksheet.set_column('D:D', wid_5)
            worksheet.write('D4', 'A', subtitle_bg_fmt)
            worksheet.set_column('E:E', wid_5)
            worksheet.write('E4', 'EMP', subtitle_bg_fmt)
            worksheet.set_column('F:F', wid_5)
            worksheet.write('F4', 'PRO', subtitle_bg_fmt)
            worksheet.set_column('G:G', wid_5)
            worksheet.write('G4', 'HE', subtitle_bg_fmt)
            worksheet.set_column('H:H',wid_5)
            worksheet.write('H4', 'FU', subtitle_bg_fmt)
            worksheet.set_column('I:I', wid_5)
            worksheet.write('I4', 'HD', subtitle_bg_fmt)
        # VIERNES
        if self.friday_date:
            worksheet.merge_range('J2:O2', datetime.datetime.strptime(self.friday_date, '%Y-%m-%d').strftime('%d-%m-%Y'), subtitle_bg_fmt)
            worksheet.merge_range('J3:O3', 'VIERNES', subtitle_fmt)
            worksheet.set_column('J:J', wid_5)
            worksheet.write('J4', 'A', subtitle_bg_fmt)
            worksheet.set_column('K:K', wid_5)
            worksheet.write('K4', 'EMP', subtitle_bg_fmt)
            worksheet.set_column('L:L', wid_5)
            worksheet.write('L4', 'PRO', subtitle_bg_fmt)
            worksheet.set_column('M:M', wid_5)
            worksheet.write('M4', 'HE', subtitle_bg_fmt)
            worksheet.set_column('N:N', wid_5)
            worksheet.write('N4', 'FU', subtitle_bg_fmt)
            worksheet.set_column('O:O', wid_5)
            worksheet.write('O4', 'HD', subtitle_bg_fmt)
        # SABADO
        if self.saturday_date:
            worksheet.merge_range('P2:U2', datetime.datetime.strptime(self.saturday_date, '%Y-%m-%d').strftime('%d-%m-%Y'), subtitle_bg_fmt)
            worksheet.merge_range('P3:U3', 'SABADO', subtitle_fmt)
            worksheet.set_column('P:P', wid_5)
            worksheet.write('P4', 'A', subtitle_bg_fmt)
            worksheet.set_column('Q:Q', wid_5)
            worksheet.write('Q4', 'EMP', subtitle_bg_fmt)
            worksheet.set_column('R:R', wid_5)
            worksheet.write('R4', 'PRO', subtitle_bg_fmt)
            worksheet.set_column('S:S', wid_5)
            worksheet.write('S4', 'HE', subtitle_bg_fmt)
            worksheet.set_column('T:T', wid_5)
            worksheet.write('T4', 'FU', subtitle_bg_fmt)
            worksheet.set_column('U:U', wid_5)
            worksheet.write('U4', 'HD', subtitle_bg_fmt)
        # DOMINGO
        if self.sunday_date:
            worksheet.merge_range('V2:AA2', datetime.datetime.strptime(self.sunday_date, '%Y-%m-%d').strftime('%d-%m-%Y'), subtitle_bg_fmt)
            worksheet.merge_range('V3:AA3', 'DOMINGO', subtitle_fmt)
            worksheet.set_column('V:V', wid_5)
            worksheet.write('V4', 'A', subtitle_bg_fmt)
            worksheet.set_column('W:W', wid_5)
            worksheet.write('W4', 'EMP', subtitle_bg_fmt)
            worksheet.set_column('X:X', wid_5)
            worksheet.write('X4', 'PRO', subtitle_bg_fmt)
            worksheet.set_column('Y:Y', wid_5)
            worksheet.write('Y4', 'HE', subtitle_bg_fmt)
            worksheet.set_column('Z:Z', wid_5)
            worksheet.write('Z4', 'FU', subtitle_bg_fmt)
            worksheet.write('AA4', 'HD', subtitle_bg_fmt)
        # LUNES
        if self.monday_date:
            worksheet.merge_range('AB2:AG2', datetime.datetime.strptime(self.monday_date, '%Y-%m-%d').strftime('%d-%m-%Y'), subtitle_bg_fmt)
            worksheet.merge_range('AB3:AG3', 'LUNES', subtitle_fmt)
            worksheet.set_column('AB:AB', wid_5)
            worksheet.write('AB4', 'A', subtitle_bg_fmt)
            worksheet.set_column('AC:AC', wid_5)
            worksheet.write('AC4', 'EMP', subtitle_bg_fmt)
            worksheet.set_column('AD:AD', wid_5)
            worksheet.write('AD4', 'PRO', subtitle_bg_fmt)
            worksheet.set_column('AE:AE', wid_5)
            worksheet.write('AE4', 'HE', subtitle_bg_fmt)
            worksheet.set_column('AF:AF', wid_5)
            worksheet.write('AF4', 'FU', subtitle_bg_fmt)
            worksheet.set_column('AG:AG', wid_5)
            worksheet.write('AG4', 'HD', subtitle_bg_fmt)
        # MARTES
        if self.tuesday_date:
            worksheet.merge_range('AH2:AM2', datetime.datetime.strptime(self.tuesday_date, '%Y-%m-%d').strftime('%d-%m-%Y'), subtitle_bg_fmt)
            worksheet.merge_range('AH3:AM3', 'MARTES', subtitle_fmt)
            worksheet.set_column('AH:AH', wid_5)
            worksheet.write('AH4', 'A', subtitle_bg_fmt)
            worksheet.write('AI4', 'EMP', subtitle_bg_fmt)
            worksheet.set_column('AJ:AJ', wid_5)
            worksheet.write('AJ4', 'PRO', subtitle_bg_fmt)
            worksheet.set_column('AK:AK', wid_5)
            worksheet.write('AK4', 'HE', subtitle_bg_fmt)
            worksheet.set_column('AL:AL', wid_5)
            worksheet.write('AL4', 'FU', subtitle_bg_fmt)
            worksheet.set_column('AM:AM', wid_5)
            worksheet.write('AM4', 'HD', subtitle_bg_fmt)
        # MIERCOLES
        if self.wednesday_date:
            worksheet.merge_range('AN2:AS2', datetime.datetime.strptime(self.wednesday_date, '%Y-%m-%d').strftime('%d-%m-%Y'), subtitle_bg_fmt)
            worksheet.merge_range('AN3:AS3', 'MIERCOLES', subtitle_fmt)
            worksheet.set_column('AN:AN', wid_5)
            worksheet.write('AN4', 'A', subtitle_bg_fmt)
            worksheet.set_column('AO:AO', wid_5)
            worksheet.write('AO4', 'EMP', subtitle_bg_fmt)
            worksheet.set_column('AP:AP', wid_5)
            worksheet.write('AP4', 'PRO', subtitle_bg_fmt)
            worksheet.set_column('AQ:AQ', wid_5)
            worksheet.write('AQ4', 'HE', subtitle_bg_fmt)
            worksheet.set_column('AR:AR', wid_5)
            worksheet.write('AR4', 'FU', subtitle_bg_fmt)
            worksheet.set_column('AS:AS', wid_5)
            worksheet.write('AS4', 'HD', subtitle_bg_fmt)

        worksheet.set_column('AT:AT', wid_10)
        worksheet.merge_range('AT2:AT4', 'DESCUEN\nTOS', subtitle_bg_fmt)
        worksheet.set_column('AU:AU', wid_10)
        worksheet.merge_range('AU2:AU4', 'TOTAL A \nPAGAR', subtitle_bg_fmt)
        worksheet.set_column('AV:AV', wid_15)
        worksheet.merge_range('AV2:AV4', 'COMENTARIOS', subtitle_fmt)