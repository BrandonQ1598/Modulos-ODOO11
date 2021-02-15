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

from odoo import fields, models, api
from odoo.exceptions import Warning


class HrAttendanceConfig(models.Model):
    """ Modelo para agregar configuración a las listas de asistencia, en lo que respecta
        horarios de entrada y salida, así como también, rangos de redondeo para las horas.
        Con lo cual se cálculan automáticamente la asistencia, horas trabajadas, horas
        extras y la validación correcta de las horas. """

    _name = "hr.attendance.config"
    _description = "Configuracion de la lista de asistencia"

    name = fields.Char(string="Nombre", required=True)
    time_in = fields.Float(string="Hora de entrada", required=True, default=0.00)
    time_out = fields.Float(string="Hora de salida", required=True, default=0.00)
    time_in_sunday = fields.Float(string="Hora de entrada", required=True, default=0.00)
    time_out_sunday = fields.Float(string="Hora de salida", required=True, default=0.00)
    min_limit = fields.Float(string="Mínimo minutos", required=True, default=0.00,
                             help="Valor mínimo utilizado para redondear la hora de trabajo, cualquier valor "
                                  "mayor o igual al especificado, se redondea hacia arriba, de lo contrario "
                                  "el redondeo es hacía abajo")
    max_limit = fields.Float(string="Máximo minutos", required=True, default=0.00,
                             help="Valor máximo utilizado para redondear la hora de trabajo, cualquier valor "
                                  "mayor o igual al especificado, se redondea hacia arriba, de lo contrario "
                                  "el redonde es hacía abajo")
    bonus_amount = fields.Float('Bono semanal', default=0.00, required=True)
    discount_amount = fields.Float('Descuento prestamo', default=0.00, required=True)
    active = fields.Boolean(string="Activo", default=True)

    @api.multi
    def _verify_times(self, vals):
        """
            :param vals: diccionario con valores a ser actualizados
            :param time_in: hora de entrada local, si no se modifico se toma la hora ya existente
            :param time_out: hora de salida local, si no se modifico se toma la hora ya existente

            return: valores a ser actualizados
        """
        # Validar si se modifico la hora de entrada y hora de salida
        time_in = self.time_in if 'time_in' not in vals else vals['time_in']
        time_out = self.time_out if 'time_out' not in vals else vals['time_out']
        time_in_sunday = self.time_in_sunday if 'time_in_sunday' not in vals else vals['time_in_sunday']
        time_out_sunday = self.time_out_sunday if 'time_out_sunday' not in vals else vals['time_out_sunday']
        # Validar si se modifico min_limit y max_limit
        min_limit = self.min_limit if 'min_limit' not in vals else vals['min_limit']
        max_limit = self.max_limit if 'max_limit' not in vals else vals['max_limit']
        # Validar el periodo de trabajo
        self._verify_time_error(time_in, time_out)
        self._verify_time_error(time_in_sunday, time_out_sunday)
        # Validar los limites de redondeo
        if min_limit >= 1 or max_limit >= 1:
            raise Warning("Los límites no pueden ser mayores a 1.")
        elif min_limit > max_limit:
            raise Warning("El límite mínimo no puede ser mayor al límite máximo.")
        elif min_limit < 0 or max_limit < 0:
            raise Warning("Los límites no pueden ser negativos")

    def _verify_time_error(self, time_in, time_out):
        """ Validar las horas de entrada y salida """
        if time_in < 0 or time_out < 0:
            raise Warning("No se permiten tiempos negativos")
        if time_in > time_out:
            raise Warning("La hora de entrada no puede ser mayor a la hora de salida")
        if time_in > 23.99 or time_out > 23.99:
            raise Warning("La hora ingresada no puede ser mayo a 23:59hr")

    @api.multi
    def write(self, vals):
        """ Validar las horas de entrada y salida antes de guardar los cambios """
        self._verify_times(vals)
        res = super(HrAttendanceConfig, self).write(vals)
        return res

    @api.model
    def create(self, vals):
        """ Validar las horas de entrada y salida antes de guardar por primera vez la lista de asistencia """
        self._verify_times(vals)
        res = super(HrAttendanceConfig, self).create(vals)
        return res


class HrConfigOrderEmployee(models.Model):
    _name = "hr.config.order.employee"
    _description = "Modelo que permite ordenar los empleados en las listas de asistencia"

    name = fields.Char(string="Tipo de empleado", required=True)
    active = fields.Boolean(string="Activo", default=True)
    attended = fields.Boolean(string="Marcar asistencia?")


