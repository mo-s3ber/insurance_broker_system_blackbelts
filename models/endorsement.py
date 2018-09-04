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

        riskrecordd = self.env["new.risks"].search([('id', 'in', self.number_policy.new_risk_ids.ids)])
        records_cargo = []
        for rec in riskrecordd:
                objectcargo = (
                    0, 0, {'risk': rec.risk, 'risk_description': rec.risk_description})
                records_cargo.append(objectcargo)
            # # .......
            #
        recordproposal = self.env['proposal.bb'].search([('id', 'in', self.number_policy.propoasl_ids.ids)])
        records_proposal = []
        for rec in recordproposal:
                proposal_opp = (
                    0, 0, {'Company': rec.Company.id, 'product_pol': rec.product_pol.id, 'premium': rec.premium})
                records_proposal.append(proposal_opp)

        if self.number_edit:
            return {
                'name': ('Policy'),
                'view_type': 'form',
                'view_mode': 'form',
                'views': [(form_view.id, 'form')],
                'res_model': 'policy.broker',
                'target': 'current',
                'type': 'ir.actions.act_window',
                'context': {
                    'default_std_id': self.number_policy.std_id,
                    'default_customer':self.number_policy.customer.id,
                    'default_edit_number':self.number_edit ,
                    'default_edit_decr':self.reasonedit ,
                    'default_insurance_type': self.number_policy.insurance_type,
                    'default_line_of_bussines':self.number_policy.line_of_bussines.id ,
                    'default_ins_type': self.number_policy.ins_type,
                    'default_new_risk_ids':records_cargo ,
                    'default_propoasl_ids':records_proposal,

                            }
            }
