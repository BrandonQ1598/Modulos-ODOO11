# -*- coding: utf-8 -*-


from odoo import fields, models, api
from odoo.exceptions import Warning
from datetime import datetime, timedelta
from time import strptime
#from openerp import workflow


class HrAttendanceGaa(models.Model):
    _name = "hr.attendance.gaa"
    _inherit = ["mail.thread"]
    _description = "Lista de asistencia y corte"
    _order = "name desc"

    @api.multi
    def _get_time_in(self):
        config_obj = self.env['hr.attendance.config'].search([('active', '=', True)])
        if len(config_obj) == 1:
            return config_obj.time_in
        else:
            raise Warning(
                "No existe ningún registro de configuración. / Solo debe haber un registro de configuracion activo. Configurar en Recursos humanos > Configuracion > Personalizadas > Lista de asistencia")

    @api.multi
    def _get_time_out(self):
        config_obj = self.env['hr.attendance.config'].search([('active', '=', True)])
        if len(config_obj) == 1:
            return config_obj.time_out
        else:
            raise Warning(
                "No existe ningún registro de configuración. / Solo debe haber un registro de configuracion activo. Configurar en Recursos humanos > Configuracion > Personalizadas > Lista de asistencia")

    @api.multi
    def _get_time_in_sunday(self):
        config_obj = self.env['hr.attendance.config'].search([('active', '=', True)])
        if len(config_obj) == 1:
            return config_obj.time_in_sunday
        else:
            raise Warning(
                "No existe ningún registro de configuración. / Solo debe haber un registro de configuracion activo. Configurar en Recursos humanos > Configuracion > Personalizadas > Lista de asistencia")

    @api.multi
    def _get_time_out_sunday(self):
        config_obj = self.env['hr.attendance.config'].search([('active', '=', True)])
        if len(config_obj) == 1:
            return config_obj.time_out_sunday
        else:
            raise Warning(
                "No existe ningún registro de configuración. / Solo debe haber un registro de configuracion activo. Configurar en Recursos humanos > Configuracion > Personalizadas > Lista de asistencia")

    @api.multi
    def _get_bonus_amount(self):
        config_obj = self.env['hr.attendance.config'].search([('active', '=', True)])
        if len(config_obj) == 1:
            return config_obj.bonus_amount
        else:
            raise Warning(
                "No existe ningún registro de configuración. / Solo debe haber un registro de configuracion activo. Configurar en Recursos humanos > Configuracion > Personalizadas > Lista de asistencia")

    @api.multi
    def _get_discount_amount(self):
        config_obj = self.env['hr.attendance.config'].search([('active', '=', True)])
        if len(config_obj) == 1:
            return config_obj.discount_amount
        else:
            raise Warning(
                "No existe ningún registro de configuración. / Solo debe haber un registro de configuracion activo. Configurar en Recursos humanos > Configuracion > Personalizadas > Lista de asistencia")

    READONLY_ESTATES = {
        'confirmed': [('readonly', True)],
        'done': [('readonly', True)],
        'canceled': [('readonly', True)],
    }

    READONLY_ESTATES_COMPANY_SEASON = {
        'loaded': [('readonly', True)],
        'confirmed': [('readonly', True)],
        'done': [('readonly', True)],
        'canceled': [('readonly', True)],
    }

    READONLY_ESTATES_EMPLOYEES = {
        'draft': [('readonly', True)],
        'confirmed': [('readonly', True)],
        'done': [('readonly', True)],
        'canceled': [('readonly', True)],
    }

    def _get_attendance_number(self):
        sequence = self.env['ir.sequence'].next_by_code('hr.attendance.gaa')
        return sequence

    name = fields.Char(string="Nombre", readonly=True)
    reference = fields.Char(string="Referencia")
    monday_employees_ids = fields.One2many("hr.attendance.gaa.monday", "attendance_id", string="Empleados lunes",
                                           states=READONLY_ESTATES_EMPLOYEES)
    tuesday_employees_ids = fields.One2many("hr.attendance.gaa.tuesday", "attendance_id", string="Empleados martes",
                                            states=READONLY_ESTATES_EMPLOYEES)
    wednesday_employees_ids = fields.One2many("hr.attendance.gaa.wednesday", "attendance_id",
                                              string="Empleados miércoles", states=READONLY_ESTATES_EMPLOYEES)
    thursday_employees_ids = fields.One2many("hr.attendance.gaa.thursday", "attendance_id", string="Empleados jueves",
                                             states=READONLY_ESTATES_EMPLOYEES)
    friday_employees_ids = fields.One2many("hr.attendance.gaa.friday", "attendance_id", string="Empleados viernes",
                                           states=READONLY_ESTATES_EMPLOYEES)
    sunday_employees_ids = fields.One2many("hr.attendance.gaa.sunday", "attendance_id", string="Empleados domingo",
                                           states=READONLY_ESTATES_EMPLOYEES)
    saturday_employees_ids = fields.One2many("hr.attendance.gaa.saturday", "attendance_id", string="Empleados sábado",
                                             states=READONLY_ESTATES_EMPLOYEES)
    resume = fields.One2many("hr.attendance.gaa.resume", "attendance_id", string="Resumen",
                             states=READONLY_ESTATES_EMPLOYEES)
    company_hg_id = fields.Many2one("res.company.hg", string="Empresa", required=True,
                                    states=READONLY_ESTATES_COMPANY_SEASON)
    company_id = fields.Many2one("res.company", string="Empresa", default=lambda self: self.env.user.company_id.id)
    season_id = fields.Many2one("stock.estate.season", string="Temporada", required=True,
                                domain=[('state', 'in', ['open'])], states=READONLY_ESTATES_COMPANY_SEASON)
    user_id = fields.Many2one("res.users", string="Usuario", default=lambda self: self.env.user, readonly=True)
    date_from = fields.Date(string="Inicio", required=True, select=1, states=READONLY_ESTATES_COMPANY_SEASON)
    date_to = fields.Date(string="Final", required=True, compute='_onchange_date_from', readonly=True)
    time_in = fields.Float(string="Hora de entrada", required=True, default=_get_time_in,
                           states=READONLY_ESTATES_COMPANY_SEASON)
    time_out = fields.Float(string="Hora de salida", required=True, default=_get_time_out,
                            states=READONLY_ESTATES_COMPANY_SEASON)
    time_in_sunday = fields.Float(string="Hora de entrada", required=True, default=_get_time_in_sunday,
                                  states=READONLY_ESTATES_COMPANY_SEASON)
    time_out_sunday = fields.Float(string="Hora de salida", required=True, default=_get_time_out_sunday,
                                   states=READONLY_ESTATES_COMPANY_SEASON)
    bonus_amount = fields.Float('Bono semanal', required=True, default=_get_bonus_amount)
    discount_amount = fields.Float('Descuento prestamo', required=True, default=_get_discount_amount)
    note = fields.Text(string="Notas")
    default_crop_id = fields.Many2one("stock.estate.crop", string="Cultivo por defecto", required=True,
                                      domain=[('state', 'in', ['open'])])
    # Campo utilizado para agregar al empleado en todos los días.
    employee_id = fields.Many2one('hr.employee', 'Empleado', states=READONLY_ESTATES)
    thursday_date = fields.Date('Jueves')
    friday_date = fields.Date('Viernes')
    saturday_date = fields.Date('Sábado')
    sunday_date = fields.Date('Domingo')
    monday_date = fields.Date('Lunes')
    tuesday_date = fields.Date('Martes')
    wednesday_date = fields.Date('Miércoles')

    # Ocultar/mostrar columnas
    hide_columns = fields.Boolean(string='Ocultar columnas', default=False)

    state = fields.Selection([
        ('draft', "Borrador"),
        ('loaded', "Generada"),
        ('confirmed', "Aprobada"),
        ('done', "Realizada"),
        ('canceled', "Cancelada"),
    ], string="Estado", default='draft')

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         'El nombre de la lista de asistencia debe ser único'),
    ]

    @api.model
    def fields_view_get(self, view_id=None, view_type=False, toolbar=False, submenu=False):
        attendance = False
        params = self.env.context.get('params', False)
        if params:
            attendance_id = params.get('id', False)
            if attendance_id:
                attendance = self.browse(attendance_id)

        if attendance and attendance.hide_columns:
            self = self.with_context(hide_columns=True)

        result = super(HrAttendanceGaa, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                              submenu=submenu)
        return result

    @api.model
    def create(self, vals):
        seq = self._get_attendance_number()
        vals['name'] = seq
        res = super(HrAttendanceGaa, self).create(vals)
        return res

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_confirmed(self):
        # Calcular el resumen del trabajo semanal
        self.calculate()
        if self._check_empty_attended():
            raise Warning("No se puede confirmar una lista que todos los totales sean cero (0).")
        # Confirmar la lista de asistencia
        self.state = 'confirmed'

    def _check_empty_attended(self):
        total = 0
        for resume in self.resume:
            total += resume.total_attended + resume.total_boxes_rasp1 + resume.total_boxes_straw1 + resume.total_pots_rasp1 \
                     + resume.total_pots_straw1 + resume.total_boxes_rasp2 + resume.total_boxes_straw2 + resume.total_pots_rasp2 \
                     + resume.total_pots_straw2 + resume.total_boxes_rasp3 + resume.total_boxes_straw3 + resume.total_pots_rasp3 \
                     + resume.total_pots_straw3 + resume.total_hours + resume.total_extra_expense + resume.total_extra_hours

        if total <= 0:
            return True
        else:
            return False

    @api.multi
    def action_done(self):
        self.state = 'done'

    @api.multi
    def action_canceled(self):
        # Validar si la lista fue utilizada para generar nómina
        payslip_obj = self.env['hr.payslip'].search([('hr_attendance_id', '=', self.id), ('state', '=', 'done')])
        if len(payslip_obj) > 0:
            raise Warning(
                "No puede cancelarse una lista de asistencia que haya sido utilizada para la generación de nómina.")

        # Verificar que esten cancelados primero los movimientos de cosecha
        harvest_obj = self.env['stock.estate.harvest'].search([('attendance_id', '=', self.ids[0])])
        for harvest in harvest_obj:
            if harvest.state != 'canceled':
                raise Warning("Primero deben ser cancelados todos los movimientos de cosecha.")
        self.state = 'canceled'

    @api.onchange('date_from')
    @api.one
    def _onchange_date_from(self):
        if self.date_from:
            self.date_to = datetime(*strptime(self.date_from, "%Y-%m-%d")[0:6]) + timedelta(days=6)
            self.thursday_date = self.date_from
            self.friday_date = datetime.strptime(self.date_from, "%Y-%m-%d") + timedelta(days=1)
            self.saturday_date = datetime.strptime(self.date_from, "%Y-%m-%d") + timedelta(days=2)
            self.sunday_date = datetime.strptime(self.date_from, "%Y-%m-%d") + timedelta(days=3)
            self.monday_date = datetime.strptime(self.date_from, "%Y-%m-%d") + timedelta(days=4)
            self.tuesday_date = datetime.strptime(self.date_from, "%Y-%m-%d") + timedelta(days=5)
            self.wednesday_date = self.date_to

    @api.onchange('time_in', 'time_out', 'time_in_sunday', 'time_out_sunday')
    def _verify_times(self):
        if self.time_in < 0 or self.time_out < 0 or self.time_in_sunday < 0 or self.time_out_sunday < 0:
            raise Warning("No se permiten tiempos negativos")
        if (self.time_in > self.time_out and self.time_out != 00.00) or (self.time_in_sunday > self.time_out_sunday and self.time_out != 00.00):
            raise Warning("La hora de entrada no puede ser mayor a la hora de salida")
        if self.time_in > 23.99 or self.time_out > 23.99 or self.time_in_sunday > 23.00 or self.time_out_sunday > 23.99:
            raise Warning("La hora ingresada no puede ser mayor a 23:59hr")

    @api.multi
    def unlink(self):
        for attendance in self:
            if attendance.state not in ['draft', 'canceled', 'loaded']:
                raise Warning("No se puede borrar una lista de asistencia confirmada o realizada")
        return super(HrAttendanceGaa, self).unlink()

    @api.multi
    def write(self, vals):
        vals['employee_id'] = None
        return super(HrAttendanceGaa, self).write(vals)

    def validate_dates(self):
        # Validar que la fecha de inicio no sea mayor a la fecha final
        if datetime(*strptime(self.date_to, "%Y-%m-%d")[0:6]) < datetime(*strptime(self.date_from, "%Y-%m-%d")[0:6]):
            raise Warning("Error en el rango de fecha, la fecha final no puede ser mayor a la fecha de inicio")
        # Validar que el rango sea igual a una semana
        if (datetime(*strptime(self.date_from, "%Y-%m-%d")[0:6]) + timedelta(days=6)) != datetime(
                *strptime(self.date_to, "%Y-%m-%d")[0:6]):
            raise Warning("El rango de fechas debe ser igual a una semana. La fecha de termino debería ser: " + (
                        datetime(*strptime(self.date_from, "%Y-%m-%d")[0:6]) + timedelta(days=6)).strftime("%d/%m/%Y"))

    @api.multi
    def get_domain_default_crop(self, season_id):
        if season_id:
            return {'domain': {'default_crop_id': [('season_id', '=', season_id)]},
                    'value': {'default_crop_id': None}}
        else:
            return {'value': {'default_crop_id': None}}

    def _exist_employees(self):
        if not self.monday_employees_ids or not self.tuesday_employees_ids \
                or not self.wednesday_employees_ids or not self.thursday_employees_ids \
                or not self.friday_employees_ids or not self.saturday_employees_ids \
                or not self.sunday_employees_ids:
            raise Warning("No puede marcase como generada una lista de asistencia sin empleados.")

    # @api.multi
    # def change_to_loaded(self):
    #    self._exist_employees()
    #    self.action_loaded(0)
    #    return True

    @api.multi
    def action_loaded(self):
        """
        @param employees: todos los usuarios activos en el sistema
        @param employee: usuario individual para lectura del id del empleado
        :return:
        """
        self.validate_dates()
        self._verify_times()
        try:
            if not self.default_crop_id:
                raise Warning("Se requiere específicar un cultivo por defecto.")
            employees = self.env["hr.employee"].search(
                [('active', '=', True), ('company_hg_id', '=', self.company_hg_id.id)])
            count = len(employees)
            if count < 0:
                raise Warning('No existen empleados activos para agregar')

            # Recorrido de todos los empleados
            for employee in employees:
                row = {
                    'name': employee.id, 'employee_type': employee.employee_type.id, 'attendance_id': self.id,
                    'attended': employee.employee_type.attended, 'season_id': self.season_id.id,
                    'attended_crop_id': None, 'time_in': self.time_in, 'time_out': self.time_out,
                    # Corte de cultivo 1
                    'boxes_rasp1': 0, 'boxes_straw1': 0, 'pots_rasp1': 0, 'pots_straw1': 0, 'boxes_pots_crop_id1': None,
                    # Corte de cultivo 2
                    'boxes_rasp2': 0, 'boxes_straw2': 0, 'pots_rasp2': 0, 'pots_straw2': 0, 'boxes_pots_crop_id2': None,
                    # Corte de cultivo 3
                    'boxes_rasp3': 0, 'boxes_straw3': 0, 'pots_rasp3': 0, 'pots_straw3': 0, 'boxes_pots_crop_id3': None,
                    'hours': 0, 'hours_crop_id': None, 'extra_hours': 0, 'extra_hours_crop_id': None,
                    'date_from': self.date_from,'date_to': self.date_to,
                }
                # Si la asistencia se marca, establecer el cultivo por defecto
                if row['attended']:
                    row['attended_crop_id'] = self.default_crop_id.id
                id_reg = self.env['hr.attendance.gaa.wednesday'].create(row)
                row['date'] = self.date_from
                id_reg = self.env['hr.attendance.gaa.thursday'].create(row)
                row['date'] = datetime.strptime(self.date_from, "%Y-%m-%d") + timedelta(days=1)
                id_reg = self.env['hr.attendance.gaa.friday'].create(row)
                row['date'] = datetime.strptime(self.date_from, "%Y-%m-%d") + timedelta(days=2)
                id_reg = self.env['hr.attendance.gaa.saturday'].create(row)
                row['date'] = datetime.strptime(self.date_from, "%Y-%m-%d") + timedelta(days=4)
                id_reg = self.env['hr.attendance.gaa.monday'].create(row)
                row['date'] = datetime.strptime(self.date_from, "%Y-%m-%d") + timedelta(days=5)
                id_reg = self.env['hr.attendance.gaa.tuesday'].create(row)
                # Ajustar horario de entrada del día domingo
                row['time_in'] = self.time_in_sunday
                row['time_out'] = self.time_out_sunday
                row['attended'] = False
                # Establecer el cultivo por defecto vacío, ya que en domingo no hay asistencia
                row['attended_crop_id'] = None

                row['date'] = datetime.strptime(self.date_from, "%Y-%m-%d") + timedelta(days=3)
                id_reg = self.env['hr.attendance.gaa.sunday'].create(row)
                row = {
                    'name': employee.id, 'employee_type': employee.employee_type.id, 'attendance_id': self.id,
                    'weekly_bonus': self.bonus_amount, 'loan_discount': self.discount_amount,
                    # Total corte de cultivo 1
                    'total_boxes_rasp1': 0, 'total_boxes_straw1': 0, 'total_pots_rasp1': 0, 'total_pots_straw1': 0,
                    # Total corte de cultivo 2
                    'total_boxes_rasp2': 0, 'total_boxes_straw2': 0, 'total_pots_rasp2': 0, 'total_pots_straw2': 0,
                    # Total corte de cultivo 3
                    'total_boxes_rasp3': 0, 'total_boxes_straw3': 0, 'total_pots_rasp3': 0, 'total_pots_straw3': 0,
                    'total_hours': 0, 'total_extra_hours': 0, 'date': self.date_from,'date_to': self.date_to,
                }
                id_reg = self.env['hr.attendance.gaa.resume'].create(row)
            self.state = 'loaded'
        except:
            raise Warning("Error al cargar los empleados.")

    @api.one
    def calculate(self):
        try:
            for x in range(len(self.resume)):
                # Inicializar los totales
                self.resume[x].total_attended = 0
                # Resumento cultivo 1
                self.resume[x].total_boxes_rasp1 = 0
                self.resume[x].total_boxes_straw1 = 0
                self.resume[x].total_pots_rasp1 = 0
                self.resume[x].total_pots_straw1 = 0
                # Resumento cultivo 2
                self.resume[x].total_boxes_rasp2 = 0
                self.resume[x].total_boxes_straw2 = 0
                self.resume[x].total_pots_rasp2 = 0
                self.resume[x].total_pots_straw2 = 0
                # Resumento cultivo 3
                self.resume[x].total_boxes_rasp3 = 0
                self.resume[x].total_boxes_straw3 = 0
                self.resume[x].total_pots_rasp3 = 0
                self.resume[x].total_pots_straw3 = 0
                self.resume[x].total_hours = 0
                self.resume[x].total_extra_hours = 0
                self.resume[x].total_extra_expense = 0

                for y in range(len(self.resume)):
                    # Monday
                    if self.resume[x].name.id == self.monday_employees_ids[y].name.id:
                        if self.monday_employees_ids[y].attended:
                            self.resume[x].total_attended += 1
                        # Resumento cultivo 1
                        self.resume[x].total_boxes_rasp1 += self.monday_employees_ids[y].boxes_rasp1
                        self.resume[x].total_boxes_straw1 += self.monday_employees_ids[y].boxes_straw1
                        self.resume[x].total_pots_rasp1 += self.monday_employees_ids[y].pots_rasp1
                        self.resume[x].total_pots_straw1 += self.monday_employees_ids[y].pots_straw1
                        # Resumento cultivo 2
                        self.resume[x].total_boxes_rasp2 += self.monday_employees_ids[y].boxes_rasp2
                        self.resume[x].total_boxes_straw2 += self.monday_employees_ids[y].boxes_straw2
                        self.resume[x].total_pots_rasp2 += self.monday_employees_ids[y].pots_rasp2
                        self.resume[x].total_pots_straw2 += self.monday_employees_ids[y].pots_straw2
                        # Resumento cultivo 3
                        self.resume[x].total_boxes_rasp3 += self.monday_employees_ids[y].boxes_rasp3
                        self.resume[x].total_boxes_straw3 += self.monday_employees_ids[y].boxes_straw3
                        self.resume[x].total_pots_rasp3 += self.monday_employees_ids[y].pots_rasp3
                        self.resume[x].total_pots_straw3 += self.monday_employees_ids[y].pots_straw3
                        self.resume[x].total_hours += self.monday_employees_ids[y].hours
                        self.resume[x].total_extra_hours += self.monday_employees_ids[y].extra_hours
                        self.resume[x].total_extra_expense += self.monday_employees_ids[y].extra_expense
                        self.monday_employees_ids[y].date = (
                                    datetime(*strptime(self.date_from, "%Y-%m-%d")[0:6]) + timedelta(days=3)).strftime(
                            "%Y-%m-%d")
                    # Tuesday
                    if self.resume[x].name.id == self.tuesday_employees_ids[y].name.id:
                        if self.tuesday_employees_ids[y].attended:
                            self.resume[x].total_attended += 1
                        # Resumen cultivo 1
                        self.resume[x].total_boxes_rasp1 += self.tuesday_employees_ids[y].boxes_rasp1
                        self.resume[x].total_boxes_straw1 += self.tuesday_employees_ids[y].boxes_straw1
                        self.resume[x].total_pots_rasp1 += self.tuesday_employees_ids[y].pots_rasp1
                        self.resume[x].total_pots_straw1 += self.tuesday_employees_ids[y].pots_straw1
                        # Resumen cultivo 2
                        self.resume[x].total_boxes_rasp2 += self.tuesday_employees_ids[y].boxes_rasp2
                        self.resume[x].total_boxes_straw2 += self.tuesday_employees_ids[y].boxes_straw2
                        self.resume[x].total_pots_rasp2 += self.tuesday_employees_ids[y].pots_rasp2
                        self.resume[x].total_pots_straw2 += self.tuesday_employees_ids[y].pots_straw2
                        # Resumen cultivo 3
                        self.resume[x].total_boxes_rasp3 += self.tuesday_employees_ids[y].boxes_rasp3
                        self.resume[x].total_boxes_straw3 += self.tuesday_employees_ids[y].boxes_straw3
                        self.resume[x].total_pots_rasp3 += self.tuesday_employees_ids[y].pots_rasp3
                        self.resume[x].total_pots_straw3 += self.tuesday_employees_ids[y].pots_straw3
                        self.resume[x].total_hours += self.tuesday_employees_ids[y].hours
                        self.resume[x].total_extra_hours += self.tuesday_employees_ids[y].extra_hours
                        self.resume[x].total_extra_expense += self.tuesday_employees_ids[y].extra_expense
                        self.tuesday_employees_ids[y].date = (
                                    datetime(*strptime(self.date_from, "%Y-%m-%d")[0:6]) + timedelta(days=5)).strftime(
                            "%Y-%m-%d")
                    # Wednesday
                    if self.resume[x].name.id == self.wednesday_employees_ids[y].name.id:
                        if self.wednesday_employees_ids[y].attended:
                            self.resume[x].total_attended += 1
                        # Resumen cultivo 1
                        self.resume[x].total_boxes_rasp1 += self.wednesday_employees_ids[y].boxes_rasp1
                        self.resume[x].total_boxes_straw1 += self.wednesday_employees_ids[y].boxes_straw1
                        self.resume[x].total_pots_rasp1 += self.wednesday_employees_ids[y].pots_rasp1
                        self.resume[x].total_pots_straw1 += self.wednesday_employees_ids[y].pots_straw1
                        # Resumen cultivo 2
                        self.resume[x].total_boxes_rasp2 += self.wednesday_employees_ids[y].boxes_rasp2
                        self.resume[x].total_boxes_straw2 += self.wednesday_employees_ids[y].boxes_straw2
                        self.resume[x].total_pots_rasp2 += self.wednesday_employees_ids[y].pots_rasp2
                        self.resume[x].total_pots_straw2 += self.wednesday_employees_ids[y].pots_straw2
                        # Resumen cultivo 3
                        self.resume[x].total_boxes_rasp3 += self.wednesday_employees_ids[y].boxes_rasp3
                        self.resume[x].total_boxes_straw3 += self.wednesday_employees_ids[y].boxes_straw3
                        self.resume[x].total_pots_rasp3 += self.wednesday_employees_ids[y].pots_rasp3
                        self.resume[x].total_pots_straw3 += self.wednesday_employees_ids[y].pots_straw3
                        self.resume[x].total_hours += self.wednesday_employees_ids[y].hours
                        self.resume[x].total_extra_hours += self.wednesday_employees_ids[y].extra_hours
                        self.resume[x].total_extra_expense += self.wednesday_employees_ids[y].extra_expense
                        self.wednesday_employees_ids[y].date = self.date_to
                    # Thursday
                    if self.resume[x].name.id == self.thursday_employees_ids[y].name.id:
                        if self.thursday_employees_ids[y].attended:
                            self.resume[x].total_attended += 1
                        # Resumen cultivo 1
                        self.resume[x].total_boxes_rasp1 += self.thursday_employees_ids[y].boxes_rasp1
                        self.resume[x].total_boxes_straw1 += self.thursday_employees_ids[y].boxes_straw1
                        self.resume[x].total_pots_rasp1 += self.thursday_employees_ids[y].pots_rasp1
                        self.resume[x].total_pots_straw1 += self.thursday_employees_ids[y].pots_straw1
                        # Resumen cultivo 2
                        self.resume[x].total_boxes_rasp2 += self.thursday_employees_ids[y].boxes_rasp2
                        self.resume[x].total_boxes_straw2 += self.thursday_employees_ids[y].boxes_straw2
                        self.resume[x].total_pots_rasp2 += self.thursday_employees_ids[y].pots_rasp2
                        self.resume[x].total_pots_straw2 += self.thursday_employees_ids[y].pots_straw2
                        # Resumen cultivo 3
                        self.resume[x].total_boxes_rasp3 += self.thursday_employees_ids[y].boxes_rasp3
                        self.resume[x].total_boxes_straw3 += self.thursday_employees_ids[y].boxes_straw3
                        self.resume[x].total_pots_rasp3 += self.thursday_employees_ids[y].pots_rasp3
                        self.resume[x].total_pots_straw3 += self.thursday_employees_ids[y].pots_straw3
                        self.resume[x].total_hours += self.thursday_employees_ids[y].hours
                        self.resume[x].total_extra_hours += self.thursday_employees_ids[y].extra_hours
                        self.resume[x].total_extra_expense += self.thursday_employees_ids[y].extra_expense
                        self.thursday_employees_ids[y].date = self.date_from
                    # Friday
                    if self.resume[x].name.id == self.friday_employees_ids[y].name.id:
                        if self.friday_employees_ids[y].attended:
                            self.resume[x].total_attended += 1
                        # Resumen cultivo 1
                        self.resume[x].total_boxes_rasp1 += self.friday_employees_ids[y].boxes_rasp1
                        self.resume[x].total_boxes_straw1 += self.friday_employees_ids[y].boxes_straw1
                        self.resume[x].total_pots_rasp1 += self.friday_employees_ids[y].pots_rasp1
                        self.resume[x].total_pots_straw1 += self.friday_employees_ids[y].pots_straw1
                        # Resumen cultivo 2
                        self.resume[x].total_boxes_rasp2 += self.friday_employees_ids[y].boxes_rasp2
                        self.resume[x].total_boxes_straw2 += self.friday_employees_ids[y].boxes_straw2
                        self.resume[x].total_pots_rasp2 += self.friday_employees_ids[y].pots_rasp2
                        self.resume[x].total_pots_straw2 += self.friday_employees_ids[y].pots_straw2
                        # Resumen cultivo 3
                        self.resume[x].total_boxes_rasp3 += self.friday_employees_ids[y].boxes_rasp3
                        self.resume[x].total_boxes_straw3 += self.friday_employees_ids[y].boxes_straw3
                        self.resume[x].total_pots_rasp3 += self.friday_employees_ids[y].pots_rasp3
                        self.resume[x].total_pots_straw3 += self.friday_employees_ids[y].pots_straw3
                        self.resume[x].total_hours += self.friday_employees_ids[y].hours
                        self.resume[x].total_extra_hours += self.friday_employees_ids[y].extra_hours
                        self.resume[x].total_extra_expense += self.friday_employees_ids[y].extra_expense
                        self.friday_employees_ids[y].date = (
                                    datetime(*strptime(self.date_from, "%Y-%m-%d")[0:6]) + timedelta(days=1)).strftime(
                            "%Y-%m-%d")
                    # Saturday
                    if self.resume[x].name.id == self.saturday_employees_ids[y].name.id:
                        if self.saturday_employees_ids[y].attended:
                            self.resume[x].total_attended += 1
                        # Resumen cultivo 1
                        self.resume[x].total_boxes_rasp1 += self.saturday_employees_ids[y].boxes_rasp1
                        self.resume[x].total_boxes_straw1 += self.saturday_employees_ids[y].boxes_straw1
                        self.resume[x].total_pots_rasp1 += self.saturday_employees_ids[y].pots_rasp1
                        self.resume[x].total_pots_straw1 += self.saturday_employees_ids[y].pots_straw1
                        # Resumen cultivo 2
                        self.resume[x].total_boxes_rasp2 += self.saturday_employees_ids[y].boxes_rasp2
                        self.resume[x].total_boxes_straw2 += self.saturday_employees_ids[y].boxes_straw2
                        self.resume[x].total_pots_rasp2 += self.saturday_employees_ids[y].pots_rasp2
                        self.resume[x].total_pots_straw2 += self.saturday_employees_ids[y].pots_straw2
                        # Resumen cultivo 3
                        self.resume[x].total_boxes_rasp3 += self.saturday_employees_ids[y].boxes_rasp3
                        self.resume[x].total_boxes_straw3 += self.saturday_employees_ids[y].boxes_straw3
                        self.resume[x].total_pots_rasp3 += self.saturday_employees_ids[y].pots_rasp3
                        self.resume[x].total_pots_straw3 += self.saturday_employees_ids[y].pots_straw3
                        self.resume[x].total_hours += self.saturday_employees_ids[y].hours
                        self.resume[x].total_extra_hours += self.saturday_employees_ids[y].extra_hours
                        self.resume[x].total_extra_expense += self.saturday_employees_ids[y].extra_expense
                        self.saturday_employees_ids[y].date = (
                                    datetime(*strptime(self.date_from, "%Y-%m-%d")[0:6]) + timedelta(days=2)).strftime(
                            "%Y-%m-%d")
                    # Sunday
                    if self.resume[x].name.id == self.sunday_employees_ids[y].name.id:
                        if self.sunday_employees_ids[y].attended:
                            self.resume[x].total_attended += 1
                        # Resumen cultivo 1
                        self.resume[x].total_boxes_rasp1 += self.sunday_employees_ids[y].boxes_rasp1
                        self.resume[x].total_boxes_straw1 += self.sunday_employees_ids[y].boxes_straw1
                        self.resume[x].total_pots_rasp1 += self.sunday_employees_ids[y].pots_rasp1
                        self.resume[x].total_pots_straw1 += self.sunday_employees_ids[y].pots_straw1
                        # Resumen cultivo 2
                        self.resume[x].total_boxes_rasp2 += self.sunday_employees_ids[y].boxes_rasp2
                        self.resume[x].total_boxes_straw2 += self.sunday_employees_ids[y].boxes_straw2
                        self.resume[x].total_pots_rasp2 += self.sunday_employees_ids[y].pots_rasp2
                        self.resume[x].total_pots_straw2 += self.sunday_employees_ids[y].pots_straw2
                        # Resumen cultivo 3
                        self.resume[x].total_boxes_rasp3 += self.sunday_employees_ids[y].boxes_rasp3
                        self.resume[x].total_boxes_straw3 += self.sunday_employees_ids[y].boxes_straw3
                        self.resume[x].total_pots_rasp3 += self.sunday_employees_ids[y].pots_rasp3
                        self.resume[x].total_pots_straw3 += self.sunday_employees_ids[y].pots_straw3
                        self.resume[x].total_hours += self.sunday_employees_ids[y].hours
                        self.resume[x].total_extra_hours += self.sunday_employees_ids[y].extra_hours
                        self.resume[x].total_extra_expense += self.sunday_employees_ids[y].extra_expense
                        self.sunday_employees_ids[y].date = (
                                    datetime(*strptime(self.date_from, "%Y-%m-%d")[0:6]) + timedelta(days=3)).strftime(
                            "%Y-%m-%d")
        except:
            raise Warning("Error al realizar la sumatoria. Verifique que los empleados que hayan sido \
                agregados manualmente, se encuentren en cada uno de los días de la semana.")

    @api.multi
    def add_employee(self):
        """ Método para agregar un nuevo empleado en todos los días de la lista de asistencia. """
        # Validar que se haya seleccionado un empleado para agregar
        if not self._context['employee_id']:
            raise Warning('Error!, debe seleccionar un empleado para poderlo agregar')
        # Verificamos si el empleado existe en alguno de los días de la semana
        self.exists_employee_by_day()

        # Saber que tipo de empleado es para marcar o no la asistencia
        employee_obj = self.env['hr.employee'].search([('id', '=', self._context['employee_id'])])[0]

        # Agregar empleado en el resumen
        data = {
            'attendance_id': self.id,
            'name': self._context['employee_id'],
        }
        if not self.env['hr.attendance.gaa.resume'].create(data):
            raise Warning('Se produjo un error al intentar agregar el empleado a la pestaña Resumen.')
        # Valores para el día domingo
        data['season_id'] = self.season_id.id
        data['time_in'] = self.time_in_sunday
        data['time_out'] = self.time_out_sunday
        # Valores para cualquier día de la semana
        if employee_obj.employee_type.attended:
            data['attended'] = True
        else:
            data['attended'] = False
        data['employee_type'] = employee_obj.employee_type.id

        if not self.env['hr.attendance.gaa.sunday'].create(data):
            raise Warning('Se produjo un error al intentar agregar el empleado el día Domingo.')
        # Horario de entrada de Lunes - Sabado
        data['time_in'] = self.time_in
        data['time_out'] = self.time_out

        if not self.env['hr.attendance.gaa.monday'].create(data):
            raise Warning('Se produjo un error al intentar agregar el empleado el día Lunes.')
        if not self.env['hr.attendance.gaa.tuesday'].create(data):
            raise Warning('Se produjo un error al intentar agregar el empleado el día Martes.')
        if not self.env['hr.attendance.gaa.wednesday'].create(data):
            raise Warning('Se produjo un error al intentar agregar el empleado el día Miércoles.')
        if not self.env['hr.attendance.gaa.thursday'].create(data):
            raise Warning('Se produjo un error al intentar agregar el empleado el día Jueves.')
        if not self.env['hr.attendance.gaa.friday'].create(data):
            raise Warning('Se produjo un error al intentar agregar el empleado el día Viernes.')
        if not self.env['hr.attendance.gaa.saturday'].create(data):
            raise Warning('Se produjo un error al intentar agregar el empleado el día Sábado.')

    def exists_employee_by_day(self):
        """ Método para verificar si el empleado no se encuentra agregado ya en la lista de asistencia validar
            día por día """
        if self.monday_employees_ids.search_count(
                [('attendance_id', '=', self.id), ('name', '=', self._context.get('employee_id'))]) > 0:
            raise Warning('El empleado ya existe en el día Lunes de la lista de asistencia')
        if self.tuesday_employees_ids.search_count(
                [('attendance_id', '=', self.id), ('name', '=', self._context.get('employee_id'))]) > 0:
            raise Warning('El empleado ya existe en el día Martes de la lista de asistencia')
        if self.wednesday_employees_ids.search_count(
                [('attendance_id', '=', self.id), ('name', '=', self._context.get('employee_id'))]) > 0:
            raise Warning('El empleado ya existe en el día Miércoles de la lista de asistencia')
        if self.thursday_employees_ids.search_count(
                [('attendance_id', '=', self.id), ('name', '=', self._context.get('employee_id'))]) > 0:
            raise Warning('El empleado ya existe en el día Jueves de la lista de asistencia')
        if self.friday_employees_ids.search_count(
                [('attendance_id', '=', self.id), ('name', '=', self._context.get('employee_id'))]) > 0:
            raise Warning('El empleado ya existe en el día Viernes de la lista de asistencia')
        if self.saturday_employees_ids.search_count(
                [('attendance_id', '=', self.id), ('name', '=', self._context.get('employee_id'))]) > 0:
            raise Warning('El empleado ya existe en el día Sabado de la lista de asistencia')
        if self.sunday_employees_ids.search_count(
                [('attendance_id', '=', self.id), ('name', '=', self._context.get('employee_id'))]) > 0:
            raise Warning('El empleado ya existe en el día Domingo de la lista de asistencia')
        if self.resume.search_count([('attendance_id', '=', self.id), ('name', '=', self.env.context.get('employee_id'))]) > 0:
            raise Warning('El empleado ya existe en el Resumen de la lista de asistencia')

    @api.one
    def count_employees(self):
        days = {
            'sun': 0, 'mon': 0, 'tue': 0, 'wed': 0, 'thu': 0, 'fri': 0, 'sat': 0, 'res': 0
        }

        days['sun'] = self.sunday_employees_ids.search_count([('attendance_id', '=', self.id)])
        days['mon'] = self.monday_employees_ids.search_count([('attendance_id', '=', self.id)])
        days['tue'] = self.tuesday_employees_ids.search_count([('attendance_id', '=', self.id)])
        days['wed'] = self.wednesday_employees_ids.search_count([('attendance_id', '=', self.id)])
        days['thu'] = self.thursday_employees_ids.search_count([('attendance_id', '=', self.id)])
        days['fri'] = self.friday_employees_ids.search_count([('attendance_id', '=', self.id)])
        days['sat'] = self.saturday_employees_ids.search_count([('attendance_id', '=', self.id)])
        days['res'] = self.resume.search_count([('attendance_id', '=', self.id)])

        total = days['sun'] + days['mon'] + days['tue'] + days['wed'] + \
                days['thu'] + days['fri'] + days['sat']

        raise Warning('Total de empleados Lunes - Domingo: ' + str(total) + '\n Lunes: ' + str(days['mon']) +
                      '\n Martes: ' + str(days['tue']) + '\n Miércoles: ' + str(days['wed']) +
                      '\n Jueves: ' + str(days['thu']) + '\n Viernes: ' + str(days['fri']) +
                      '\n Sábado: ' + str(days['sat']) + '\n Domingo: ' + str(days['sun']) +
                      '\n Resumen: ' + str(days['res']))


    def remove_employee(self):
        """ Método para quitar un empleados de todos los días de la lista de asistencia """
        # Validar que se haya seleccionado un empleado para agregar
        if not self.employee_id:
            raise Warning('Error!, debe seleccionar un empleado para poderlo quitarlo de la lista de asistencia')
        self.monday_employees_ids.search(
            [('attendance_id', '=', self.id), ('name', '=', self._context['employee_id'])]).unlink()
        self.tuesday_employees_ids.search(
            [('attendance_id', '=', self.id), ('name', '=', self._context['employee_id'])]).unlink()
        self.wednesday_employees_ids.search(
            [('attendance_id', '=', self.id), ('name', '=', self._context['employee_id'])]).unlink()
        self.thursday_employees_ids.search(
            [('attendance_id', '=', self.id), ('name', '=', self._context['employee_id'])]).unlink()
        self.friday_employees_ids.search(
            [('attendance_id', '=', self.id), ('name', '=', self._context['employee_id'])]).unlink()
        self.saturday_employees_ids.search(
            [('attendance_id', '=', self.id), ('name', '=', self._context['employee_id'])]).unlink()
        self.sunday_employees_ids.search(
            [('attendance_id', '=', self.id), ('name', '=', self._context['employee_id'])]).unlink()
        self.resume.search([('attendance_id', '=', self.id), ('name', '=', self._context['employee_id'])]).unlink()


# Lunes
class HrAttendanceGaaMonday(models.Model):
    _name = "hr.attendance.gaa.monday"
    _description = "Empleados de la lista de asistencia lunes"
    _order = "employee_type, name"

    name = fields.Many2one("hr.employee", string="Empleado")
    employee_type = fields.Many2one("hr.config.order.employee", string="Tipo de empleado")
    season_id = fields.Many2one("stock.estate.season", string="Temporada")
    attendance_id = fields.Many2one("hr.attendance.gaa", string="Lista de asistencia", ondelete='cascade')
    attended = fields.Boolean(string="Asist.", default=True)
    attended_crop_id = fields.Many2one("stock.estate.crop", string="Cultivo 1", domain=[('state', 'in', ['open'])])
    time_in = fields.Float(string="Entrada", required=True)
    time_out = fields.Float(string="Salida", required=True)
    # Corte cultivo 1
    boxes_rasp1 = fields.Integer(string="C. Fra", default=0)
    boxes_straw1 = fields.Integer(string="C. Fre", default=0)
    pots_rasp1 = fields.Integer(string="B. Fra", default=0)
    pots_straw1 = fields.Integer(string="B. Fre", default=0)
    boxes_pots_crop_id1 = fields.Many2one("stock.estate.crop", string="Cultivo 2", domain=[('state', 'in', ['open'])])
    # Corte cultivo 2
    boxes_rasp2 = fields.Integer(string="C. Fra", default=0)
    boxes_straw2 = fields.Integer(string="C. Fre", default=0)
    pots_rasp2 = fields.Integer(string="B. Fra", default=0)
    pots_straw2 = fields.Integer(string="B. Fre", default=0)
    boxes_pots_crop_id2 = fields.Many2one("stock.estate.crop", string="Cultivo 3", domain=[('state', 'in', ['open'])])
    # Corte cultivo 3
    boxes_rasp3 = fields.Integer(string="C. Fra", default=0)
    boxes_straw3 = fields.Integer(string="C. Fre", default=0)
    pots_rasp3 = fields.Integer(string="B. Fra", default=0)
    pots_straw3 = fields.Integer(string="B. Fre", default=0)
    boxes_pots_crop_id3 = fields.Many2one("stock.estate.crop", string="Cultivo 4", domain=[('state', 'in', ['open'])])
    hours = fields.Float(string="Hrs.", default=0, readonly=True)
    hours_crop_id = fields.Many2one("stock.estate.crop", string="Cultivo 5", domain=[('state', 'in', ['open'])])
    extra_hours = fields.Float(string="H. extra", default=0, readonly=True)
    extra_hours_crop_id = fields.Many2one("stock.estate.crop", string="Cultivo 6", domain=[('state', 'in', ['open'])])
    comments = fields.Text(string="Actividades", readonly=True)
    # activity_id = fields.Many2many('hr.attendance.activity.list', 'hr_attendance_activity_rel', 'attendance_id', 'activity_id', 'Actividades')
    activity_id = fields.Many2one('hr.attendance.activity.list', 'Actividad')
    extra_activity_id = fields.Many2one('hr.attendance.activity.list', 'Actividad Extra')
    date = fields.Date(string="Fecha")
    # Utilizado para ordenar los registros
    sequence = fields.Integer('Secuencia')
    extra_expense = fields.Float(string='Gasto extra')
    extra_expense_activity_id = fields.Many2one('hr.attendance.activity.list', string='Justificación')
    extra_expense_estate_id = fields.Many2one('stock.estate.crop', string="Cult. gasto extra",
                                              domain=[('state', 'in', ['open'])])

    @api.multi
    def _verify_times(self, vals):
        # Validar si se modifico la hora de entrada y hora de salida
        time_in = self.time_in if ('time_in' not in vals) else vals['time_in']
        time_out = self.time_out if 'time_out' not in vals else vals['time_out']
        if time_in < 0 or time_out < 0:
            raise Warning("No se permiten tiempos negativos")
        if time_in > time_out:
            raise Warning("La hora de entrada no puede ser mayor a la hora de salida")
        if time_in > 23.99 or time_out > 23.99:
            raise Warning("La hora ingresada no puede ser mayor a 23:59hr")

    @api.multi
    def write(self, vals):
        self._verify_times(vals=vals)
        res = super(HrAttendanceGaaMonday, self).write(vals)
        return res

    @api.model
    def create(self, vals):
        season_id = self.env['hr.attendance.gaa'].search([('id', '=', vals['attendance_id'])])[0].season_id.id
        vals['season_id'] = season_id
        res = super(HrAttendanceGaaMonday, self).create(vals)
        return res

    def _round_time(self, min_limit, max_limit, time_worked):
        # Verificar si se cumple el mínimo o máximo de segundos
        minutes = time_worked - float((str(time_worked).split('.'))[0])
        horas = time_worked - minutes
        if minutes >= min_limit and minutes < max_limit:
            time_worked = horas + 0.50
        elif minutes >= max_limit:
            time_worked = horas + 1
        else:
            time_worked = horas
        return time_worked

    @api.multi
    def calculate_hours(self, vals):
        # Verificar los rangos de las horas
        self._verify_times(vals=vals)
        if int(vals['time_in']) <= 0 or int(vals['time_out']) <= 0:
            return
        time_in = vals['time_in']
        time_out = vals['time_out']
        time_obj = self.attendance_id
        time_limits_obj = self.env['hr.attendance.config'].search([('active', '=', True)])
        # Horas de trabajo por día establecidas por la empresa
        hours_per_day = time_obj.time_out - time_obj.time_in
        time_worked_normal = 0.00
        time_worked_extra = 0.00
        # Validar horas normales
        if time_in <= time_obj.time_out:
            if time_out <= time_obj.time_out:
                if time_in < time_obj.time_in:
                    time_worked_normal = time_out - time_obj.time_in
                else:
                    time_worked_normal = time_out - time_in
            elif time_in < time_obj.time_in:
                time_worked_normal = time_obj.time_out - time_obj.time_in
            else:
                time_worked_normal = time_obj.time_out - time_in

        # Validar horas extra
        if time_in > time_obj.time_out:
            time_worked_extra = time_out - time_in
        else:
            if time_out > time_obj.time_out:
                time_worked_extra = time_out - time_obj.time_out
            if time_in < time_obj.time_in:
                time_worked_extra += time_obj.time_in - time_in

        # Redondear las horas normales y horas extra
        time_worked_normal = self._round_time(time_limits_obj.min_limit, time_limits_obj.max_limit, time_worked_normal)
        time_worked_extra = self._round_time(time_limits_obj.min_limit, time_limits_obj.max_limit, time_worked_extra)

        # Determinar si se marca la asistencia de acuerdo si cumplio el horario establecido
        attended = False
        if time_worked_normal >= hours_per_day:
            attended = True
            time_worked_normal -= hours_per_day

        return {'value': {
            'attended': attended,
            'hours': time_worked_normal,
            'extra_hours': time_worked_extra, }}

    @api.multi
    def set_default_crop(self, opc, br=0, bs=0, pr=0, ps=0, attended=None, h=0, xh=0):
        """ Método para establecer el cultivo por defecto automáticamente de acuerdo ciertas validaciones
            br= box_rasp, bs=box_straw, pr=pots_rasp, ps=pots_straw, h=hours, xh=extra_hours"""
        # Verificar si tiene o no asistencia, en este caso ps=asistencia o no
        if opc == 1:
            if attended:
                return {'value': {'attended_crop_id': self.attendance_id.default_crop_id.id}}
            else:
                return {'value': {'attended_crop_id': None}}
        # Verificar si hay corte en alguno de los 3 cultivos
        elif 1 < opc < 5:
            if br + bs + pr + ps > 0:
                if opc == 2:
                    return {'value': {'boxes_pots_crop_id1': self.attendance_id.default_crop_id.id}}
                elif opc == 3:
                    return {'value': {'boxes_pots_crop_id2': self.attendance_id.default_crop_id.id}}
                elif opc == 4:
                    return {'value': {'boxes_pots_crop_id3': self.attendance_id.default_crop_id.id}}
            else:
                if opc == 2:
                    return {'value': {'boxes_pots_crop_id1': None}}
                elif opc == 3:
                    return {'value': {'boxes_pots_crop_id2': None}}
                elif opc == 4:
                    return {'value': {'boxes_pots_crop_id3': None}}
        # Verificar si hay o no horas de trabajo
        elif opc == 5:
            if h > 0:
                return {'value': {'hours_crop_id': self.attendance_id.default_crop_id.id}}
            else:
                return {'value': {'hours_crop_id': None}}
        # Verificar si hay o no horas extras
        elif opc == 6:
            if xh > 0:
                return {'value': {'extra_hours_crop_id': self.attendance_id.default_crop_id.id}}
            else:
                return {'value': {'extra_hours_crop_id': None}}


# Martes
class HrAttendanceGaaTuesday(models.Model):
    _name = "hr.attendance.gaa.tuesday"
    _description = "Empleados de la lista de asistencia martes"
    _order = "employee_type, name"

    name = fields.Many2one("hr.employee", string="Empleado")
    employee_type = fields.Many2one("hr.config.order.employee", string="Tipo de empleado")
    season_id = fields.Many2one("stock.estate.season", string="Temporada")
    attendance_id = fields.Many2one("hr.attendance.gaa", string="Lista de asistencia", ondelete='cascade')
    attended = fields.Boolean(string="Asist.", default=True)
    attended_crop_id = fields.Many2one("stock.estate.crop", string="Cultivo 1", domain=[('state', 'in', ['open'])])
    time_in = fields.Float(string="Entrada", required=True)
    time_out = fields.Float(string="Salida", required=True)
    # Corte cultivo 1
    boxes_rasp1 = fields.Integer(string="C. Fra", default=0)
    boxes_straw1 = fields.Integer(string="C. Fre", default=0)
    pots_rasp1 = fields.Integer(string="B. Fra", default=0)
    pots_straw1 = fields.Integer(string="B. Fre", default=0)
    boxes_pots_crop_id1 = fields.Many2one("stock.estate.crop", string="Cultivo 2", domain=[('state', 'in', ['open'])])
    # Corte cultivo 2
    boxes_rasp2 = fields.Integer(string="C. Fra", default=0)
    boxes_straw2 = fields.Integer(string="C. Fre", default=0)
    pots_rasp2 = fields.Integer(string="B. Fra", default=0)
    pots_straw2 = fields.Integer(string="B. Fre", default=0)
    boxes_pots_crop_id2 = fields.Many2one("stock.estate.crop", string="Cultivo 3", domain=[('state', 'in', ['open'])])
    # Corte cultivo 3
    boxes_rasp3 = fields.Integer(string="C. Fra", default=0)
    boxes_straw3 = fields.Integer(string="C. Fre", default=0)
    pots_rasp3 = fields.Integer(string="B. Fra", default=0)
    pots_straw3 = fields.Integer(string="B. Fre", default=0)
    boxes_pots_crop_id3 = fields.Many2one("stock.estate.crop", string="Cultivo 4", domain=[('state', 'in', ['open'])])
    hours = fields.Float(string="Hrs", default=0, readonly=True)
    hours_crop_id = fields.Many2one("stock.estate.crop", string="Cultivo 5", domain=[('state', 'in', ['open'])])
    extra_hours = fields.Float(string="H. extra", default=0, readonly=True)
    extra_hours_crop_id = fields.Many2one("stock.estate.crop", string="Cultivo 6", domain=[('state', 'in', ['open'])])
    comments = fields.Text(string="Actividades", readonly=True)
    # activity_id = fields.Many2many('hr.attendance.activity.list', 'hr_attendance_activity_rel', 'attendance_id', 'activity_id', 'Actividades')
    activity_id = fields.Many2one('hr.attendance.activity.list', 'Actividad')
    extra_activity_id = fields.Many2one('hr.attendance.activity.list', 'Actividad Extra')
    date = fields.Date(string="Fecha")
    # Utilizado para ordenar los registros
    sequence = fields.Integer('Secuencia')
    extra_expense = fields.Float(string='Gasto extra')
    extra_expense_activity_id = fields.Many2one('hr.attendance.activity.list', string='Justificación')
    extra_expense_estate_id = fields.Many2one('stock.estate.crop', string="Cult. gasto extra",
                                              domain=[('state', 'in', ['open'])])

    @api.multi
    def _verify_times(self, vals):
        # Validar si se modifico la hora de entrada y hora de salida
        time_in = self.time_in if ('time_in' not in vals) else vals['time_in']
        time_out = self.time_out if 'time_out' not in vals else vals['time_out']
        if time_in < 0 or time_out < 0:
            raise Warning("No se permiten tiempos negativos")
        if time_in > time_out:
            raise Warning("La hora de entrada no puede ser mayor a la hora de salida")
        if time_in > 23.99 or time_out > 23.99:
            raise Warning("La hora ingresada no puede ser mayor a 23:59hr")

    @api.multi
    def write(self, vals):
        self._verify_times(vals=vals)
        res = super(HrAttendanceGaaTuesday, self).write(vals)
        return res

    @api.model
    def create(self, vals):
        season_id = self.env['hr.attendance.gaa'].search([('id', '=', vals['attendance_id'])])[0].season_id.id
        vals['season_id'] = season_id
        res = super(HrAttendanceGaaTuesday, self).create(vals)
        return res

    def _round_time(self, min_limit, max_limit, time_worked):
        # Verificar si se cumple el mínimo o máximo de segundos
        minutes = time_worked - float((str(time_worked).split('.'))[0])
        horas = time_worked - minutes
        if minutes >= min_limit and minutes < max_limit:
            time_worked = horas + 0.50
        elif minutes >= max_limit:
            time_worked = horas + 1
        else:
            time_worked = horas
        return time_worked

    @api.multi
    def calculate_hours(self, vals):
        # Verificar los rangos de las horas
        self._verify_times(vals=vals)
        if int(vals['time_in']) <= 0 or int(vals['time_out']) <= 0:
            return
        time_in = vals['time_in']
        time_out = vals['time_out']
        time_obj = self.attendance_id
        time_limits_obj = self.env['hr.attendance.config'].search([('active', '=', True)])
        # Horas de trabajo por día establecidas por la empresa
        hours_per_day = time_obj.time_out - time_obj.time_in
        time_worked_normal = 0.00
        time_worked_extra = 0.00
        # Validar horas normales
        if time_in <= time_obj.time_out:
            if time_out <= time_obj.time_out:
                if time_in < time_obj.time_in:
                    time_worked_normal = time_out - time_obj.time_in
                else:
                    time_worked_normal = time_out - time_in
            elif time_in < time_obj.time_in:
                time_worked_normal = time_obj.time_out - time_obj.time_in
            else:
                time_worked_normal = time_obj.time_out - time_in

        # Validar horas extra
        if time_in > time_obj.time_out:
            time_worked_extra = time_out - time_in
        else:
            if time_out > time_obj.time_out:
                time_worked_extra = time_out - time_obj.time_out
            if time_in < time_obj.time_in:
                time_worked_extra += time_obj.time_in - time_in

        # Redondear las horas normales y horas extra
        time_worked_normal = self._round_time(time_limits_obj.min_limit, time_limits_obj.max_limit, time_worked_normal)
        time_worked_extra = self._round_time(time_limits_obj.min_limit, time_limits_obj.max_limit, time_worked_extra)

        # Determinar si se marca la asistencia de acuerdo si cumplio el horario establecido
        attended = False
        if time_worked_normal >= hours_per_day:
            attended = True
            time_worked_normal -= hours_per_day

        return {'value': {
            'attended': attended,
            'hours': time_worked_normal,
            'extra_hours': time_worked_extra, }}

    @api.multi
    def set_default_crop(self, opc, br=0, bs=0, pr=0, ps=0, attended=None, h=0, xh=0):
        """ Método para establecer el cultivo por defecto automáticamente de acuerdo ciertas validaciones
            br= box_rasp, bs=box_straw, pr=pots_rasp, ps=pots_straw, h=hours, xh=extra_hours"""
        # Verificar si tiene o no asistencia, en este caso ps=asistencia o no
        if opc == 1:
            if attended:
                return {'value': {'attended_crop_id': self.attendance_id.default_crop_id.id}}
            else:
                return {'value': {'attended_crop_id': None}}
        # Verificar si hay corte en alguno de los 3 cultivos
        elif 1 < opc < 5:
            if br + bs + pr + ps > 0:
                if opc == 2:
                    return {'value': {'boxes_pots_crop_id1': self.attendance_id.default_crop_id.id}}
                elif opc == 3:
                    return {'value': {'boxes_pots_crop_id2': self.attendance_id.default_crop_id.id}}
                elif opc == 4:
                    return {'value': {'boxes_pots_crop_id3': self.attendance_id.default_crop_id.id}}
            else:
                if opc == 2:
                    return {'value': {'boxes_pots_crop_id1': None}}
                elif opc == 3:
                    return {'value': {'boxes_pots_crop_id2': None}}
                elif opc == 4:
                    return {'value': {'boxes_pots_crop_id3': None}}
        # Verificar si hay o no horas de trabajo
        elif opc == 5:
            if h > 0:
                return {'value': {'hours_crop_id': self.attendance_id.default_crop_id.id}}
            else:
                return {'value': {'hours_crop_id': None}}
        # Verificar si hay o no horas extras
        elif opc == 6:
            if xh > 0:
                return {'value': {'extra_hours_crop_id': self.attendance_id.default_crop_id.id}}
            else:
                return {'value': {'extra_hours_crop_id': None}}


# Miercoles
class HrAttendanceGaaWednesday(models.Model):
    _name = "hr.attendance.gaa.wednesday"
    _description = "Empleados de la lista de asistencia miercoles"
    _order = "employee_type, name"

    name = fields.Many2one("hr.employee", string="Empleado")
    employee_type = fields.Many2one("hr.config.order.employee", string="Tipo de empleado")
    season_id = fields.Many2one("stock.estate.season", string="Temporada")
    attendance_id = fields.Many2one("hr.attendance.gaa", string="Lista de asistencia", ondelete='cascade')
    attended = fields.Boolean(string="Asist.", default=True)
    attended_crop_id = fields.Many2one("stock.estate.crop", string="Cultivo 1", domain=[('state', 'in', ['open'])])
    time_in = fields.Float(string="Entrada", required=True)
    time_out = fields.Float(string="Salida", required=True)
    # Corte cultivo 1
    boxes_rasp1 = fields.Integer(string="C. Fra", default=0)
    boxes_straw1 = fields.Integer(string="C. Fre", default=0)
    pots_rasp1 = fields.Integer(string="B. Fra", default=0)
    pots_straw1 = fields.Integer(string="B. Fre", default=0)
    boxes_pots_crop_id1 = fields.Many2one("stock.estate.crop", string="Cultivo 2", domain=[('state', 'in', ['open'])])
    # Corte cultivo 2
    boxes_rasp2 = fields.Integer(string="C. Fra", default=0)
    boxes_straw2 = fields.Integer(string="C. Fre", default=0)
    pots_rasp2 = fields.Integer(string="B. Fra", default=0)
    pots_straw2 = fields.Integer(string="B. Fre", default=0)
    boxes_pots_crop_id2 = fields.Many2one("stock.estate.crop", string="Cultivo 3", domain=[('state', 'in', ['open'])])
    # Corte cultivo 3
    boxes_rasp3 = fields.Integer(string="C. Fra", default=0)
    boxes_straw3 = fields.Integer(string="C. Fre", default=0)
    pots_rasp3 = fields.Integer(string="B. Fra", default=0)
    pots_straw3 = fields.Integer(string="B. Fre", default=0)
    boxes_pots_crop_id3 = fields.Many2one("stock.estate.crop", string="Cultivo 4", domain=[('state', 'in', ['open'])])
    hours = fields.Float(string="Hrs.", default=0, readonly=True)
    hours_crop_id = fields.Many2one("stock.estate.crop", string="Cultivo 5", domain=[('state', 'in', ['open'])])
    extra_hours = fields.Float(string="H. extra", default=0, readonly=True)
    extra_hours_crop_id = fields.Many2one("stock.estate.crop", string="Cultivo 6", domain=[('state', 'in', ['open'])])
    comments = fields.Text(string="Actividades", readonly=True)
    # activity_id = fields.Many2many('hr.attendance.activity.list', 'hr_attendance_activity_rel', 'attendance_id', 'activity_id', 'Actividades')
    activity_id = fields.Many2one('hr.attendance.activity.list', 'Actividad')
    extra_activity_id = fields.Many2one('hr.attendance.activity.list', 'Actividad Extra')
    date = fields.Date(string="Fecha")
    # Utilizado para ordenar los registros
    sequence = fields.Integer('Secuencia')
    extra_expense = fields.Float(string='Gasto extra')
    extra_expense_activity_id = fields.Many2one('hr.attendance.activity.list', string='Justificación')
    extra_expense_estate_id = fields.Many2one('stock.estate.crop', string="Cult. gasto extra",
                                              domain=[('state', 'in', ['open'])])

    @api.multi
    def _verify_times(self, vals):
        # Validar si se modifico la hora de entrada y hora de salida
        time_in = self.time_in if ('time_in' not in vals) else vals['time_in']
        time_out = self.time_out if 'time_out' not in vals else vals['time_out']
        if time_in < 0 or time_out < 0:
            raise Warning("No se permiten tiempos negativos")
        if time_in > time_out:
            raise Warning("La hora de entrada no puede ser mayor a la hora de salida")
        if time_in > 23.99 or time_out > 23.99:
            raise Warning("La hora ingresada no puede ser mayor a 23:59hr")

    @api.multi
    def write(self, vals):
        self._verify_times(vals=vals)
        res = super(HrAttendanceGaaWednesday, self).write(vals)
        return res

    @api.model
    def create(self, vals):
        season_id = self.env['hr.attendance.gaa'].search([('id', '=', vals['attendance_id'])])[0].season_id.id
        vals['season_id'] = season_id
        res = super(HrAttendanceGaaWednesday, self).create(vals)
        return res

    def _round_time(self, min_limit, max_limit, time_worked):
        # Verificar si se cumple el mínimo o máximo de segundos
        minutes = time_worked - float((str(time_worked).split('.'))[0])
        horas = time_worked - minutes
        if minutes >= min_limit and minutes < max_limit:
            time_worked = horas + 0.50
        elif minutes >= max_limit:
            time_worked = horas + 1
        else:
            time_worked = horas
        return time_worked

    @api.multi
    def calculate_hours(self, vals):
        # Verificar los rangos de las horas
        self._verify_times(vals=vals)
        if int(vals['time_in']) <= 0 or int(vals['time_out']) <= 0:
            return
        time_in = vals['time_in']
        time_out = vals['time_out']
        time_obj = self.attendance_id
        time_limits_obj = self.env['hr.attendance.config'].search([('active', '=', True)])
        # Horas de trabajo por día establecidas por la empresa
        hours_per_day = time_obj.time_out - time_obj.time_in
        time_worked_normal = 0.00
        time_worked_extra = 0.00
        # Validar horas normales
        if time_in <= time_obj.time_out:
            if time_out <= time_obj.time_out:
                if time_in < time_obj.time_in:
                    time_worked_normal = time_out - time_obj.time_in
                else:
                    time_worked_normal = time_out - time_in
            elif time_in < time_obj.time_in:
                time_worked_normal = time_obj.time_out - time_obj.time_in
            else:
                time_worked_normal = time_obj.time_out - time_in

        # Validar horas extra
        if time_in > time_obj.time_out:
            time_worked_extra = time_out - time_in
        else:
            if time_out > time_obj.time_out:
                time_worked_extra = time_out - time_obj.time_out
            if time_in < time_obj.time_in:
                time_worked_extra += time_obj.time_in - time_in

        # Redondear las horas normales y horas extra
        time_worked_normal = self._round_time(time_limits_obj.min_limit, time_limits_obj.max_limit, time_worked_normal)
        time_worked_extra = self._round_time(time_limits_obj.min_limit, time_limits_obj.max_limit, time_worked_extra)

        # Determinar si se marca la asistencia de acuerdo si cumplio el horario establecido
        attended = False
        if time_worked_normal >= hours_per_day:
            attended = True
            time_worked_normal -= hours_per_day

        return {'value': {
            'attended': attended,
            'hours': time_worked_normal,
            'extra_hours': time_worked_extra, }}

    @api.multi
    def set_default_crop(self, opc, br=0, bs=0, pr=0, ps=0, attended=None, h=0, xh=0):
        """ Método para establecer el cultivo por defecto automáticamente de acuerdo ciertas validaciones
            br= box_rasp, bs=box_straw, pr=pots_rasp, ps=pots_straw, h=hours, xh=extra_hours"""
        # Verificar si tiene o no asistencia, en este caso ps=asistencia o no
        if opc == 1:
            if attended:
                return {'value': {'attended_crop_id': self.attendance_id.default_crop_id.id}}
            else:
                return {'value': {'attended_crop_id': None}}
        # Verificar si hay corte en alguno de los 3 cultivos
        elif 1 < opc < 5:
            if br + bs + pr + ps > 0:
                if opc == 2:
                    return {'value': {'boxes_pots_crop_id1': self.attendance_id.default_crop_id.id}}
                elif opc == 3:
                    return {'value': {'boxes_pots_crop_id2': self.attendance_id.default_crop_id.id}}
                elif opc == 4:
                    return {'value': {'boxes_pots_crop_id3': self.attendance_id.default_crop_id.id}}
            else:
                if opc == 2:
                    return {'value': {'boxes_pots_crop_id1': None}}
                elif opc == 3:
                    return {'value': {'boxes_pots_crop_id2': None}}
                elif opc == 4:
                    return {'value': {'boxes_pots_crop_id3': None}}
        # Verificar si hay o no horas de trabajo
        elif opc == 5:
            if h > 0:
                return {'value': {'hours_crop_id': self.attendance_id.default_crop_id.id}}
            else:
                return {'value': {'hours_crop_id': None}}
        # Verificar si hay o no horas extras
        elif opc == 6:
            if xh > 0:
                return {'value': {'extra_hours_crop_id': self.attendance_id.default_crop_id.id}}
            else:
                return {'value': {'extra_hours_crop_id': None}}


# Jueves
class HrAttendanceGaaThursday(models.Model):
    _name = "hr.attendance.gaa.thursday"
    _description = "Empleados de la lista de asistencia jueves"
    _order = "employee_type, name"

    name = fields.Many2one("hr.employee", string="Empleado")
    employee_type = fields.Many2one("hr.config.order.employee", string="Tipo de empleado")
    season_id = fields.Many2one("stock.estate.season", string="Temporada")
    attendance_id = fields.Many2one("hr.attendance.gaa", string="Lista de asistencia", ondelete='cascade')
    attended = fields.Boolean(string="Asist.", default=True)
    attended_crop_id = fields.Many2one("stock.estate.crop", string="Cultivo 1", domain=[('state', 'in', ['open'])])
    time_in = fields.Float(string="Entrada", required=True)
    time_out = fields.Float(string="Salida", required=True)
    # Corte cultivo 1
    boxes_rasp1 = fields.Integer(string="C. Fra", default=0)
    boxes_straw1 = fields.Integer(string="C. Fre", default=0)
    pots_rasp1 = fields.Integer(string="B. Fra", default=0)
    pots_straw1 = fields.Integer(string="B. Fre", default=0)
    boxes_pots_crop_id1 = fields.Many2one("stock.estate.crop", string="Cultivo 2", domain=[('state', 'in', ['open'])])
    # Corte cultivo 2
    boxes_rasp2 = fields.Integer(string="C. Fra", default=0)
    boxes_straw2 = fields.Integer(string="C. Fre", default=0)
    pots_rasp2 = fields.Integer(string="B. Fra", default=0)
    pots_straw2 = fields.Integer(string="B. Fre", default=0)
    boxes_pots_crop_id2 = fields.Many2one("stock.estate.crop", string="Cultivo 3", domain=[('state', 'in', ['open'])])
    # Corte cultivo 3
    boxes_rasp3 = fields.Integer(string="C. Fra", default=0)
    boxes_straw3 = fields.Integer(string="C. Fre", default=0)
    pots_rasp3 = fields.Integer(string="B. Fra", default=0)
    pots_straw3 = fields.Integer(string="B. Fre", default=0)
    boxes_pots_crop_id3 = fields.Many2one("stock.estate.crop", string="Cultivo 4", domain=[('state', 'in', ['open'])])
    hours = fields.Float(string="Hrs.", default=0, readonly=True)
    hours_crop_id = fields.Many2one("stock.estate.crop", string="Cultivo 5", domain=[('state', 'in', ['open'])])
    extra_hours = fields.Float(string="H. extra", default=0, readonly=True)
    extra_hours_crop_id = fields.Many2one("stock.estate.crop", string="Cultivo 6", domain=[('state', 'in', ['open'])])
    comments = fields.Text(string="Actividades", readonly=True)
    # activity_id = fields.Many2many('hr.attendance.activity.list', 'hr_attendance_activity_rel', 'attendance_id', 'activity_id', 'Actividades')
    activity_id = fields.Many2one('hr.attendance.activity.list', 'Actividad')
    extra_activity_id = fields.Many2one('hr.attendance.activity.list', 'Actividad Extra')
    date = fields.Date(string="Fecha")
    # Utilizado para ordenar los registros
    sequence = fields.Integer('Secuencia')
    extra_expense = fields.Float(string='Gasto extra')
    extra_expense_activity_id = fields.Many2one('hr.attendance.activity.list', string='Justificación')
    extra_expense_estate_id = fields.Many2one('stock.estate.crop', string="Cult. gasto extra",
                                              domain=[('state', 'in', ['open'])])

    @api.multi
    def _verify_times(self, vals):
        # Validar si se modifico la hora de entrada y hora de salida
        time_in = self.time_in if ('time_in' not in vals) else vals['time_in']
        time_out = self.time_out if 'time_out' not in vals else vals['time_out']
        if time_in < 0 or time_out < 0:
            raise Warning("No se permiten tiempos negativos")
        if time_in > time_out:
            raise Warning("La hora de entrada no puede ser mayor a la hora de salida")
        if time_in > 23.99 or time_out > 23.99:
            raise Warning("La hora ingresada no puede ser mayor a 23:59hr")

    @api.multi
    def write(self, vals):
        self._verify_times(vals=vals)
        res = super(HrAttendanceGaaThursday, self).write(vals)
        return res

    @api.model
    def create(self, vals):
        season_id = self.env['hr.attendance.gaa'].search([('id', '=', vals['attendance_id'])])[0].season_id.id
        vals['season_id'] = season_id
        res = super(HrAttendanceGaaThursday, self).create(vals)
        return res

    def _round_time(self, min_limit, max_limit, time_worked):
        # Verificar si se cumple el mínimo o máximo de segundos
        minutes = time_worked - float((str(time_worked).split('.'))[0])
        horas = time_worked - minutes
        if minutes >= min_limit and minutes < max_limit:
            time_worked = horas + 0.50
        elif minutes >= max_limit:
            time_worked = horas + 1
        else:
            time_worked = horas
        return time_worked

    @api.multi
    def calculate_hours(self, vals):
        # Verificar los rangos de las horas
        self._verify_times(vals=vals)
        if int(vals['time_in']) <= 0 or int(vals['time_out']) <= 0:
            return
        time_in = vals['time_in']
        time_out = vals['time_out']
        time_obj = self.attendance_id
        time_limits_obj = self.env['hr.attendance.config'].search([('active', '=', True)])
        # Horas de trabajo por día establecidas por la empresa
        hours_per_day = time_obj.time_out - time_obj.time_in
        time_worked_normal = 0.00
        time_worked_extra = 0.00
        # Validar horas normales
        if time_in <= time_obj.time_out:
            if time_out <= time_obj.time_out:
                if time_in < time_obj.time_in:
                    time_worked_normal = time_out - time_obj.time_in
                else:
                    time_worked_normal = time_out - time_in
            elif time_in < time_obj.time_in:
                time_worked_normal = time_obj.time_out - time_obj.time_in
            else:
                time_worked_normal = time_obj.time_out - time_in

        # Validar horas extra
        if time_in > time_obj.time_out:
            time_worked_extra = time_out - time_in
        else:
            if time_out > time_obj.time_out:
                time_worked_extra = time_out - time_obj.time_out
            if time_in < time_obj.time_in:
                time_worked_extra += time_obj.time_in - time_in

        # Redondear las horas normales y horas extra
        time_worked_normal = self._round_time(time_limits_obj.min_limit, time_limits_obj.max_limit, time_worked_normal)
        time_worked_extra = self._round_time(time_limits_obj.min_limit, time_limits_obj.max_limit, time_worked_extra)

        # Determinar si se marca la asistencia de acuerdo si cumplio el horario establecido
        attended = False
        if time_worked_normal >= hours_per_day:
            attended = True
            time_worked_normal -= hours_per_day

        return {'value': {
            'attended': attended,
            'hours': time_worked_normal,
            'extra_hours': time_worked_extra, }}

    @api.multi
    def set_default_crop(self, opc, br=0, bs=0, pr=0, ps=0, attended=None, h=0, xh=0):
        """ Método para establecer el cultivo por defecto automáticamente de acuerdo ciertas validaciones
            br= box_rasp, bs=box_straw, pr=pots_rasp, ps=pots_straw, h=hours, xh=extra_hours"""
        # Verificar si tiene o no asistencia, en este caso ps=asistencia o no
        if opc == 1:
            if attended:
                return {'value': {'attended_crop_id': self.attendance_id.default_crop_id.id}}
            else:
                return {'value': {'attended_crop_id': None}}
        # Verificar si hay corte en alguno de los 3 cultivos
        elif 1 < opc < 5:
            if br + bs + pr + ps > 0:
                if opc == 2:
                    return {'value': {'boxes_pots_crop_id1': self.attendance_id.default_crop_id.id}}
                elif opc == 3:
                    return {'value': {'boxes_pots_crop_id2': self.attendance_id.default_crop_id.id}}
                elif opc == 4:
                    return {'value': {'boxes_pots_crop_id3': self.attendance_id.default_crop_id.id}}
            else:
                if opc == 2:
                    return {'value': {'boxes_pots_crop_id1': None}}
                elif opc == 3:
                    return {'value': {'boxes_pots_crop_id2': None}}
                elif opc == 4:
                    return {'value': {'boxes_pots_crop_id3': None}}
        # Verificar si hay o no horas de trabajo
        elif opc == 5:
            if h > 0:
                return {'value': {'hours_crop_id': self.attendance_id.default_crop_id.id}}
            else:
                return {'value': {'hours_crop_id': None}}
        # Verificar si hay o no horas extras
        elif opc == 6:
            if xh > 0:
                return {'value': {'extra_hours_crop_id': self.attendance_id.default_crop_id.id}}
            else:
                return {'value': {'extra_hours_crop_id': None}}


# Viernes
class HrAttendanceGaaFriday(models.Model):
    _name = "hr.attendance.gaa.friday"
    _description = "Empleados de la lista de asistencia viernes"
    _order = "employee_type, name"

    name = fields.Many2one("hr.employee", string="Empleado")
    employee_type = fields.Many2one("hr.config.order.employee", string="Tipo de empleado")
    season_id = fields.Many2one("stock.estate.season", string="Temporada")
    attendance_id = fields.Many2one("hr.attendance.gaa", string="Lista de asistencia", ondelete='cascade')
    attended = fields.Boolean(string="Asist.", default=True)
    attended_crop_id = fields.Many2one("stock.estate.crop", string="Cultivo 1", domain=[('state', 'in', ['open'])])
    time_in = fields.Float(string="Entrada", required=True)
    time_out = fields.Float(string="Salida", required=True)
    # Corte cultivo 1
    boxes_rasp1 = fields.Integer(string="C. Fra", default=0)
    boxes_straw1 = fields.Integer(string="C. Fre", default=0)
    pots_rasp1 = fields.Integer(string="B. Fra", default=0)
    pots_straw1 = fields.Integer(string="B. Fre", default=0)
    boxes_pots_crop_id1 = fields.Many2one("stock.estate.crop", string="Cultivo 2", domain=[('state', 'in', ['open'])])
    # Corte cultivo 2
    boxes_rasp2 = fields.Integer(string="C. Fra", default=0)
    boxes_straw2 = fields.Integer(string="C. Fre", default=0)
    pots_rasp2 = fields.Integer(string="B. Fra", default=0)
    pots_straw2 = fields.Integer(string="B. Fre", default=0)
    boxes_pots_crop_id2 = fields.Many2one("stock.estate.crop", string="Cultivo 3", domain=[('state', 'in', ['open'])])
    # Corte cultivo 3
    boxes_rasp3 = fields.Integer(string="C. Fra", default=0)
    boxes_straw3 = fields.Integer(string="C. Fre", default=0)
    pots_rasp3 = fields.Integer(string="B. Fra", default=0)
    pots_straw3 = fields.Integer(string="B. Fre", default=0)
    boxes_pots_crop_id3 = fields.Many2one("stock.estate.crop", string="Cultivo 4", domain=[('state', 'in', ['open'])])
    hours = fields.Float(string="Hrs.", default=0, readonly=True)
    hours_crop_id = fields.Many2one("stock.estate.crop", string="Cultivo 5", domain=[('state', 'in', ['open'])])
    extra_hours = fields.Float(string="H. extra", default=0, readonly=True)
    extra_hours_crop_id = fields.Many2one("stock.estate.crop", string="Cultivo 6", domain=[('state', 'in', ['open'])])
    comments = fields.Text(string="Actividades", readonly=True)
    # activity_id = fields.Many2many('hr.attendance.activity.list', 'hr_attendance_activity_rel', 'attendance_id', 'activity_id', 'Actividades')
    activity_id = fields.Many2one('hr.attendance.activity.list', 'Actividad')
    extra_activity_id = fields.Many2one('hr.attendance.activity.list', 'Actividad Extra')
    date = fields.Date(string="Fecha")
    # Utilizado para ordenar los registros
    sequence = fields.Integer('Secuencia')
    extra_expense = fields.Float(string='Gasto extra')
    extra_expense_activity_id = fields.Many2one('hr.attendance.activity.list', string='Justificación')
    extra_expense_estate_id = fields.Many2one('stock.estate.crop', string="Cult. gasto extra",
                                              domain=[('state', 'in', ['open'])])

    @api.multi
    def _verify_times(self, vals):
        # Validar si se modifico la hora de entrada y hora de salida
        time_in = self.time_in if ('time_in' not in vals) else vals['time_in']
        time_out = self.time_out if 'time_out' not in vals else vals['time_out']
        if time_in < 0 or time_out < 0:
            raise Warning("No se permiten tiempos negativos")
        if time_in > time_out:
            raise Warning("La hora de entrada no puede ser mayor a la hora de salida")
        if time_in > 23.99 or time_out > 23.99:
            raise Warning("La hora ingresada no puede ser mayor a 23:59hr")

    @api.multi
    def write(self, vals):
        self._verify_times(vals=vals)
        res = super(HrAttendanceGaaFriday, self).write(vals)
        return res

    @api.model
    def create(self, vals):
        season_id = self.env['hr.attendance.gaa'].search([('id', '=', vals['attendance_id'])])[0].season_id.id
        vals['season_id'] = season_id
        res = super(HrAttendanceGaaFriday, self).create(vals)
        return res

    def _round_time(self, min_limit, max_limit, time_worked):
        # Verificar si se cumple el mínimo o máximo de segundos
        minutes = time_worked - float((str(time_worked).split('.'))[0])
        horas = time_worked - minutes
        if minutes >= min_limit and minutes < max_limit:
            time_worked = horas + 0.50
        elif minutes >= max_limit:
            time_worked = horas + 1
        else:
            time_worked = horas
        return time_worked

    @api.multi
    def calculate_hours(self, vals):
        # Verificar los rangos de las horas
        self._verify_times(vals=vals)
        if int(vals['time_in']) <= 0 or int(vals['time_out']) <= 0:
            return
        time_in = vals['time_in']
        time_out = vals['time_out']
        time_obj = self.attendance_id
        time_limits_obj = self.env['hr.attendance.config'].search([('active', '=', True)])
        # Horas de trabajo por día establecidas por la empresa
        hours_per_day = time_obj.time_out - time_obj.time_in
        time_worked_normal = 0.00
        time_worked_extra = 0.00
        # Validar horas normales
        if time_in <= time_obj.time_out:
            if time_out <= time_obj.time_out:
                if time_in < time_obj.time_in:
                    time_worked_normal = time_out - time_obj.time_in
                else:
                    time_worked_normal = time_out - time_in
            elif time_in < time_obj.time_in:
                time_worked_normal = time_obj.time_out - time_obj.time_in
            else:
                time_worked_normal = time_obj.time_out - time_in

        # Validar horas extra
        if time_in > time_obj.time_out:
            time_worked_extra = time_out - time_in
        else:
            if time_out > time_obj.time_out:
                time_worked_extra = time_out - time_obj.time_out
            if time_in < time_obj.time_in:
                time_worked_extra += time_obj.time_in - time_in

        # Redondear las horas normales y horas extra
        time_worked_normal = self._round_time(time_limits_obj.min_limit, time_limits_obj.max_limit, time_worked_normal)
        time_worked_extra = self._round_time(time_limits_obj.min_limit, time_limits_obj.max_limit, time_worked_extra)

        # Determinar si se marca la asistencia de acuerdo si cumplio el horario establecido
        attended = False
        if time_worked_normal >= hours_per_day:
            attended = True
            time_worked_normal -= hours_per_day

        return {'value': {
            'attended': attended,
            'hours': time_worked_normal,
            'extra_hours': time_worked_extra, }}

    @api.multi
    def set_default_crop(self, opc, br=0, bs=0, pr=0, ps=0, attended=None, h=0, xh=0):
        """ Método para establecer el cultivo por defecto automáticamente de acuerdo ciertas validaciones
            br= box_rasp, bs=box_straw, pr=pots_rasp, ps=pots_straw, h=hours, xh=extra_hours"""
        # Verificar si tiene o no asistencia, en este caso ps=asistencia o no
        if opc == 1:
            if attended:
                return {'value': {'attended_crop_id': self.attendance_id.default_crop_id.id}}
            else:
                return {'value': {'attended_crop_id': None}}
        # Verificar si hay corte en alguno de los 3 cultivos
        elif 1 < opc < 5:
            if br + bs + pr + ps > 0:
                if opc == 2:
                    return {'value': {'boxes_pots_crop_id1': self.attendance_id.default_crop_id.id}}
                elif opc == 3:
                    return {'value': {'boxes_pots_crop_id2': self.attendance_id.default_crop_id.id}}
                elif opc == 4:
                    return {'value': {'boxes_pots_crop_id3': self.attendance_id.default_crop_id.id}}
            else:
                if opc == 2:
                    return {'value': {'boxes_pots_crop_id1': None}}
                elif opc == 3:
                    return {'value': {'boxes_pots_crop_id2': None}}
                elif opc == 4:
                    return {'value': {'boxes_pots_crop_id3': None}}
        # Verificar si hay o no horas de trabajo
        elif opc == 5:
            if h > 0:
                return {'value': {'hours_crop_id': self.attendance_id.default_crop_id.id}}
            else:
                return {'value': {'hours_crop_id': None}}
        # Verificar si hay o no horas extras
        elif opc == 6:
            if xh > 0:
                return {'value': {'extra_hours_crop_id': self.attendance_id.default_crop_id.id}}
            else:
                return {'value': {'extra_hours_crop_id': None}}


# Sabado
class HrAttendanceGaaSaturday(models.Model):
    _name = "hr.attendance.gaa.saturday"
    _description = "Empleados de la lista de asistencia sabado"
    _order = "employee_type, name"

    name = fields.Many2one("hr.employee", string="Empleado")
    employee_type = fields.Many2one("hr.config.order.employee", string="Tipo de empleado")
    season_id = fields.Many2one("stock.estate.season", string="Temporada")
    attendance_id = fields.Many2one("hr.attendance.gaa", string="Lista de asistencia", ondelete='cascade')
    attended = fields.Boolean(string="Asist.", default=True)
    attended_crop_id = fields.Many2one("stock.estate.crop", string="Cultivo 1", domain=[('state', 'in', ['open'])])
    time_in = fields.Float(string="Entrada", required=True)
    time_out = fields.Float(string="Salida", required=True)
    # Corte cultivo 1
    boxes_rasp1 = fields.Integer(string="C. Fra", default=0)
    boxes_straw1 = fields.Integer(string="C. Fre", default=0)
    pots_rasp1 = fields.Integer(string="B. Fra", default=0)
    pots_straw1 = fields.Integer(string="B. Fre", default=0)
    boxes_pots_crop_id1 = fields.Many2one("stock.estate.crop", string="Cultivo 2", domain=[('state', 'in', ['open'])])
    # Corte cultivo 2
    boxes_rasp2 = fields.Integer(string="C. Fra", default=0)
    boxes_straw2 = fields.Integer(string="C. Fre", default=0)
    pots_rasp2 = fields.Integer(string="B. Fra", default=0)
    pots_straw2 = fields.Integer(string="B. Fre", default=0)
    boxes_pots_crop_id2 = fields.Many2one("stock.estate.crop", string="Cultivo 3", domain=[('state', 'in', ['open'])])
    # Corte cultivo 3
    boxes_rasp3 = fields.Integer(string="C. Fra", default=0)
    boxes_straw3 = fields.Integer(string="C. Fre", default=0)
    pots_rasp3 = fields.Integer(string="B. Fra", default=0)
    pots_straw3 = fields.Integer(string="B. Fre", default=0)
    boxes_pots_crop_id3 = fields.Many2one("stock.estate.crop", string="Cultivo 4", domain=[('state', 'in', ['open'])])
    hours = fields.Float(string="Hrs.", default=0, readonly=True)
    hours_crop_id = fields.Many2one("stock.estate.crop", string="Cultivo 5", domain=[('state', 'in', ['open'])])
    extra_hours = fields.Float(string="H. extra", default=0, readonly=True)
    extra_hours_crop_id = fields.Many2one("stock.estate.crop", string="Cultivo 6", domain=[('state', 'in', ['open'])])
    comments = fields.Text(string="Actividades", readonly=True)
    # activity_id = fields.Many2many('hr.attendance.activity.list', 'hr_attendance_activity_rel', 'attendance_id', 'activity_id', 'Actividades')
    activity_id = fields.Many2one('hr.attendance.activity.list', 'Actividad')
    extra_activity_id = fields.Many2one('hr.attendance.activity.list', 'Actividad Extra')
    date = fields.Date(string="Fecha")
    # Utilizado para ordenar los registros
    sequence = fields.Integer('Secuencia')
    extra_expense = fields.Float(string='Gasto extra')
    extra_expense_activity_id = fields.Many2one('hr.attendance.activity.list', string='Justificación')
    extra_expense_estate_id = fields.Many2one('stock.estate.crop', string="Cult. gasto extra",
                                              domain=[('state', 'in', ['open'])])

    @api.multi
    def _verify_times(self, vals):
        # Validar si se modifico la hora de entrada y hora de salida
        time_in = self.time_in if ('time_in' not in vals) else vals['time_in']
        time_out = self.time_out if 'time_out' not in vals else vals['time_out']
        if time_in < 0 or time_out < 0:
            raise Warning("No se permiten tiempos negativos")
        if time_in > time_out:
            raise Warning("La hora de entrada no puede ser mayor a la hora de salida")
        if time_in > 23.99 or time_out > 23.99:
            raise Warning("La hora ingresada no puede ser mayor a 23:59hr")

    @api.multi
    def write(self, vals):
        self._verify_times(vals=vals)
        res = super(HrAttendanceGaaSaturday, self).write(vals)
        return res

    @api.model
    def create(self, vals):
        season_id = self.env['hr.attendance.gaa'].search([('id', '=', vals['attendance_id'])])[0].season_id.id
        vals['season_id'] = season_id
        res = super(HrAttendanceGaaSaturday, self).create(vals)
        return res

    def _round_time(self, min_limit, max_limit, time_worked):
        # Verificar si se cumple el mínimo o máximo de segundos
        minutes = time_worked - float((str(time_worked).split('.'))[0])
        horas = time_worked - minutes
        if minutes >= min_limit and minutes < max_limit:
            time_worked = horas + 0.50
        elif minutes >= max_limit:
            time_worked = horas + 1
        else:
            time_worked = horas
        return time_worked

    @api.multi
    def calculate_hours(self, vals):
        # Verificar los rangos de las horas
        self._verify_times(vals=vals)
        if int(vals['time_in']) <= 0 or int(vals['time_out']) <= 0:
            return
        time_in = vals['time_in']
        time_out = vals['time_out']
        time_obj = self.attendance_id
        time_limits_obj = self.env['hr.attendance.config'].search([('active', '=', True)])
        # Horas de trabajo por día establecidas por la empresa
        hours_per_day = time_obj.time_out - time_obj.time_in
        time_worked_normal = 0.00
        time_worked_extra = 0.00
        # Validar horas normales
        if time_in <= time_obj.time_out:
            if time_out <= time_obj.time_out:
                if time_in < time_obj.time_in:
                    time_worked_normal = time_out - time_obj.time_in
                else:
                    time_worked_normal = time_out - time_in
            elif time_in < time_obj.time_in:
                time_worked_normal = time_obj.time_out - time_obj.time_in
            else:
                time_worked_normal = time_obj.time_out - time_in

        # Validar horas extra
        if time_in > time_obj.time_out:
            time_worked_extra = time_out - time_in
        else:
            if time_out > time_obj.time_out:
                time_worked_extra = time_out - time_obj.time_out
            if time_in < time_obj.time_in:
                time_worked_extra += time_obj.time_in - time_in

        # Redondear las horas normales y horas extra
        time_worked_normal = self._round_time(time_limits_obj.min_limit, time_limits_obj.max_limit, time_worked_normal)
        time_worked_extra = self._round_time(time_limits_obj.min_limit, time_limits_obj.max_limit, time_worked_extra)

        # Determinar si se marca la asistencia de acuerdo si cumplio el horario establecido
        attended = False
        if time_worked_normal >= hours_per_day:
            attended = True
            time_worked_normal -= hours_per_day

        return {'value': {
            'attended': attended,
            'hours': time_worked_normal,
            'extra_hours': time_worked_extra, }}

    @api.multi
    def set_default_crop(self, opc, br=0, bs=0, pr=0, ps=0, attended=None, h=0, xh=0):
        """ Método para establecer el cultivo por defecto automáticamente de acuerdo ciertas validaciones
            br= box_rasp, bs=box_straw, pr=pots_rasp, ps=pots_straw, h=hours, xh=extra_hours"""
        # Verificar si tiene o no asistencia, en este caso ps=asistencia o no
        if opc == 1:
            if attended:
                return {'value': {'attended_crop_id': self.attendance_id.default_crop_id.id}}
            else:
                return {'value': {'attended_crop_id': None}}
        # Verificar si hay corte en alguno de los 3 cultivos
        elif 1 < opc < 5:
            if br + bs + pr + ps > 0:
                if opc == 2:
                    return {'value': {'boxes_pots_crop_id1': self.attendance_id.default_crop_id.id}}
                elif opc == 3:
                    return {'value': {'boxes_pots_crop_id2': self.attendance_id.default_crop_id.id}}
                elif opc == 4:
                    return {'value': {'boxes_pots_crop_id3': self.attendance_id.default_crop_id.id}}
            else:
                if opc == 2:
                    return {'value': {'boxes_pots_crop_id1': None}}
                elif opc == 3:
                    return {'value': {'boxes_pots_crop_id2': None}}
                elif opc == 4:
                    return {'value': {'boxes_pots_crop_id3': None}}
        # Verificar si hay o no horas de trabajo
        elif opc == 5:
            if h > 0:
                return {'value': {'hours_crop_id': self.attendance_id.default_crop_id.id}}
            else:
                return {'value': {'hours_crop_id': None}}
        # Verificar si hay o no horas extras
        elif opc == 6:
            if xh > 0:
                return {'value': {'extra_hours_crop_id': self.attendance_id.default_crop_id.id}}
            else:
                return {'value': {'extra_hours_crop_id': None}}


# Domingo
class HrAttendanceSunday(models.Model):
    _name = "hr.attendance.gaa.sunday"
    _description = "Empleados de la lista de asistencia domingo"
    _order = "employee_type, name"

    name = fields.Many2one("hr.employee", string="Empleado")
    employee_type = fields.Many2one("hr.config.order.employee", string="Tipo de empleado")
    season_id = fields.Many2one("stock.estate.season", string="Temporada")
    attendance_id = fields.Many2one("hr.attendance.gaa", string="Lista de asistencia", ondelete='cascade')
    attended = fields.Boolean(string="Asist.", default=True)
    attended_crop_id = fields.Many2one("stock.estate.crop", string="Cultivo 1", domain=[('state', 'in', ['open'])])
    time_in = fields.Float(string="Entrada", required=True)
    time_out = fields.Float(string="Salida", required=True)
    # Corte cultivo 1
    boxes_rasp1 = fields.Integer(string="C. Fra", default=0)
    boxes_straw1 = fields.Integer(string="C. Fre", default=0)
    pots_rasp1 = fields.Integer(string="B. Fra", default=0)
    pots_straw1 = fields.Integer(string="B. Fre", default=0)
    boxes_pots_crop_id1 = fields.Many2one("stock.estate.crop", string="Cultivo 2", domain=[('state', 'in', ['open'])])
    # Corte cultivo 2
    boxes_rasp2 = fields.Integer(string="C. Fra", default=0)
    boxes_straw2 = fields.Integer(string="C. Fre", default=0)
    pots_rasp2 = fields.Integer(string="B. Fra", default=0)
    pots_straw2 = fields.Integer(string="B. Fre", default=0)
    boxes_pots_crop_id2 = fields.Many2one("stock.estate.crop", string="Cultivo 3", domain=[('state', 'in', ['open'])])
    # Corte cultivo 3
    boxes_rasp3 = fields.Integer(string="C. Fra", default=0)
    boxes_straw3 = fields.Integer(string="C. Fre", default=0)
    pots_rasp3 = fields.Integer(string="B. Fra", default=0)
    pots_straw3 = fields.Integer(string="B. Fre", default=0)
    boxes_pots_crop_id3 = fields.Many2one("stock.estate.crop", string="Cultivo 4", domain=[('state', 'in', ['open'])])
    hours = fields.Float(string="Hrs.", default=0, readonly=True)
    hours_crop_id = fields.Many2one("stock.estate.crop", string="Cultivo 5", domain=[('state', 'in', ['open'])])
    extra_hours = fields.Float(string="H. extra", default=0, readonly=True)
    extra_hours_crop_id = fields.Many2one("stock.estate.crop", string="Cultivo 6", domain=[('state', 'in', ['open'])])
    comments = fields.Text(string="Actividades", readonly=True)
    # activity_id = fields.Many2many('hr.attendance.activity.list', 'hr_attendance_activity_rel', 'attendance_id', 'activity_id', 'Actividades')
    activity_id = fields.Many2one('hr.attendance.activity.list', 'Actividad')
    extra_activity_id = fields.Many2one('hr.attendance.activity.list', 'Actividad Extra')
    date = fields.Date(string="Fecha")
    # Utilizado para ordenar los registros
    sequence = fields.Integer('Secuencia')
    extra_expense = fields.Float(string='Gasto extra')
    extra_expense_activity_id = fields.Many2one('hr.attendance.activity.list', string='Justificación')
    extra_expense_estate_id = fields.Many2one('stock.estate.crop', string="Cult. gasto extra",
                                              domain=[('state', 'in', ['open'])])

    @api.multi
    def _verify_times(self, vals):
        # Validar si se modifico la hora de entrada y hora de salida
        time_in = self.time_in if ('time_in' not in vals) else vals['time_in']
        time_out = self.time_out if 'time_out' not in vals else vals['time_out']
        if time_in < 0 or time_out < 0:
            raise Warning("No se permiten tiempos negativos")
        if time_in > time_out:
            raise Warning("La hora de entrada no puede ser mayor a la hora de salida")
        if time_in > 23.59 or time_out > 23.59:
            raise Warning("La hora ingresada no puede ser mayo a 23:59hr")

    @api.multi
    def write(self, vals):
        self._verify_times(vals=vals)
        res = super(HrAttendanceSunday, self).write(vals)
        return res

    @api.model
    def create(self, vals):
        season_id = self.env['hr.attendance.gaa'].search([('id', '=', vals['attendance_id'])])[0].season_id.id
        vals['season_id'] = season_id
        res = super(HrAttendanceSunday, self).create(vals)
        return res

    def _round_time(self, min_limit, max_limit, time_worked):
        # Verificar si se cumple el mínimo o máximo de segundos
        minutes = time_worked - float((str(time_worked).split('.'))[0])
        horas = time_worked - minutes
        if minutes >= min_limit and minutes < max_limit:
            time_worked = horas + 0.50
        elif minutes >= max_limit:
            time_worked = horas + 1
        else:
            time_worked = horas
        return time_worked

    @api.multi
    def calculate_hours(self, vals):
        # Verificar los rangos de las horas
        self._verify_times(vals=vals)
        if int(vals['time_in']) <= 0 or int(vals['time_out']) <= 0:
            return
        time_in = vals['time_in']
        time_out = vals['time_out']
        time_obj = self.attendance_id
        time_limits_obj = self.env['hr.attendance.config'].search([('active', '=', True)])
        # Horas de trabajo por día establecidas por la empresa
        hours_per_day = time_obj.time_out_sunday - time_obj.time_in_sunday
        time_worked_normal = 0.00
        time_worked_extra = 0.00
        # Validar horas normales
        if time_in <= time_obj.time_out_sunday:
            if time_out <= time_obj.time_out_sunday:
                if time_in < time_obj.time_in_sunday:
                    time_worked_normal = time_out - time_obj.time_in_sunday
                else:
                    time_worked_normal = time_out - time_in
            elif time_in < time_obj.time_in_sunday:
                time_worked_normal = time_obj.time_out_sunday - time_obj.time_in_sunday
            else:
                time_worked_normal = time_obj.time_out_sunday - time_in

        # Validar horas extra
        if time_in > time_obj.time_out_sunday:
            time_worked_extra = time_out - time_in
        else:
            if time_out > time_obj.time_out_sunday:
                time_worked_extra = time_out - time_obj.time_out_sunday
            if time_in < time_obj.time_in_sunday:
                time_worked_extra += time_obj.time_in_sunday - time_in

        # Redondear las horas normales y horas extra
        time_worked_normal = self._round_time(time_limits_obj.min_limit, time_limits_obj.max_limit, time_worked_normal)
        time_worked_extra = self._round_time(time_limits_obj.min_limit, time_limits_obj.max_limit, time_worked_extra)

        # Determinar si se marca la asistencia de acuerdo si cumplio el horario establecido
        attended = False
        if time_worked_normal >= hours_per_day:
            attended = True
            time_worked_normal -= hours_per_day

        return {'value': {
            'attended': attended,
            'hours': time_worked_normal,
            'extra_hours': time_worked_extra, }}

    @api.multi
    def set_default_crop(self, opc, br=0, bs=0, pr=0, ps=0, attended=None, h=0, xh=0):
        """ Método para establecer el cultivo por defecto automáticamente de acuerdo ciertas validaciones
            br= box_rasp, bs=box_straw, pr=pots_rasp, ps=pots_straw, h=hours, xh=extra_hours"""
        # Verificar si tiene o no asistencia, en este caso ps=asistencia o no
        if opc == 1:
            if attended:
                return {'value': {'attended_crop_id': self.attendance_id.default_crop_id.id}}
            else:
                return {'value': {'attended_crop_id': None}}
        # Verificar si hay corte en alguno de los 3 cultivos
        elif 1 < opc < 5:
            if br + bs + pr + ps > 0:
                if opc == 2:
                    return {'value': {'boxes_pots_crop_id1': self.attendance_id.default_crop_id.id}}
                elif opc == 3:
                    return {'value': {'boxes_pots_crop_id2': self.attendance_id.default_crop_id.id}}
                elif opc == 4:
                    return {'value': {'boxes_pots_crop_id3': self.attendance_id.default_crop_id.id}}
            else:
                if opc == 2:
                    return {'value': {'boxes_pots_crop_id1': None}}
                elif opc == 3:
                    return {'value': {'boxes_pots_crop_id2': None}}
                elif opc == 4:
                    return {'value': {'boxes_pots_crop_id3': None}}
        # Verificar si hay o no horas de trabajo
        elif opc == 5:
            if h > 0:
                return {'value': {'hours_crop_id': self.attendance_id.default_crop_id.id}}
            else:
                return {'value': {'hours_crop_id': None}}
        # Verificar si hay o no horas extras
        elif opc == 6:
            if xh > 0:
                return {'value': {'extra_hours_crop_id': self.attendance_id.default_crop_id.id}}
            else:
                return {'value': {'extra_hours_crop_id': None}}


# Clase para almacenar el total de todos los días de la semana.
class HrAttendanceGaaResume(models.Model):
    _name = "hr.attendance.gaa.resume"
    _description = "Resumen de los trabajo por empleado"
    _order = "employee_type, name"

    name = fields.Many2one("hr.employee", string="Empleado")
    employee_type = fields.Many2one("hr.config.order.employee", string="Tipo de empleado")
    attendance_id = fields.Many2one("hr.attendance.gaa", readonly=True, string="Lista de asistencia",
                                    ondelete='cascade')
    total_attended = fields.Integer(string="Total asistencias", readonly=True)
    # Corte cultivo 1
    total_boxes_rasp1 = fields.Integer(string="C. Fra", default=0, readonly=True)
    total_boxes_straw1 = fields.Integer(string="C. Fre", default=0, readonly=True)
    total_pots_rasp1 = fields.Integer(string="B. Fra", default=0, readonly=True)
    total_pots_straw1 = fields.Integer(string="B. Fre", default=0, readonly=True)
    # Corte cultivo 2
    total_boxes_rasp2 = fields.Integer(string="C. Fra", default=0, readonly=True)
    total_boxes_straw2 = fields.Integer(string="C. Fre", default=0, readonly=True)
    total_pots_rasp2 = fields.Integer(string="B. Fra", default=0, readonly=True)
    total_pots_straw2 = fields.Integer(string="B. Fre", default=0, readonly=True)
    # Corte cultivo 3
    total_boxes_rasp3 = fields.Integer(string="C. Fra", default=0, readonly=True)
    total_boxes_straw3 = fields.Integer(string="C. Fre", default=0, readonly=True)
    total_pots_rasp3 = fields.Integer(string="B. Fra", default=0, readonly=True)
    total_pots_straw3 = fields.Integer(string="B. Fre", default=0, readonly=True)
    total_hours = fields.Float(string="Horas", default=0, readonly=True)
    total_extra_hours = fields.Float(string="H. extra", default=0, readonly=True)
    # Bono y Descuento
    weekly_bonus = fields.Float('Bono', default=0.00)
    loan_discount = fields.Float('Descuento', default=0.00)
    date = fields.Date(string="Fecha")
    # Utilizado para ordenar los registros
    sequence = fields.Integer('Secuencia')
    total_extra_expense = fields.Float(string='G. extra', default=0, readonly=True)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: