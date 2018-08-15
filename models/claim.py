from odoo import models, fields, api
from odoo.exceptions import ValidationError

class claimPolicy(models.Model):
    _name ="insurance.claim"

    policy_number = fields.Many2one('policy.broker',string='Policy Number',required=True)
    renewal = fields.Char(string='Renewal', required=True)
    endorsement= fields.Char(string='Endorsement', required=True)
    risk_person = fields.Many2one('person.object',string='Person Risk')
    risk_vehicle=fields.Many2one('vehicle.object',string='Vehicle Risk')
    risk_cargo = fields.Many2one('cargo.object', string='Cargo Risk')
    coverage = fields.Many2one('insurance.product.coverage',string='Coverage')
    details= fields.Char(string='Details')
    amount = fields.Float(string='Amount')