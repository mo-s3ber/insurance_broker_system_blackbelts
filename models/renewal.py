from odoo import api, fields, models

class Renewal_Again(models.Model):
    _name = "renewal.again"
    _rec_name="new_number"

    old_number = fields.Many2one("policy.broker", string="Old Policy Number")
    new_number = fields.Char(string="New Policy Number")
    issue_date = fields.Date(string="Issue Date")
    start_date = fields.Date(string="Coverage Start On")
    end_date = fields.Date(string="Coverage End On")

    @api.multi
    def create_renewal(self):
        form_view = self.env.ref('insurance_broker_system_blackbelts.my_view_for_policy_form_kmlo1')
        if self.new_number:
            return {
                'name': ('Policy'),
                'view_type': 'form',
                'view_mode': 'form',
                'views': [(form_view.id, 'form')],
                'res_model': 'policy.broker',
                'target': 'current',
                'type': 'ir.actions.act_window',
                'context': {
                            'default_renwal_check': True
                            }
            }