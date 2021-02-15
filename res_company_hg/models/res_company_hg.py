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
#    it under the terms of t# -*- coding: utf-8 -*-
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

from odoo import models, fields


class ResCompanyHg (models.Model):
    _name = "res.company.hg"

    name = fields.Char(string="Nombre de la empresa", required=True)
    partner_id = fields.Many2one("res.partner", string="Empresa propietaria", required=True)
    logo = fields.Binary(string="Logo")
    street = fields.Char(string="Calle")
    street2 = fields.Char(string="Colonia")
    city = fields.Char(string="Ciudad")
    state_id = fields.Many2one("res.country.state", strring="Estado")
    zip = fields.Char(string="Código postal")
    country_id = fields.Many2one("res.country", string="País")
    rml_header1 = fields.Char(string="Lema de la empresa")
    website = fields.Char(string="Sitio web")
    phone = fields.Char(string="Teléfono")
    email = fields.Char(string="Email")
    vat = fields.Char(string="RFC")


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:he GNU Affero General Public License as
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

from odoo import models, fields


class ResCompanyHg (models.Model):
    _name = "res.company.hg"

    name = fields.Char(string="Nombre de la empresa", required=True)
    partner_id = fields.Many2one("res.partner", string="Empresa propietaria", required=True)
    logo = fields.Binary(string="Logo")
    street = fields.Char(string="Calle")
    street2 = fields.Char(string="Colonia")
    city = fields.Char(string="Ciudad")
    state_id = fields.Many2one("res.country.state", strring="Estado")
    zip = fields.Char(string="Código postal")
    country_id = fields.Many2one("res.country", string="País")
    rml_header1 = fields.Char(string="Lema de la empresa")
    website = fields.Char(string="Sitio web")
    phone = fields.Char(string="Teléfono")
    email = fields.Char(string="Email")
    vat = fields.Char(string="RFC")


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: