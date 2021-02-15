{
    'name': "Pagina Web de Facturación",
    'summary': """
        Genera un sitio web de facturacion""",
    'description': """
        Crear reporte de ventas en determinadas fechas
            - Dado un periodo de tiempo
            - Por cliente o general
            - Incluye Facturas, Pagos, Notas de Credito y Anticipos
    """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Test',
    'version': '1.0',
    'depends': ['base','point_of_sale'],
    'data': [
        'views/templates.xml',
    ],
    'qweb':['static/src/xml/pos_ticket_view.xml'],
    'sequence': 1,
    'auto_install': False,
    'application': False,
}