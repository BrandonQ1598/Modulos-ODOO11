# -*- coding: utf-8 -*-

{
    'name': 'Administración de temporadas, predios y cultivos',
    'summary': """Habilitar uso de predios""",
    'version': '1.0',
    'author': 'HG Consulting',
    'category': 'Inventory, Logistic, Storage',
    'website': 'http://www.holocorp.com.mx',
    'description': """
Habilitar el uso de temporadas, predios y cultivos en el sistema
=============================================================================================================================

Crea un nuevo menú del módulo.

* Este módulo permite habilitar el uso de temporadas, predios y cultivos para administrar los gastos de acuerdo a la
ubicación en un centro de producción agrícola. El módulo hereda las propiedades del módelo de Almacenes para los
predios.
* Agrega además al modelo el campo Es predio.
* Agrega al modelo stock.warehouse [Almácenes], el dominio para evitar ver los predio, así como el respectivo
dominio a los predios para evitar ver los almácenes.
* Al crear un nuevo almacén o predio, automáticamente se llenan los campos empresa y es predio, de acuerdo al
tipo de elemento creado.

""",
    'depends': ['stock'],
    'data': [
        'security/estate_security.xml',
        'security/ir.model.access.csv',
        'views/stock_estate_view.xml',
        'views/stock_estate_crop_view.xml',
        'views/stock_estate_crop_workflow.xml',
        'views/stock_estate_season_view.xml',
        'views/stock_estate_season_workflow.xml',
    ],
    'active': True,
    'sequence': 10,
    'installable': True,
    'auto_install': False,
}