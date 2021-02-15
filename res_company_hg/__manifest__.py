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
    'name': 'Nuevo modelo empresas',
    'summary': """Añadir sección empresas en contabilidad""",
    'version': '1.0',
    'author': 'HG Consulting',
    'category': 'Company',
    'website': 'http://www.holocorp.com.mx',
    'description': """
Nuevo modelo de empresas
=============================================================================================================================

Permite agregar una nueva sección en el módulo de contabilidad para crear las diferentes
empresas del sistema. Esta es una alternativa al modelo de empresas del sistema encontrada en la sección
Configuración.

Se ha optado por esta solución aunque poco conveniente, permite crear todas las empresas necesarias que pueden
ser vistas por los demás usuarios, el módelo original no permite visualizar empresas diferentes a la principal,
a excepción que se active la funcionalidad multiempresa, la cual, no es conveniente agregar a cada uno de los usuarios.
Esta información será utilizada para agregar el fistro en los diferentes modelos para la generación de reportes.

Ademas se agrega el campo de empresa referente a esta nueva sección a los siguientes modelos:
* Cuentas bancarias [res.partner.bank]
* Empleados [hr.employee]
* Vehiculos [fleet.vechicle]

""",
    'depends': ['base', 'hr', 'fleet', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/company_view.xml',
        'views/fleet_vehicle_view.xml',
        'views/hr_employee_view.xml',
        'views/res_company_hg_view.xml',
        'views/res_users_view.xml',
        #'views/stock_warehouse_view.xml',
    ],
    #'active': True,
    'sequence': 9,
    #'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: