{
    'name': "Reporte Pagos Generales",
    'summary': """
        Crear reporte de pagos generales""",
    'description': """
        Crear reporte de pagos generales
    """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Test',
    'version': '1.0',
    'depends': ['base', 'account'],
    'data': [
        'wizard/pagos_generales_report_wizard_template.xml',
        'report/pagos_generales_report_template.xml',
        'views/account_payment_views.xml',
    ],
    'sequence': 1,
    'auto_install': False,
    'application': False,
}