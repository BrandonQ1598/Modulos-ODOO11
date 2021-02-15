# -*- coding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2015 HG Consulting - http://www.holocorp.com.mx
#    All Rights Reserved.
#    info HG Consulting (info@holocorp.com.mx)
############################################################################
#    Coded by: ltorres (ltorres@holocorp.com.mx, leomorsy@gmail.com)
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
    'name': 'Orden de los empleados en lista de asistencia',
    'summary': """Orden de los empleados en lista de asistencia""",
    'version': '1.0',
    'author': 'HG Consulting',
    'category': 'Human Resources',
    'website': 'http://www.holocorp.com.mx',
    'description': """
Orden de los empleados en lista de asistencia
=============================================================================================================================

Este módulo agrega una nueva vista de los empleados del tipo tree desde la cual, se pueden modificar 
el nombre del empleado, puesto de trabajo, tipo de empleado y secuencia, este último campo es utilizado 
para darle orden a los empleados de la lista de asistencia en cada uno de los días.
""",
    'depends': ['base', 'mail', 'hr', 'hr_attendance_gaa'],
    'data': [
        'views/hr_attendance_gaa_view.xml',
        'views/hr_employee_view.xml',
    ],
    'sequence': 18,
    'installable': True,
    'application': False,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: