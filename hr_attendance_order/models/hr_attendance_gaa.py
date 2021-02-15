# -*- coding: utf-8 -*-

from odoo import models, api


class HrAttendanceGaa(models.Model):
    _inherit = 'hr.attendance.gaa'

    @api.multi
    def update_sequence(self):
        for item in self.monday_employees_ids:
            item.sequence = item.name.sequence

        for item in self.tuesday_employees_ids:
            item.sequence = item.name.sequence

        for item in self.wednesday_employees_ids:
            item.sequence = item.name.sequence

        for item in self.thursday_employees_ids:
            item.sequence = item.name.sequence

        for item in self.friday_employees_ids:
            item.sequence = item.name.sequence

        for item in self.saturday_employees_ids:
            item.sequence = item.name.sequence

        for item in self.sunday_employees_ids:
            item.sequence = item.name.sequence

        for item in self.resume:
            item.sequence = item.name.sequence



class HrAttendanceGaaMonday(models.Model):
    _inherit = 'hr.attendance.gaa.monday'
    _order = 'sequence'


class HrAttendanceGaaTuesday(models.Model):
    _inherit = 'hr.attendance.gaa.tuesday'
    _order = 'sequence'


class HrAttendanceGaaWednesday(models.Model):
    _inherit = 'hr.attendance.gaa.wednesday'
    _order = 'sequence'


class HrAttendanceGaaThursday(models.Model):
    _inherit = 'hr.attendance.gaa.thursday'
    _order = 'sequence'


class HrAttendanceGaaFriday(models.Model):
    _inherit = 'hr.attendance.gaa.friday'
    _order = 'sequence'


class HrAttendanceGaaSaturday(models.Model):
    _inherit = 'hr.attendance.gaa.saturday'
    _order = 'sequence'


class HrAttendanceGaaSunday(models.Model):
    _inherit = 'hr.attendance.gaa.sunday'
    _order = 'sequence'


class HrAttendanceGaaResume(models.Model):
    _inherit = 'hr.attendance.gaa.resume'
    _order = 'sequence'


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: