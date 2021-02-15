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

{
    'name': 'Reportes lista de asistencia',
    'summary': """Resumen de lista de asistencia""",
    'version': '2020.8.1',
    'author': 'HG Consulting',
    'category': 'Human Resources',
    'website': 'http://www.holocorp.com.mx',
    'depends': ['hr_payroll', 'hr_attendance_gaa'],
    'data': [
        'security/ir.model.access.csv',
        'data/report_paperformat.xml',
        'report/hr_attendance_report.xml',
        'report/hr_attendance_report_styles.xml',
        'views/hr_attendance_report_menu.xml',
        'views/hr_attendance_gaa_view.xml',
    ],
    'application': False,
    'sequence': 4,
    'installable': True,
    'auto_install': False,
}
