# -*- coding: utf-8 -*-
{
    'name': 'Reportes de predios',
    'summary': """Generación de reportes de predios""",
    'version': '1.0',
    'author': 'HG Consulting',
    'category': 'Warehouse',
    'website': 'http://www.holocorp.com.mx',
    'description': """
Reportes de predios
=============================================================================================================================

Se agregan diferentes reportes para los gastos de los predios, siendo estos los siguientes:
* Reporte de bono semanal
* Reporte de bono al final de la temporada
""",
    'depends': ['stock_estate', 'hr_attendance_gaa', 'stock_estate_expense'],
    'data': [
        'security/ir.model.access.csv',
        'data/report_paperformat.xml',
        'report/estate_bonus_week_report.xml',
        'report/estate_bonus_week_styles.xml',
        'report/expense_crop_report.xml',
        'views/estate_report_menu.xml',
        'wizard/bonus_week_report_wizard.xml',
        'wizard/expense_report_wizard.xml',
    ],
    #'active': True,
    'sequence': 12,
    #'installable': True,
    'auto_install': False,
}