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

{
    'name': 'Lista de asistencia y corte',
    'summary': """Capturar la asistencia y corte""",
    'version': '1.0',
    'author': 'HG Consulting',
    'category': 'Human Resources',
    'website': 'http://www.holocorp.com.mx',
    'description': """
Lista de asistencia y corte
=============================================================================================================================

Permite capturar la asistencia de los empleados por semana de trabajo, así como también, la cantidad
de cajas, botes, trabajo por horas y horas extras, con lo cual, se podrá realizar el cálculo
automático del sueldo de los empleados. Ingresando la hora de entrada y salida, el sistema realiza
automáticamente todos los cálculos para las horas trabajadas, asistencia y horas extra.
""",
    'depends': ['base', 'mail', 'res_company_hg', 'hr', 'hr_payroll', 'stock_estate'],
    'data': [
        'security/estate_security.xml',
        'security/ir.model.access.csv',
        'data/report_paperformat.xml',
        'report/print_work_day_menu.xml',
        'report/print_work_day_report_tuesday.xml',
        'report/print_work_day_report_wednesday.xml',
        'report/print_work_day_report_thursday.xml',
        'report/print_work_day_report_friday.xml',
        'report/print_work_day_report_saturday.xml',
        'report/print_work_day_report_sunday.xml',
        'report/print_work_day_report_monday.xml',
        'report/print_work_day_report_resumen.xml',
        'views/hr_attendance_config_view.xml',
        'views/hr_attendance_gaa_view.xml',
        'views/hr_attendance_gaa_workflow.xml',
        'views/hr_employee_view.xml',
        'views/res_config_view.xml',
        'views/sequence.xml',
        'views/stock_move_view.xml',
    ],
    #'active': True,
    'sequence': 3,
    #'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: