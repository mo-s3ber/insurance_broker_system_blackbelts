from odoo import models, fields, api
from odoo.exceptions import ValidationError

class claimPolicy(models.Model):
    _name ="insurance.claim"

    policy_number = fields.Many2one('policy.broker',string='Policy Number',required=True)
    risk_object=fields.Char(string='Risk Object')
    renewal = fields.Many2one('renewal.again',string='Renewal', required=True,domain="[('old_number','=',policy_number)]")
    endorsement= fields.Many2one('endorsement.edit',string='Endorsement', required=True,domain="[('number_policy','=',policy_number)]")
    risk_person = fields.Many2one('person.object',string='Person Risk')
    risk_vehicle=fields.Many2one('vehicle.object',string='Vehicle Risk')
    risk_cargo = fields.Many2one('cargo.object', string='Cargo Risk')
    coverage = fields.Many2one('insurance.product.coverage',string='Coverage')
    details= fields.Char(string='Details')
    amount = fields.Float(string='Amount')

    @api.onchange('policy_number')
    def _onchange_policy_number(self):
        if self:
            self.risk_object = self.policy_number.line_of_bussines.object
        else:
            self.risk_object = 0

