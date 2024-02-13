from odoo import models, fields

class ResPartner(models.Model):
    _inherit = "res.partner"

    untrustworthy = fields.Boolean(string="Untrustworthy")
