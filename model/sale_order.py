from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        check_boolean = self.env["res.partner"].search([('name', '=', self.partner_id.name)])
        check_opportunity = self.opportunity_id.name
        check_amount = self.amount_total
        count = self.env.context
        context = {'active_id': self.env.context.get('id')}
        wizard = {
            'name': "warning",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'warning.wizard',
            'view_id': self.env.ref('task_context.untrustworthy_warning_wizard_forms').id,
            'target': 'new',
            'context': context}
        if check_boolean.untrustworthy and count.update({'count':0})>1:
            msg = "This customer is untrustworthy. Are you sure you want to proceed?"
            context.update({'msg':msg})
            return wizard
            # wizard_action_id = self.env.ref('task_context.untrustworthy_warning_wizard_forms')
            # msg = "This customer is untrustworthy. Are you sure you want to proceed?"
            # raise RedirectWarning(msg, wizard_action_id.id, ('proceed'),
            #                       {'active_id': self.env.context.get('id'), })
        elif check_opportunity == False :
            msg = "The quotation is not related to any opportunity."
            wizard['context']['msg'] = msg
            return wizard
        elif check_amount == 0:
            msg = "The total amount is Zero!"
            wizard['context']['msg'] = msg
            return wizard
        else:
            return super(SaleOrder, self).action_confirm()
