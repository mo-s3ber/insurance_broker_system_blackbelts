import random
import string
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class PolicyBroker(models.Model):
    _name = "policy.broker"
    _rec_name = "std_id"

    # @api.multi
    # def create_proposal(self):
    #     form_view = self.env.ref('insurance_broker_system_blackbelts.my_view_for_policy_form2')
    #     return {
    #         'name': ('policy Form2'),
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'views': [(form_view.id, 'form')],
    #         'res_model': 'proposal.bb',
    #         'target': 'current',
    #         'type': 'ir.actions.act_window',
    #         'context': {"default_proposal_policy":self.id
    #
    #         }
    #     }







    @api.model
    def default_get(self, fields):
        res = super(PolicyBroker, self).default_get(fields)
        if self._context.get('active_model') == 'crm.lead':
            # return res
            lead = self.env['crm.lead'].browse(self._context.get('active_id'))

            recordrisks = self.env['risks.opp'].search([('id', 'in', lead.objectrisks.ids)])
            records_risks = []
            for rec in recordrisks:
                objectrisks = (
                    0, 0, {'risk': rec.risk_id, ' risk_description': rec.risk_desc})
                records_risks.append(objectrisks)




            # recordproposal = self.env['proposal.opp.bb'].search([('id', 'in', lead.proposal_opp.ids)])
            # records_proposal = []
            # for rec in recordproposal:
            #     proposal_opp = (
            #     0, 0, {'Company': rec.Company.id, 'product_pol': rec.product_pol.id, 'premium': rec.premium})
            #     records_proposal.append(proposal_opp)

            res['insurance_type'] = lead.insurance_type
            res['line_of_bussines'] = lead.LOB.id
            res['ins_type'] = lead.ins_type
            # res['propoasl_ids'] = records_proposal
            res['new_risk_ids'] = records_risks
            res['customer'] = lead.partner_id.id
            res['salesperson'] = lead.user_id.id
            res['std_id'] = lead.policy_number
            # res['test_computed'] = lead.test_computed


        if self._context.get('active_model') == 'renewal.again':
            lead = self.env['renewal.again'].browse(self._context.get('active_id'))

            riskrecord = self.env["new.risks"].search([('id', 'in', lead.old_number.new_risk_ids.ids)])
            records_cargoo = []
            for rec in riskrecord:
                objectcargoo = (
                    0, 0, {'risk': rec.risk, 'risk_description': rec.risk_description})
                records_cargoo.append(objectcargoo)

            recordproposal = self.env['proposal.bb'].search([('id', 'in', lead.old_number.propoasl_ids.ids)])
            records_proposal = []
            for rec in recordproposal:
                proposal_opp = (
                    0, 0, {'Company': rec.Company.id, 'product_pol': rec.product_pol.id, 'premium': rec.premium})
                records_proposal.append(proposal_opp)

            res['policy_number'] = lead.new_number
            res['std_id'] = lead.old_number.std_id
            res['issue_date'] = lead.issue_date
            res['start_date'] = lead.start_date
            res['end_date'] = lead.end_date
            res['test'] = lead.old_number.test

            res['customer'] = lead.old_number.customer.id
            res['holding_cam'] = lead.old_number.holding_cam
            res['insurance_type'] = lead.old_number.insurance_type
            res['line_of_bussines'] = lead.old_number.line_of_bussines.id
            res['ins_type'] = lead.old_number.ins_type

            res['new_risk_ids'] = records_cargoo
            res['propoasl_ids'] = records_proposal

        return res

<<<<<<< HEAD


<<<<<<< HEAD
=======
    # @api.model
    # def default_get(self, fields):
    #     res = super(PolicyBroker, self).default_get(fields)
    #     lead = self.env['renewal.again'].browse(self._context.get('active_id'))
    #
    #     riskrecord = self.env["new.risks"].search([('id', 'in', lead.old_number.new_risk_ids.ids)])
    #     records_cargoo = []
    #     for rec in riskrecord:
    #         objectcargoo = (
    #             0, 0, {'risk': rec.risk, 'risk_description': rec.risk_description})
    #         records_cargoo.append(objectcargoo)
    #
    #
    #     recordproposal = self.env['proposal.bb'].search([('id', 'in', lead.old_number.propoasl_ids.ids)])
    #     records_proposal = []
    #     for rec in recordproposal:
    #         proposal_opp = (
    #             0, 0, {'Company': rec.Company.id, 'product_pol': rec.product_pol.id, 'premium': rec.premium})
    #         records_proposal.append(proposal_opp)
    #
    #     res['policy_number'] = lead.new_number
    #     res['std_id'] = lead.old_number.std_id
    #     res['issue_date'] = lead.issue_date
    #     res['start_date'] = lead.start_date
    #     res['end_date'] = lead.end_date
    #     res['test'] = lead.old_number.test
    #
    #     res['customer'] = lead.old_number.customer.id
    #     res['holding_cam'] = lead.old_number.holding_cam
    #     res['insurance_type'] = lead.old_number.insurance_type
    #     res['line_of_bussines'] = lead.old_number.line_of_bussines.id
    #     res['ins_type'] = lead.old_number.ins_type
    #
    #     res['new_risk_ids'] = records_cargoo
    #     res['propoasl_ids'] = records_proposal
    #
    #     return res

=======
<<<<<<< HEAD
>>>>>>> 04c237543c50c9224795509ef5da60e0ab3603fc

    # @api.model
    # def default_get(self, fields):
    #     res = super(PolicyBroker, self).default_get(fields)
    #     lead = self.env['renewal.again'].browse(self._context.get('active_id'))
    #
    #     riskrecord = self.env["new.risks"].search([('id', 'in', lead.old_number.new_risk_ids.ids)])
    #     records_cargoo = []
    #     for rec in riskrecord:
    #         objectcargoo = (
    #             0, 0, {'risk': rec.risk, 'risk_description': rec.risk_description})
    #         records_cargoo.append(objectcargoo)


        # recordproposal = self.env['proposal.bb'].search([('id', 'in', lead.old_number.propoasl_ids.ids)])
        # records_proposal = []
        # for rec in recordproposal:
        #     proposal_opp = (
        #         0, 0, {'Company': rec.Company.id, 'product_pol': rec.product_pol.id, 'premium': rec.premium})
        #     records_proposal.append(proposal_opp)

        # res['policy_number'] = lead.new_number
        # res['std_id'] = lead.old_number.std_id
        # res['issue_date'] = lead.issue_date
        # res['start_date'] = lead.start_date
        # res['end_date'] = lead.end_date
        # # res['Test'] = lead.old_number.Test
        #
        # res['customer'] = lead.old_number.customer.id
        # res['insurance_type'] = lead.old_number.insurance_type
        # res['line_of_bussines'] = lead.old_number.line_of_bussines.id
        # res['ins_type'] = lead.old_number.ins_type
        #
        # res['new_risk_ids'] = records_cargoo


        return res
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 60da00b23ccb9222cf1ccd4ce21144593f9a4117

>>>>>>> 04c237543c50c9224795509ef5da60e0ab3603fc

    @api.onchange("term", "number")
    def _cmpute_date_and_amount(self):
        if self.term == "onetime":
            self.rella_installment_id = [(0, 0, {
                "date": self.start_date,
                "amount": self.t_permimum,

            })]
        elif self.term == "year":
            start = fields.Datetime.from_string(self.start_date)
            duration = timedelta(days=365)

            phone_numbers = []
            for i in range(int(self.number)):
                x = (0, 0, {
                    "date": start + duration,
                    "amount": self.t_permimum / 1

                })
                phone_numbers.append(x)
                duration = duration + timedelta(days=365)
            self.rella_installment_id = phone_numbers
        elif self.term == "quarter":
            start = fields.Datetime.from_string(self.start_date)
            duration = timedelta(days=90)
            phone_numbers = []
            for i in range(4):
                x = (0, 0, {
                    "date": start + duration,
                    "amount": self.t_permimum / 4

                })
                phone_numbers.append(x)
                duration = duration + timedelta(days=90)
            self.rella_installment_id = phone_numbers
        elif self.term == "month":
            start = fields.Datetime.from_string(self.start_date)
            duration = timedelta(days=30)
            phone_numbers = []
            for i in range(12):
                x = (0, 0, {
                    "date": start + duration,
                    "amount": self.t_permimum / 12

                })
                phone_numbers.append(x)
                duration = duration + timedelta(days=30)
            self.rella_installment_id = phone_numbers

    # def proposalselected(self):
    #     ids = self.env['proposal.bb'].search([('id', '=', self.prop_id)]).ids
    #     self.selected_proposal = [(6, 0, ids)]

    @api.onchange('line_of_bussines')
    def _compute_comment(self):
        for record in self:
            record.check_item = record.line_of_bussines.object


    @api.multi
    @api.constrains('share_policy_rel_ids')
    def _check_something(self):
        total = 0.0
        for rec in self.share_policy_rel_ids:
            total += rec.share_commition

        if total > 100:
            raise ValidationError("Your share percentage must be under percentage")

=======
<<<<<<< HEAD

    @api.multi
    @api.onchange('bool')
    def setcovers_veh(self):
        ids = self.env['insurance.product.coverage'].search(
            [('product_id', '=', self.product_policy.id)])
        print(ids)
        if self.bool:
            print('xxx')
            for record in self.new_risk_ids:
                 for rec in ids:
                     print('i enter')
                     record.name_cover_risk_ids =(0, 0, {
                         "name": rec.Name,
                         "sum_insure": rec.defaultvalue,
                         "check": rec.readonly,
                         # "rate": rec.product_id.name_cover_ids.covers_rel_ids.rate,
                         "net_perimum": rec.readonly and rec.defaultvalue
                     })


    bool = fields.Boolean()
    edit_number = fields.Integer(string="Endorsement Number", readonly=True)
    edit_decr = fields.Text('Endorsement Description', readonly=True)
    ediet_number = fields.Char('Endorsement Policy Number')
<<<<<<< HEAD

=======
=======
>>>>>>> 60da00b23ccb9222cf1ccd4ce21144593f9a4117
    _sql_constraints = [('std_id_uniq', 'unique(std_id)', 'This policy number already exists !')]

    # @api.model
    # def create(self, vals):
    #     seq = self.env['ir.sequence'].next_by_code('policy.broker') or '/'
    #     vals['std_id'] = seq
    #     return super(PolicyBroker, self).create(vals)
<<<<<<< HEAD

=======
>>>>>>> 60da00b23ccb9222cf1ccd4ce21144593f9a4117
>>>>>>> 04c237543c50c9224795509ef5da60e0ab3603fc




    policy_number = fields.Char(string="Renewal Policy Number")
    renwal_check = fields.Boolean(string="Renewal")
    holding_cam = fields.Char(string="Holding Campany")

    std_id = fields.Char(string="Policy Number" ,required=True)
    issue_date = fields.Date(string="Issue Date")
    start_date = fields.Date(string="Coverage Start On", required=True)
    end_date = fields.Date(string="Coverage End On")



    term = fields.Selection(
        [("onetime", "One Time"), ("year", "yearly"), ("quarter", "Quarterly"), ("month", "Monthly")],
        string="payment frequency")
    number = fields.Integer(string="No Of Years", default=1)
    barnche = fields.Char("Branch")

    gross_perimum = fields.Float(string="Gross Perimum")
    t_permimum = fields.Float(string="Net Permium", compute="_compute_t_premium")

    salesperson = fields.Many2one('res.users', string='Salesperson', index=True, default=lambda self: self.env.user)
    onlayer = fields.Selection(related="salesperson.layer", string="Sales Layer")
    personcom = fields.Integer(string="commission",compute="_compute_personcom")
    rel_com_detail_id = fields.One2many("layers.layer", "policy_rel_do_id")
    rella_installment_id = fields.One2many("installment.installment", "installment_rel_id")
    share_policy_rel_ids = fields.One2many("share.commition", "share_commition_rel_id")
    customer = fields.Many2one('res.partner', 'Customer')

<<<<<<< HEAD
    test_computed=fields.Char('')
=======

>>>>>>> 60da00b23ccb9222cf1ccd4ce21144593f9a4117

    insurance_type = fields.Selection([('life', 'Life'),
                                       ('p&c', 'P&C'),
                                       ('health', 'Health'), ],
                                      'Insurance Type', track_visibility='onchange')
    ins_type = fields.Selection([('Individual', 'Individual'),
                                 ('Group', 'Group'), ],
                                'I&G', track_visibility='onchange')
    # policy_dur = fields.Selection([('Every 6 Months', 'Every 6 Months'),
    #                                ('Every Year', 'Every Year'), ],
    #                               'Policy Duration', track_visibility='onchange')
    line_of_bussines = fields.Many2one('insurance.line.business', string='Line of business',
                                       domain="[('insurance_type','=',insurance_type)]")

    check_item = fields.Char()
    group = fields.Boolean()

    # propoasl_ids = fields.One2many("proposal.bb", "proposal_policy", readonly=True)
    # selected_proposal = fields.One2many('proposal.bb', 'select', compute='proposalselected')
    # prop_id = fields.Integer(readonly=True)
    # covers = fields.One2many(related='selected_proposal.covers_rel_ids')

    commision = fields.Float(string="Basic Brokerage", compute="_compute_brokerage")
    com_commision = fields.Float(string="Complementary  Brokerage", compute="_compute_com_commision")
    fixed_commision = fields.Float(string="Fixed Brokerage", compute="_compute_fixed_commision")
    earl_commision = fields.Float(string="Early Collection" , compute="_compute_earl_commision")
    total_commision = fields.Float(string="total Brokerage", compute="_compute_sum")
    new_risk_ids = fields.One2many("new.risks", 'policy_risk_id', string='Risk')
    company = fields.Many2one('res.partner', domain="[('insurer_type','=',1)]", string="Insurer")
    product_policy = fields.Many2one('insurance.product',domain="[('insurer','=',company)]", string="Product")
    hamda = fields.Many2one("new.risks")

    name_cover_rel_ids = fields.One2many("covers.lines","policy_rel_id",string="Covers Details" )
    name_rel_ids = fields.One2many("name.covers","policy_name_cover_id")
    currency_id = fields.Many2one("res.currency","Currency Code")
    benefit =fields.Char("Beneifciary")

    checho = fields.Boolean()
    count_claim = fields.Integer()


    # @api.multi
    # def _onchang_risk(self):
    #     res = []
    #     ids = self.env["new.risks"].search([('id', '=', self.hamda.id)])
    #     for id in ids:
    #         print(id.name_cover_risk_ids.ids)
    #         self.name_cover_rel_ids = [(6, 0, id.name_cover_risk_ids.ids)]


    @api.multi
    @api.depends("name_cover_rel_ids")
    def _compute_t_premium(self):
        total = 0.0
        for line in self.name_cover_rel_ids:
            total += line.net_perimum
        self.t_permimum = total


    @api.multi
    @api.depends("product_policy")
    def _compute_brokerage(self):
        for rec in self:
            rec.commision = (rec.product_policy.brokerage.basic_commission * rec.t_permimum) / 100

    @api.multi
    @api.depends("product_policy")
    def _compute_com_commision(self):
        for rec in self:
            rec.com_commision = (rec.product_policy.brokerage.complementary_commission * rec.t_permimum) / 100

    @api.multi
    @api.depends("product_policy")
    def _compute_earl_commision(self):
        for rec in self:
                rec.earl_commision = (rec.product_policy.brokerage.early_collection * rec.t_permimum) / 100


    @api.multi
    @api.depends("product_policy")
    def _compute_fixed_commision(self):
        for rec in self:
                rec.fixed_commision = (rec.product_policy.brokerage.fixed_commission * rec.t_permimum) / 100

    @api.multi
    def _compute_sum(self):
        for rec in self:
            rec.total_commision = rec.commision + rec.com_commision + rec.fixed_commision

    @api.multi
    @api.depends("salesperson","onlayer","t_permimum")
    def _compute_personcom(self):
        if self.onlayer == "l1":
            self.personcom = (self.product_policy.commision_id.layer1 * self.t_permimum) / 100
        elif self.onlayer == "l2":
            self.personcom = (self.product_policy.commision_id.layer2 * self.t_permimum) / 100
        elif self.onlayer == "l3":
            self.personcom = (self.product_policy.commision_id.layer3 * self.t_permimum) / 100
        elif self.onlayer == "l4":
            self.personcom = (self.product_policy.commision_id.layer4 * self.t_permimum) / 100
        elif self.onlayer == "l5":
            self.personcom = (self.product_policy.commision_id.layer5 * self.t_permimum) / 100


    @api.multi
    @api.onchange("salesperson")
    def onchange_objectx(self):
        for rec in self:
            self.rel_com_detail_id = [
                (0, 0, {
                    "agent": rec.salesperson,
                    "l1": rec.salesperson.layer,
                    "allocation_layer1": rec.rel_com_detail_id.allocation_layer1,
                    "portion1": rec.rel_com_detail_id.portion1
                })]

    @api.multi
    @api.onchange("salesperson")
    def onchange_num_objectx(self):
        for rec in self:
            self.share_policy_rel_ids = [
                (0, 0, {
                    "agent": rec.salesperson,
                    "share_commition": rec.share_policy_rel_ids.share_commition,
                    "amount": rec.share_policy_rel_ids.amount
                })]

    @api.multi
    def generate_covers(self):
        self.checho = True
        return True

class Extra_Covers(models.Model):
    _name = "covers.lines"
    _rec_name="riskk"


    rel_risk = fields.Many2one("new.risks")
    risko = fields.Char(related="rel_risk.risk")

<<<<<<< HEAD
=======
<<<<<<< HEAD

    name = fields.Char(string='Name' )

    name = fields.Char('')

=======
<<<<<<< HEAD
>>>>>>> 04c237543c50c9224795509ef5da60e0ab3603fc
    riskk = fields.Many2one("new.risks", "Risk ID")
    risk_description = fields.Text(string="Risk Description")
    #
    insurerd = fields.Many2one(related="policy_rel_id.company")
    prod_product = fields.Many2one(related="policy_rel_id.product_policy",domain="[('insurer','=',insurerd)]")

    name1 = fields.Many2one("insurance.product.coverage",string="Cover", domain="[('product_id', '=' , prod_product)]")
    check = fields.Boolean(related="name1.readonly")
<<<<<<< HEAD
    # name = fields.Char(string='Name' )
    # check1 = fields.Many2one('insurance.product')
    # check = fields.Boolean()
=======
=======
    name = fields.Char(string='Name' )
    name = fields.Char('')
>>>>>>> 60da00b23ccb9222cf1ccd4ce21144593f9a4117
    check1 = fields.Many2one('insurance.product')
    check = fields.Boolean()
>>>>>>> b77b9a302b8e16e1aec30841b5e7856c066daaad
>>>>>>> 04c237543c50c9224795509ef5da60e0ab3603fc
    sum_insure = fields.Float(string="SI")
    rate = fields.Float(string="Rate")
    net_perimum = fields.Float(string="Net Perimum")
    policy_rel_id = fields.Many2one("policy.broker")


    @api.onchange("check")
    def _nameget(self):
        if self.check == True:
            self.net_perimum = self.sum_insure


    @api.onchange('policy_rel_id')
    def onchange_field_id(self):
        if self.policy_rel_id:
           return {'domain': {"riskk": [('id', 'in', self.policy_rel_id.new_risk_ids.ids)]}}

    # @api.onchange('policy_rel_id')
    # def _change_domain(self):
    #     if self.policy_rel_id:
    #         ids = self.env["policy.broker"].search([])
    #         return {
    #             "domain":{
    #                 "riskk":[('risk','in',[ids.new_risk_ids.ids])]
    #             }
    #         }

    @api.onchange('name1')
    def onchange_covers(self):
        if self.name1:
            self.sum_insure = self.name1.defaultvalue

    @api.onchange('rate')
    def compute_premium(self):
        if self.name1:
            self.net_perimum = (self.sum_insure * self.rate) / 100

    @api.onchange('riskk')
    def onchange_risc_desc(self):
        if self.riskk:
            self.risk_description = self.riskk.risk_description

    #     res = {}
    #     self.riskk = False
    #     if self.policy_rel_id.new_risk_ids:
    #         print("khaled")
    #         ids = self.env["policy.broker"].browse([self.policy_rel_id.new_risk_ids])
    #         print(ids)
    #         # ids = self.policy_rel_id.new_risk_ids.mapped('id')
    #         # print(ids)
    #         # for rec in ids:
    #         #     self.riskk = rec.risk
    #     #     res['domain'] = {'riskk': [('risk', 'in', ids)]}
    #     #     print(res)
    #     # return res

    # @api.multi
    # def _compute_risk(self):
    #     bns = self.env["new.risks"].search([('risk', '=', self.policy_rel_id.new_risk_ids.id)])
    #     print(bns.ids)
    #     for rec in bns.ids:
    #         self.riskk = rec.risk


    # @api.multi
    # def _compute_coverage(self):
    #     obj = self.env['insurance.product.coverage'].search([('product_id','=',self.policy_rel_id.product_policy.id)])
    #     print(obj.ids)
    #     for rec in obj.ids:
    #         self.name = rec.Name
    #         self.check = rec.readonly
    #         self.sum_insure = rec.defaultvalue




class ExtraModel(models.Model):
    _name = "name.covers"
    # _rec_name="name"
    #
    # name = fields.Char(string='Name' )
    # check1 = fields.Many2one('insurance.product')
    # check = fields.Boolean()
    # sum_insure = fields.Float(string="SI")
    # rate = fields.Float(string="Rate")
    # net_perimum = fields.Float(string="Net Perimum")
    #
    #







    risk_brokerd_id = fields.Many2one("new.risks")
    policy_name_cover_id = fields.Many2one("policy.broker")

    rel_policy_broker_id = fields.Many2one("proposal.bb")
    rel_policy_brokerd_id = fields.Many2one("proposal.opp.bb")
    vechile=fields.Many2one('vehicle.object.opp')
    person = fields.Many2one('person.object.opp')
    cargo=fields.Many2one('cargo.object.opp')
    selected=fields.Many2one('proposal.opp.bb')
    risks=fields.Many2one('risks.opp')




<<<<<<< HEAD
=======
    # @api.multi
    # def _nameget(self):
    #     for rec in self:
    #         if rec.check == True:
    #             rec.net_perimum = rec.sum_insure
    #
    # @api.onchange("sum_insure", "rate")
    # def _onchangerate(self):
<<<<<<< HEAD
=======
=======
>>>>>>> 60da00b23ccb9222cf1ccd4ce21144593f9a4117
>>>>>>> 04c237543c50c9224795509ef5da60e0ab3603fc
    # @api.onchange('user_id')
    # def onchange_user_id(self):
    #   if self.user_id and self.env.uid != 1 :
    #        return {'domain':{'user_id': [('id','in',[self.env.uid,1])]}}

    # @api.multi
    # @api.onchange('prod1')
    # def coversname(self):
    #     print('fvdsv')
    #     if self.prod1:
    #         print('vrennnnnnnn')
    #         rec = self.env['insurance.product.coverage'].search(
    #             [('product_id', '=', self.prod1.id)])
    #         return  {'domain':{'name': [('id','in',rec.ids)]}}
<<<<<<< HEAD
=======

>>>>>>> 60da00b23ccb9222cf1ccd4ce21144593f9a4117
    @api.multi
    def _nameget(self):
        for rec in self:
            if rec.check == True:
                rec.net_perimum = rec.sum_insure

    @api.onchange("sum_insure", "rate")
    def _onchangerate(self):
        for rec in self:
            rec.net_perimum = (rec.sum_insure * rec.rate) / 100

    # @api.multi
    # def unlink(self):
    #     for rec in self:
    #         rec.net_perimum = (rec.sum_insure * rec.rate) / 100
    #
    # # @api.multi
    # # def unlink(self):
    # #     for rec in self:
    #         if rec.name.required:
    #             raise ValidationError(
    #                 ('You cannot delete this record .'))
    #         return super(ExtraModel, self).unlink()


class ShareCommition(models.Model):
    _name = "share.commition"

    agent = fields.Many2one("res.users", string="Agent")
    share_commition = fields.Float(string="Share")
    amount = fields.Float(string="Amount", compute="_compute_amount")
    share_commition_rel_id = fields.Many2one("policy.broker")

    @api.one
    def _compute_amount(self):
        self.amount = (self.share_commition_rel_id.personcom * self.share_commition) / 100


class InstallmentClass(models.Model):
    _name= "installment.installment"
    _rec_name = "date"

    date = fields.Date(string="Date")
    # enddate = fields.Date(string="End of premium")
    amount = fields.Float(string="Amount")
    paid = fields.Selection([('inv', 'Paid Invoice'),
                            ('bill', 'Paid Bill'),
                            ('brok', 'Paid Brokerage'),
                             ('comm', 'Paid Commission'),
                             ('draft', 'Draft'),],
                           'Paid Status',defualt='draft')
    installment_rel_id = fields.Many2one("policy.broker")

    @api.multi
    def create_inv(self):
        form_id = self.env.ref('account.invoice_form')
        self.write({'paid': 'inv'})
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(form_id.id, 'form')],
            'res_model': 'account.invoice',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {'default_name': self.installment_rel_id.std_id,
                        'default_origin': 'Customer Invoice',
                        'default_type': 'out_invoice',
                        'default_account_id': self.installment_rel_id.customer.property_account_receivable_id.id,
                        'default_partner_id': self.installment_rel_id.customer.id,
                        'default_invoice_line_ids':[(0, 0, {
                                            'name': self.installment_rel_id.selected_proposal.product_pol.product_name,
                                            'account_id': self.installment_rel_id.selected_proposal.product_pol.income_account.id,
                                            'price_unit': self.amount,
                                            'quantity': 1.0,
                                            'sale_line_ids': False,
                                            'invoice_line_tax_ids': False,
                                            'account_analytic_id': False,
                                        })],},
            'flags': {'tree': {'action_buttons': True}, 'form': {'action_buttons': True}, 'action_buttons': True},
        }


    @api.multi
    def create_bill(self):
        form_id = self.env.ref('account.invoice_supplier_form')
        self.write({'paid': 'bill'})
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(form_id.id, 'form')],
            'res_model': 'account.invoice',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {'default_name': self.installment_rel_id.std_id,
                        'default_origin': 'Insurer Bill',
                        'default_type': 'in_invoice',
                        'default_account_id': self.installment_rel_id.selected_proposal.Company.property_account_receivable_id.id,
                        'default_partner_id': self.installment_rel_id.selected_proposal.Company.id,
                        'default_invoice_line_ids':[(0, 0, {
                                            'name': self.installment_rel_id.selected_proposal.product_pol.product_name,
                                            'account_id': self.installment_rel_id.selected_proposal.product_pol.expense_account.id,
                                            'price_unit': self.amount,
                                            'quantity': 1.0,
                                            'sale_line_ids': False,
                                            'invoice_line_tax_ids': False,
                                            'account_analytic_id': False,
                                        })],},
            'flags': {'tree': {'action_buttons': True}, 'form': {'action_buttons': True}, 'action_buttons': True},
        }

    @api.multi
    def create_brok(self):
        form_id = self.env.ref('account.invoice_form')
        self.write({'paid': 'brok'})
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(form_id.id, 'form')],
            'res_model': 'account.invoice',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {'default_name': self.installment_rel_id.std_id,
                        'default_origin': 'Brokerage Invoice',
                        'default_type': 'out_invoice',
                        'default_account_id': self.installment_rel_id.selected_proposal.Company.property_account_receivable_id.id,
                        'default_partner_id': self.installment_rel_id.selected_proposal.Company.id,
                        'default_invoice_line_ids':[(0, 0, {
                                            'name': self.installment_rel_id.selected_proposal.product_pol.product_name,
                                            'account_id': self.installment_rel_id.selected_proposal.product_pol.income_account.id,
                                            'price_unit': self.amount,
                                            'quantity': 1.0,
                                            'sale_line_ids': False,
                                            'invoice_line_tax_ids': False,
                                            'account_analytic_id': False,
                                        })],},
            'flags': {'tree': {'action_buttons': True}, 'form': {'action_buttons': True}, 'action_buttons': True},
        }

    @api.multi
    def create_commission_bills(self):
        bill_obj = self.env['account.invoice']
        comm=self.installment_rel_id.share_policy_rel_ids
        for record in comm:
            bill = bill_obj.create({
                'name': self.installment_rel_id.std_id,
                'origin': 'Commission Bill',
                'type': 'out_invoice',
                'reference': False,
                'account_id': record.agent.property_account_receivable_id.id,
                'partner_id': record.agent.id,
                'partner_shipping_id': False,
                'invoice_line_ids': [(0, 0, {
                    'name': self.installment_rel_id.selected_proposal.product_pol.product_name,
                    'account_id': self.installment_rel_id.selected_proposal.product_pol.expense_account.id,
                    'price_unit': record.amount,
                    'quantity': 1.0,
                    'discount': 0.0,
                    'uom_id': False,
                    'sale_line_ids': False,
                    'invoice_line_tax_ids': False,
                    'account_analytic_id': False,
                })],
            })
            return bill