class HrConfigPickingProduct(models.Model):
    """ Módelo para establecer los 3 productos para generar los gastos de la lista de asistencia,
        producto fresa, producto frambuesa y producto mano de obra. Solo puede estar activo un registro """
    _name = "hr.config.picking.product"
    _description = "Módelo que permite establecer los tres productos de lista de asistencia"

    name = fields.Char(string="Productos por defecto", required=True)
    active = fields.Boolean(string="Activo", default=True)
    product_straw_id = fields.Many2one("product.product", string="Producto fresa", required=True,
                                       domain=[('product_type_id.type', '=', 'sale')])
    box_straw_uom_id = fields.Many2one("product.uom", string="Unidad caja fresa", required=True)
    pot_straw_uom_id = fields.Many2one("product.uom", string="Unidad bote fresa", required=True)
    product_rasp_id = fields.Many2one("product.product", string="Producto frambuesa", required=True,
                                      domain=[('product_type_id.type', '=', 'sale')])
    box_rasp_uom_id = fields.Many2one("product.uom", string="Unidad caja frambuesa", required=True)
    pot_rasp_uom_id = fields.Many2one("product.uom", string="Unidad bote frambuesa", required=True)
    workforce_attended_id = fields.Many2one("product.product", string="Pago asistencia", required=True,
                                            domain=[('product_type_id.type', '=', 'workforce')])
    workforce_straw_box_id = fields.Many2one("product.product", string="Pago caja fresa", required=True,
                                             domain=[('product_type_id.type', '=', 'workforce')])
    workforce_rasp_box_id = fields.Many2one("product.product", string="Pago caja frambuesa", required=True,
                                            domain=[('product_type_id.type', '=', 'workforce')])
    workforce_straw_pot_id = fields.Many2one("product.product", string="Pago bote fresa", required=True,
                                             domain=[('product_type_id.type', '=', 'workforce')])
    workforce_rasp_pot_id = fields.Many2one("product.product", string="Pago bote frambuesa", required=True,
                                            domain=[('product_type_id.type', '=', 'workforce')])
    workforce_hour_id = fields.Many2one("product.product", string="Pago hora", required=True,
                                        domain=[('product_type_id.type', '=', 'workforce')])
    workforce_extra_hour_id = fields.Many2one("product.product", string="Pago hora extra", required=True,
                                              domain=[('product_type_id.type', '=', 'workforce')])
    warehouse_expense_id = fields.Many2one("stock.warehouse", string="Almacén origen", required=True,
                                           domain=[('is_estate', '=', False)])
    workforce_bonus_id = fields.Many2one("product.product", string="Pago bono", required=True,
                                             domain=[('product_type_id.type', '=', 'workforce')])
    workforce_extra_expense_id = fields.Many2one("product.product", string="Pago gasto extra", required=True,
                                             domain=[('product_type_id.type', '=', 'workforce')])
    notes = fields.Text("Notas", placeholder="Descripción o notas al respecto")

    @api.multi
    def get_straw_uom_domain(self, product_straw_id):
        """ Método que permite aplicar un filtro a las unidades de medida de la fresa para solo mostrar unidades
            de la misma categoría. """
        if product_straw_id:
            product_obj = self.env['product.product'].search([('id', '=', product_straw_id)])[0]
            uom_obj = self.env['product.uom'].search([('category_id', '=', product_obj.uom_id.category_id.id)])
            uom_ids = []
            for uom in uom_obj:
                uom_ids += [str(uom.id)]
            return {'domain': {'box_straw_uom_id': [('id', 'in', uom_ids)], 'pot_straw_uom_id': [('id', 'in', uom_ids)]},
                    'value': {'box_straw_uom_id': product_obj.uom_id.id, 'pot_straw_uom_id': product_obj.uom_id.id}}
        else:
            return {'value': {'box_straw_uom_id': None, 'pot_straw_uom_id': None}}

    @api.multi
    def get_rasp_uom_domain(self, product_rasp_id):
        """ Método que permite aplicar un filtro a las unidades de medida de la frambuesa, para solo mostrar
            unidades de la misma categoría. """
        if product_rasp_id:
            product_obj = self.env['product.product'].search([('id', '=', product_rasp_id)])[0]
            uom_obj = self.env['product.uom'].search([('category_id', '=', product_obj.uom_id.category_id.id)])
            uom_ids = []
            for uom in uom_obj:
                uom_ids += [str(uom.id)]
            return {'domain': {'box_rasp_uom_id': [('id', 'in', uom_ids)], 'pot_rasp_uom_id': [('id', 'in', uom_ids)]},
                    'value': {'box_rasp_uom_id': product_obj.uom_id.id, 'pot_rasp_uom_id': product_obj.uom_id.id}}
        else:
            return {'value': {'box_rasp_uom_id': None, 'pot_rasp_uom_id': None}}


class HrAttendanceActivityList(models.Model):
    _name = 'hr.attendance.activity.list'
    _description = 'Listado de actividades de la lista de asistencia'

    name = fields.Char('Actividad', required=True)
    active = fields.Boolean('Activo', default=True)

    @api.multi
    def unlink(self):
        attendance_obj = self.env['hr.attendance.gaa.monday']
        activities = attendance_obj.search([('activity_id', 'in', self.ids)])
        if not activities:
            attendance_obj = self.env['hr.attendance.gaa.tuesday']
            activities = attendance_obj.search([('activity_id', 'in', self.ids)])
        if not activities:
            attendance_obj = self.env['hr.attendance.gaa.wednesday']
            activities = attendance_obj.search([('activity_id', 'in', self.ids)])
        if not activities:
            attendance_obj = self.env['hr.attendance.gaa.thursday']
            activities = attendance_obj.search([('activity_id', 'in', self.ids)])
        if not activities:
            attendance_obj = self.env['hr.attendance.gaa.friday']
            activities = attendance_obj.search([('activity_id', 'in', self.ids)])
        if not activities:
            attendance_obj = self.env['hr.attendance.gaa.saturday']
            activities = attendance_obj.search([('activity_id', 'in', self.ids)])
        if not activities:
            attendance_obj = self.env['hr.attendance.gaa.sunday']
            activities = attendance_obj.search([('activity_id', 'in', self.ids)])

        if activities:
            raise Warning("No puede ser borrada una actividad que se encuentra referenciada en alguna lista de asistencia!")
        return super(HrAttendanceActivityList, self).unlink()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: