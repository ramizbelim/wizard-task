from odoo import models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        check_boolean = self.env["res.partner"].search([('name', '=', self.partner_id.name)])
        check_opportunity = self.opportunity_id.name
        check_amount = self.amount_total
        context = {'count': 0,
                   'opportunity': check_opportunity,
                   'amount': check_amount,
                   'active_id':self.id}
        wizard = {
            'name': "warning",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'warning.wizard',
            'view_id': self.env.ref('task_context.untrustworthy_warning_wizard_forms').id,
            'target': 'new',
            'context': context}
        if check_boolean.untrustworthy and self.env.context.get('count',0)<1:
            msg = "This customer is untrustworthy. Are you sure you want to proceed?"
            context.update(count=0)
            context.update({'msg': msg})
            return wizard
        elif check_opportunity == False and self.env.context.get('count',1)<2:
            msg = "The quotation is not related to any opportunity."
            context.update(count=1)
            context.update({'msg': msg})
            return wizard
        elif check_amount == 0 and self.env.context.get('count',2)<3:
            msg = "The total amount is Zero!"
            context.update(count=2)
            context.update({'msg': msg})
            return wizard
        else:
            return super(SaleOrder, self).action_confirm()


