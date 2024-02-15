from odoo import models,fields, _,api
from odoo.exceptions import RedirectWarning

class ConfirmWarning(models.TransientModel):
    _name = "warning.wizard"
    warning = fields.Text(string="Text")

    @api.model
    def default_get(self,vals):
        res = super(ConfirmWarning,self).default_get(vals)
        res['warning'] = self.env.context.get('msg')
        return res
    def proceed(self):
        con = self.env.context.copy()
        context = {'count':0,
                   'active_id': self.env.context.get('active_id')}
        condition = self.env.context.get('count')
        wizard = {
            'name': "warning",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'warning.wizard',
            'view_id': self.env.ref('task_context.untrustworthy_warning_wizard_forms').id,
            'target': 'new',
            'context': context}
        if con.get('opportunity') == False and condition < 1:
            msg = "The quotation is not related to any opportunity."
            context.update(count=1)
            context.update({'msg': msg})
            return wizard
        elif con.get('amount') == 0 and condition < 2:
            msg = "The total amount is Zero!"
            context.update(count=2)
            context.update({'msg': msg})
            return wizard
        elif condition < 3:
            record = self.env["sale.order"].browse(self.env.context.get('active_id'))
            # context.update(count=3)
            return record.with_context(count=3).action_confirm()

