class Layers(models.Model):
    _name = "layers.layer"
    _rec_name = "agent"

    agent = fields.Many2one("res.users", string="Agent")
    l1 = fields.Char(string="Layer")
    allocation_layer1 = fields.Float(string="allocation", compute="_com_sum_one_name")

    portion1 = fields.Float(string="portion", compute="_com_sum_two_name")
    com_rel_ids = fields.Many2one("commision.setup")

    policy_rel_do_id = fields.Many2one("policy.broker")

    @api.multi
    @api.onchange("agent")
    def _compute_lay(self):
        for rec in self:
            rec.l1 = rec.agent.layer

    @api.multi
    def _com_sum_one_name(self):
        for record in self:
            if record.l1 == 'l1':
                record.allocation_layer1 = record.policy_rel_do_id.propoasl_ids.product_pol.commision_id.layer1
            elif record.l1 == 'l2':

                record.allocation_layer1 = record.policy_rel_do_id.propoasl_ids.product_pol.commision_id.layer2
            elif record.l1 == 'l3':

                record.allocation_layer1 = record.policy_rel_do_id.propoasl_ids.product_pol.commision_id.layer3
            elif record.l1 == 'l4':

                record.allocation_layer1 = record.policy_rel_do_id.propoasl_ids.product_pol.commision_id.layer4
            elif record.l1 == 'l5':

                record.allocation_layer1 = record.policy_rel_do_id.propoasl_ids.product_pol.commision_id.layer5

    @api.multi
    def _com_sum_two_name(self):
        for record in self:
            if record.l1 == 'l1':
                record.portion1 = (record.allocation_layer1 * record.policy_rel_do_id.commision) / 100
            elif record.l1 == 'l2':
                record.portion1 = (record.allocation_layer1 * record.policy_rel_do_id.commision) / 100
            elif record.l1 == 'l3':
                record.portion1 = (record.allocation_layer1 * record.policy_rel_do_id.commision) / 100
            elif record.l1 == 'l4':
                record.portion1 = (record.allocation_layer1 * record.policy_rel_do_id.commision) / 100
            elif record.l1 == 'l5':
                record.portion1 = (record.allocation_layer1 * record.policy_rel_do_id.commision) / 100


class CommisionSetup(models.Model):
    _name = "commision.setup"
    _rec_name = "date_from"

    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")
    policy_relation_id = fields.Many2one("insurance.product")
    layer1 = fields.Float(string="L1 ")
    layer2 = fields.Float(string="L2 ")
    layer3 = fields.Float(string="L3 ")
    layer4 = fields.Float(string="L4 ")
    layer5 = fields.Float(string="L5 ")


class InheritUsers(models.Model):
    _inherit = "res.users"

    layer = fields.Selection(
        [("l1", "Layer 1"), ("l2", "Layer 2"), ("l3", "Layer 3"), ("l4", "Layer 4"), ("l5", "Layer 5"),
         ("l6", "Layer 6"), ("l7", "Layer 7"), ("l8", "Layer 8")], string="Layer", required=True)


class InheritSale(models.Model):
    _inherit = "crm.lead"


