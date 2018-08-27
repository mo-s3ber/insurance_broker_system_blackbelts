from odoo import models, fields, api
from odoo.exceptions import ValidationError

class claimPolicy(models.Model):
    _name ="insurance.claim"


    policy_number = fields.Many2one('policy.broker',string='Policy Number',required=True,domain="[('edit_number','=',0)]")
    endorsement= fields.Many2one('policy.broker',string='Endorsement', required=True,domain="[('edit_number','!=',0)]")
    risk_object=fields.Char(string='Risk Object')
    risk_person = fields.Many2one('person.object',string='Person Risk',domain="[('object_person','=',policy_number)]")
    risk_person_model = fields.One2many('person.object','person_model',string='Person')
    risk_vehicle=fields.Many2one('vehicle.object',string='Vehicle Risk',domain="[('object_vehicle','=',policy_number)]")
    risk_vehicle_model=fields.One2many('vehicle.object','vehicle_model',string='Vehicle')
    risk_cargo = fields.Many2one('cargo.object', string='Cargo Risk',domain="[('object_cargo','=',policy_number)]")
    risk_cargo_model = fields.One2many('cargo.object','cargo_model',string='Cargo')
    coverage = fields.Many2one('insurance.product.coverage',string='Coverage')

    claim_line= fields.One2many('insurance.claim.line','claim_object',string='Claim Lines')
    amount = fields.Float(string='Amount')

    @api.onchange('endorsement')
    def _onchange_policy_number(self):
        if self:
            self.risk_object = self.endorsement.line_of_bussines.object
        else:
            self.risk_object = 0

    @api.onchange('risk_person')
    def _onchange_risk_person(self):
        if self:
            self.risk_person_model =self.risk_person
        else:
            self.risk_person_model = False

    @api.onchange('risk_vehicle')
    def _onchange_risk_vehicle(self):
        if self:
            self.risk_vehicle_model=self.risk_vehicle
        else:
            self.risk_vehicle_model =False

    @api.onchange('risk_cargo')
    def _onchange_risk_cargo(self):
        if self:
            self.risk_cargo_model=self.risk_cargo
        else:
            self.risk_cargo_model =False

    @api.onchange('claim_line')
    def _onchange_claim_line(self):
        index=0
        for record in self.claim_line:
            index+=record.amount
        self.amount=index

    # @api.model
    # def create(self, values):
    #     if values.get('amount', False):
    #         values['amount']=self.amount
    #     return super(claimPolicy, self).create(values)
    #
    # @api.multi
    # def write(self, values):
    #     if values.get('amount', False):
    #         values['amount'] = self.amount
    #     return super(claimPolicy, self).write(values)




class claimLine(models.Model):
    _name ="insurance.claim.line"
    _rec_name = "claim_item"

    claim_item=fields.Many2one('insurance.claim.item',string='Claim Item',domain="[('risk_objects','=',related_claim)]")
    amount=fields.Float(string='Amount')
    claim_object=fields.Many2one('insurance.claim')
    related_claim=fields.Char(related='claim_object.risk_object',store=True,readonly=True)

class claimItem(models.Model):
    _name ="insurance.claim.item"
    _rec_name = "name"

    risk_objects= fields.Selection([('person', 'Person'),
                          ('vehicle', 'Vehicle'),
                          ('cargo', 'Cargo'),],
                         'Insured Object',required=True)
    name = fields.Char(string='Name',required=True)



