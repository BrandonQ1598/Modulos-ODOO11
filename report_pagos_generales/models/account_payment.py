from odoo import models,fields,api

class PaymentAdvanceField(models.Model):
    _inherit = "account.payment"

    advance = fields.Boolean("Advance",default=False,store= True)