from odoo import api, fields, models
from odoo.exceptions import  ValidationError
from datetime import datetime,timedelta

class Proposals_opp(models.Model):
    _name='proposal.opp.bb'

    proposal_crm = fields.Many2one("crm.lead")
    Company = fields.Many2one('res.partner', domain="[('insurer_type','=',1)]", string="Insurer")
    product_pol = fields.Many2one('insurance.product',domain="[('insurer','=',Company)]", string="Product")
    premium = fields.Float('Premium')
    test=fields.Char(string='type')
    group = fields.Boolean('Groups')
    # ben=fields.One2many(related='product_pol.coverage', invisible=True)
    proposals_covers = fields.One2many('name.covers','rel_policy_broker_id')

    @api.multi
    @api.onchange("proposals_covers")
    def _check_preimum_opp(self):
        for rec in self:
            total = 0.0
            for reco in rec.proposals_covers:
                total += reco.net_perimum

            rec.premium = total


    @api.multi
    @api.onchange("Company", "product_pol")
    def onchange_num_covers_rel_ids_opp(self):
        ids = self.env['insurance.product.coverage'].search([('product_id', '=', self.product_pol.id)])
        # print(ids)
        res = []
        for rec in ids:
            res.append((0, 0, {
                "name": rec.Name,
                "sum_insure": rec.defaultvalue,
                "check": rec.readonly,
                # "rate": rec.product_id.name_cover_ids.covers_rel_ids.rate,
                "net_perimum": rec.readonly and rec.defaultvalue
            }))
        self.proposals_covers = res

    @api.multi
    @api.depends('Company')
    def get_car_proposal(self):
        result = []
        for car in self.proposal_crm.objectcar:
            result.append((0,0,{
                'Man': car.Man, ' model': car.model, 'motor_cc': car.motor_cc, "year_of_made": car.year_of_made
            }))

        self.car_proposal_test = result

    @api.multi
    @api.depends('Company')
    def get_person_proposal(self):
        result = []
        # import pdb;
        # pdb.set_trace()test check for other is it working or not
        for person in self.proposal_crm.objectperson:
            result.append((0, 0, {
                'name': person.name,'DOB': person.DOB, 'job': person.job
            }))

        self.person_proposal_test = result

    @api.multi
    @api.depends('Company')
    def get_cargo_proposal(self):
        result = []
        for cargo in self.proposal_crm.objectcargo:
            result.append((0, 0, {
                'From': cargo.From, 'To': cargo.To, 'cargo_type': cargo.cargo_type, "weight": cargo.weight
            }))

        self.cargo_proposal_test = result

    select_crm = fields.Many2one('crm.lead')

    car_proposal_test = fields.One2many('vehicle.object.opp', 'proposal_car_opp', compute=get_car_proposal ,store=True)
    person_proposal_test = fields.One2many('person.object.opp', 'proposal_person_opp',compute=get_person_proposal ,store=True )
    cargo_proposal_test = fields.One2many('cargo.object.opp', 'proposal_cargo_opp',compute=get_cargo_proposal,store=True)
    # car_proposal_test_selected = fields.One2many(related='car')
    group_proposal = fields.One2many('group.group.opp', 'proposal_group_opp', string='group proposal', readonly=True)





    @api.onchange('Company')
    def settest(self):
        self.test = self.proposal_crm.test

    @api.onchange('Company')
    def setgroup(self):
        self.group = self.proposal_crm.group


    @api.multi
    def select_proposal(self):
        self.proposal_crm.test1 = True
        self.proposal_crm.prop_id = self.id


class ExtraModel(models.Model):
    _name ="name.covers"


    name = fields.Char(string='Name' )
    check1 =fields.Many2one('insurance.product')
    check = fields.Boolean()
    sum_insure = fields.Float(string="SI")
    rate = fields.Float(string="Rate")
    net_perimum = fields.Float(string="Net Perimum")
    rel_policy_broker_id = fields.Many2one("proposal.opp.bb")

    # @api.multi
    # def _nameget(self):
    #       for rec in self:
    #           if rec.check == True:
    #               rec.net_perimum = rec.sum_insure




    @api.onchange("sum_insure","rate")
    def _onchangerate(self):
        for rec in self:
            rec.net_perimum = (rec.sum_insure*rec.rate)/100




            # else:
            #     rec.net_perimum = rec.name.limit



    # @api.multi
    # def unlink(self):
    #     for rec in self:
    #         if rec.name.required:
    #             raise ValidationError(
    #                 ('You cannot delete this record .'))
    #         return super(ExtraModel, self).unlink()




