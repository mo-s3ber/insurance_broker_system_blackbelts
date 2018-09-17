from odoo import api, fields, models

class Renewal_Again(models.Model):
    _name = "renewal.again"
    _rec_name="old_number"

    old_number = fields.Many2one("policy.broker", string="Old Policy Number")
    new_number = fields.Char(string="New Policy Number")
    issue_date = fields.Date(string="Effective Date")
    start_date = fields.Date(string="Effective Start On")
    end_date = fields.Date(string="Effective End On")

    @api.multi
    def create_renewal(self):
        form_view = self.env.ref('insurance_broker_system_blackbelts.my_view_for_policy_form_kmlo1')


        riskrecordd = self.env["new.risks"].search([('id', 'in', self.old_number.new_risk_ids.ids)])
        records_cargo = []
        for rec in riskrecordd:
            objectcargo = (
                    0, 0, {'risk': rec.risk, 'risk_description': rec.risk_description})
            records_cargo.append(objectcargo)


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
                            'default_renwal_check': True,
                    'default_policy_number':self.new_number,
                    'default_std_id': self.old_number.std_id,
                    'default_customer': self.old_number.customer.id,
                    'default_issue_date': self.issue_date,
                    'default_start_date': self.start_date,
                    'default_end_date': self.end_date,
                    'default_barnche': self.old_number.barnche,
                    'default_salesperson': self.old_number.salesperson.id,
                    'default_onlayer': self.old_number.onlayer,
                    'default_currency_id': self.old_number.currency_id.id,
                    'default_benefit': self.old_number.benefit,

                    'default_insurance_type': self.old_number.insurance_type,
                    'default_line_of_bussines': self.old_number.line_of_bussines.id,
                    'default_ins_type': self.old_number.ins_type,
                    'default_new_risk_ids': records_cargo,
                            }
            }