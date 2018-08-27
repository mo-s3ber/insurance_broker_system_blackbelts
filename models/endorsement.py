from odoo import api, fields, models

class Endorsement_edit(models.Model):
    _name="endorsement.edit"
    _rec_name="number_policy"


    number_policy=fields.Many2one("policy.broker", string="Edit policy number")
    number_edit = fields.Integer(string="Endorsement Number")
    reasonedit = fields.Text(string="Endorsement Reason")
    issue_date = fields.Date(string="Effective Date")
    start_date = fields.Date(string="Effective Start On")
    end_date = fields.Date(string="Effective End On")


    @api.multi
    def create_endorsement(self):
        form_view = self.env.ref('insurance_broker_system_blackbelts.my_view_for_policy_form_kmlo1')
        if self.number_edit:
            return {
                'name': ('Policy'),
                'view_type': 'form',
                'view_mode': 'form',
                'views': [(form_view.id, 'form')],
                'res_model': 'policy.broker',
                'target': 'current',
                'type': 'ir.actions.act_window',
                'context': {}
            }