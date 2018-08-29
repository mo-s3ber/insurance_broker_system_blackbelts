from odoo import models, fields, api ,_
from odoo.exceptions import ValidationError

class claimPolicy(models.Model):
    _name ="insurance.claim"

    name = fields.Char(string='Name', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))
    policy_number = fields.Many2one('policy.broker',string='Policy Number',required=True,domain="[('edit_number','=',False)]")
    related_policy=fields.Char(related='policy_number.std_id',store=True,readonly=True)
    customer_policy=fields.Many2one('res.partner',related='policy_number.customer',string='Customer',store=True,readonly=True)
    endorsement= fields.Many2one('policy.broker',string='Endorsement',domain="['&',('edit_number','!=',False),('std_id','=',related_policy)]")
    risk_object=fields.Char(string='Risk Object')
    risk_person = fields.Many2one('person.object',string='Person Risk',domain="[('object_person','=',endorsement)]")
    risk_person_model = fields.One2many('person.object','person_model',string='Person')
    risk_vehicle=fields.Many2one('vehicle.object',string='Vehicle Risk',domain="[('object_vehicle','=',endorsement)]")
    risk_vehicle_model=fields.One2many('vehicle.object','vehicle_model',string='Vehicle')
    risk_cargo = fields.Many2one('cargo.object', string='Cargo Risk',domain="[('object_cargo','=',endorsement)]")
    risk_cargo_model = fields.One2many('cargo.object','cargo_model',string='Cargo')
    coverage = fields.Many2one('insurance.product.coverage',string='Coverage')

    claim_line= fields.One2many('insurance.claim.line','claim_object',string='Claim Lines')
    amount = fields.Float(string='Amount')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('insurance.claim') or 'New'
        return super(claimPolicy, self).create(vals)

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





class claimLine(models.Model):
    _name ="insurance.claim.line"
    _rec_name = "claim_item"

    claim_item=fields.Many2one('insurance.claim.item',string='Claim Item',required=True,domain="[('risk_objects','=',related_claim)]")
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



