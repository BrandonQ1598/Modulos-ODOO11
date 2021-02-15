# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT


class PagosGeneralesReportWizard(models.TransientModel):
    _name="pagos.generales.report.wizard"

    partner_type = fields.Selection([('Clientes', 'Clientes'), ('Proveedores', 'Proveedores')], string='Tipo', default="Clientes")
    partner_id = fields.Many2one('res.partner')
    cantidad = fields.Selection([('Todos', 'Todos'),('Uno', 'Seleccionar uno')], string='Cantidad',default="Todos")
    start_date = fields.Date(string="Start Date",required=True)
    end_date = fields.Date(string="End Date",required=True)

    def get_report(self):
        data = {
            'model': self._name,
            'form': self.read()[0]
        }
        report = self.env.ref('report_pagos_generales.report_pagos_generales_wizard').report_action(self, data=data)
        return report


class ReportWizardFunctions(models.AbstractModel):
    _name = "report.report_pagos_generales.report_pagos_generales_template"

    #consulta los pagos de una factura
    def get_invoice_payments(self, payment_id):
        if (payment_id != 'null'):
            payments = self.env["account.payment"].search([("id", "=", payment_id.id),("state", "in", ['posted', 'reconciled'])])
        return payments

    #consulta los anticipos que no estan vinculados a ninguna factura
    def get_advances(self,start_date,end_date,partner_type):
        if(partner_type == 'Clientes'):
            advances = self.env["account.payment"].search([("payment_date", ">=", start_date),
                                                           ("payment_date", "<=", end_date),
                                                           ("payment_type", "=", "inbound"),
                                                           ("state", "in", ['posted', 'reconciled']),
                                                           ("advance", "=", True),
                                                           ("invoice_ids","=", False)])
        else:
            advances = self.env["account.payment"].search([("payment_date", ">=", start_date),
                                                           ("payment_date", "<=", end_date),
                                                           ("payment_type", "=", "outbound"),
                                                           ("state", "in", ['posted', 'reconciled']),
                                                           ("advance", "=", True),
                                                           ("invoice_ids","=",False)])
        return advances

    #consulta los anticipos no vinvulados a ninguna factura de un cliente
    def get_advances_partner(self,start_date,end_date,partner_id,partner_type):
        #si se selecciona clientes
        if(partner_type == 'Clientes'):
            advances = self.env["account.payment"].search([("partner_id", "=", partner_id.id),
                                                           ("payment_date", ">=", start_date),
                                                           ("payment_date", "<=", end_date),
                                                           ("state", "in", ['posted', 'reconciled']),
                                                           ("payment_type", "=", "inbound"),
                                                           ("advance", "=", True),
                                                           ("invoice_ids","=",False)])
        else:
            advances = self.env["account.payment"].search([("partner_id", "=", partner_id.id),
                                                           ("payment_date", ">=", start_date),
                                                           ("payment_date", "<=", end_date),
                                                           ("payment_type", "=", "outbound"),
                                                           ("state", "in", ['posted', 'reconciled']),
                                                           ("advance", "=", True),
                                                           ("invoice_ids", "=", False)])

        return advances

    @api.model
    def get_report_values(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        report_obj = self.env['ir.actions.report']
        report = report_obj._get_report_from_name('report_pagos_generales.report_pagos_generales_template')
        date_start = data['form']['start_date']
        date_end = data['form']['end_date']
        start_date = datetime.strptime(date_start, DATE_FORMAT)
        end_date = datetime.strptime(date_end, DATE_FORMAT)
        #si se selecciona todos
        if (data['form']['cantidad'] == 'Todos'):
            #si se selecciona clientes, si no proveedores
            if(data['form']['partner_type'] == 'Clientes'):
                invoices = self.env["account.invoice"].search([("date_invoice", ">=", start_date),
                                                               ("date_invoice", "<=", end_date),
                                                               ("state", "in", ['paid', 'open']),
                                                               ("type","=","out_invoice")])
            else:
                invoices = self.env["account.invoice"].search([("date_invoice", ">=", start_date),
                                                               ("date_invoice", "<=", end_date),
                                                               ("state", "in", ['paid', 'open']),
                                                               ("type", "=", "in_invoice")])
        else:
        #si solo selecciona uno
            partner_id = data['form']['partner_id'][1] #trae el id de el partner seleccionado
            #si se selecciono un cliente
            if(data['form']['partner_type'] == 'Clientes'):
                invoices = self.env["account.invoice"].search([("date_invoice", ">=", start_date),
                                                               ("date_invoice", "<=", end_date),
                                                               ("partner_id", "=", str(partner_id)),
                                                               ("state", "in", ['paid', 'open']),
                                                               ("type","=","out_invoice")])
            #si se selecciono proveedor
            else:
                invoices = self.env["account.invoice"].search([("date_invoice", ">=", start_date),
                                                               ("date_invoice", "<=", end_date),
                                                               ("partner_id", "=", str(partner_id)),
                                                               ("state", "in", ['paid', 'open']),
                                                               ("type", "=", "in_invoice")])
        #carga los documentos
        docargs = {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': docs,
            'invoices':invoices,
            'get_invoice_payments':self.get_invoice_payments,
            'get_advances':self.get_advances,
            'get_advances_partner':self.get_advances_partner,
        }
        return docargs
