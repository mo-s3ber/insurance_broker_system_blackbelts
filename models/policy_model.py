import random
import string
from odoo import api, fields, models
from odoo.exceptions import  ValidationError
from datetime import datetime,timedelta

class PolicyBroker(models.Model):
    _name = "policy.broker"
    _rec_name = "std_id"

    @api.model
    def default_get(self, fields):
        res = super(PolicyBroker, self).default_get(fields)
        lead = self.env['crm.lead'].browse(self._context.get('active_id'))


        #pass car new
        recordvehile = self.env['vehicle.object.opp'].search([('id', 'in', lead.objectcar.ids)])
        records_car = []
        for rec in recordvehile:
            objectvehicle = (0, 0, {'Man': rec.Man, ' model': rec.model, 'motor_cc': rec.motor_cc,"year_of_made":rec.year_of_made })
            records_car.append(objectvehicle)

        #.........

        # passing persons......
        recordperson = self.env['person.object.opp'].search([('id', 'in', lead.objectperson.ids)])
        records_person = []
        for rec in recordperson:
            objectperson = (0, 0, {'name': rec.name, 'DOB': rec.DOB, 'job': rec.job})
            records_person.append(objectperson)
        #.........


        # passing cargo...
        recordcargo = self.env['cargo.object.opp'].search([('id', 'in', lead.objectcargo.ids)])
        records_cargo = []
        for rec in recordcargo:
            objectcargo = (
            0, 0, {'From': rec.From, 'To': rec.To, 'cargo_type': rec.cargo_type, "weight": rec.weight})
            records_cargo.append(objectcargo)
        #.......

        recordproposal = self.env['proposal.opp.bb'].search([('id', 'in', lead.proposal_opp.ids)])
        records_proposal = []
        for rec in recordproposal:
            proposal_opp = (0, 0, {'Company': rec.Company.id, 'product_pol': rec.product_pol.id, 'premium': rec.premium})
            records_proposal.append(proposal_opp)

        
        res['insurance_type']=lead.insurance_type
        res['line_of_bussines'] = lead.LOB.id
        res['ins_type'] = lead.ins_type
        res['objectperson'] = records_person
        res['objectvehicle'] = records_car
        res['objectcargo'] = records_cargo
        res['propoasl_ids'] = records_proposal
        res['customer'] = lead.partner_id.id
        res['salesperson'] = lead.user_id.id
        res['std_id'] = lead.policy_number
        return res




    @api.onchange("term","number")
    def _cmpute_date_and_amount(self):
        if self.term == "onetime":
            self.rella_installment_id=[(0,0,{
                "date":self.start_date,
                "amount":self.t_permimum,



            })]
        elif self.term == "year":
            start = fields.Datetime.from_string(self.start_date)
            duration = timedelta(days=365)

            phone_numbers = []
            for i in range(int(self.number)):
                x = (0, 0, {
                    "date": start + duration,
                    "amount": self.t_permimum / int(self.number)

                })
                phone_numbers.append(x)
                duration = duration + timedelta(days=365)
            self.rella_installment_id = phone_numbers
        elif self.term == "quarter":
            start =fields.Datetime.from_string(self.start_date)
            duration = timedelta(days=90)
            phone_numbers = []
            for i in range(4):
                x = (0, 0, {
                        "date": start + duration,
                        "amount": self.t_permimum / 4

                })
                phone_numbers.append(x)
                duration = duration + timedelta(days=90)
            self.rella_installment_id=phone_numbers
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

    def proposalselected(self):
        ids = self.env['proposal.bb'].search([('id', '=',self.prop_id)]).ids
        self.selected_proposal = [(6, 0, ids)]



    @api.onchange('line_of_bussines')
    def _compute_comment(self):
        for record in self:
            record.test = record.line_of_bussines.object


    @api.multi
    @api.constrains('share_policy_rel_ids')
    def _check_something(self):
        total = 0.0
        for rec in self.share_policy_rel_ids:
            total +=rec.share_commition

        if total > 100:
                raise ValidationError("Your share percentage must be under percentage")


    _sql_constraints = [('std_id_uniq', 'unique(std_id)', 'This policy number already exists !')]

    # @api.model
    # def create(self, vals):
    #     seq = self.env['ir.sequence'].next_by_code('policy.broker') or '/'
    #     vals['std_id'] = seq
    #     return super(PolicyBroker, self).create(vals)



    std_id = fields.Char(string="Policy Number")
    issue_date = fields.Date(string="Issue Date")
    start_date = fields.Date(string="Coverage Start On" , required=True)
    end_date = fields.Date(string="Coverage End On")
    term = fields.Selection([("onetime", "One Time"), ("year", "yearly"),("quarter", "Quarterly"), ("month", "Monthly")],  string="payment frequency")
    number = fields.Integer(string="No Of Years", default=1)

    gross_perimum = fields.Float(string="Gross Perimum")
    t_permimum = fields.Float(string="Net Permium", compute="_compute_t_premium")

    commision = fields.Float(string="Brokerage", compute="_compute_brokerage")
    salesperson = fields.Many2one('res.users', string='Salesperson', index=True, default=lambda self: self.env.user)
    onlayer = fields.Selection(related="salesperson.layer", string="Sales Layer")
    personcom = fields.Integer(string="commition", compute="_compute_personcom")
    rel_com_detail_id = fields.One2many("layers.layer", "policy_rel_do_id")
    rella_installment_id = fields.One2many("installment.installment", "installment_rel_id")
    share_policy_rel_ids = fields.One2many("share.commition", "share_commition_rel_id")
    customer=fields.Many2one('res.partner','Customer')



    insurance_type = fields.Selection([('life', 'Life'),
                            ('p&c', 'P&C'),
                            ('health', 'Health'), ],
                           'Insurance Type', track_visibility='onchange')
    ins_type = fields.Selection([('Individual', 'Individual'),
                                 ('Group', 'Group'), ],
                                'insured State', track_visibility='onchange')
    policy_dur = fields.Selection([('Every 6 Months', 'Every 6 Months'),
                                   ('Every Year', 'Every Year'), ],
                                  'Policy Duration', track_visibility='onchange')
    line_of_bussines = fields.Many2one('insurance.line.business', string='Line of business', domain="[('insurance_type','=',insurance_type)]")



    objectvehicle = fields.One2many('vehicle.object', 'object_vehicle', string='Vehicle')#where you are using this fiedl ? in xml
    objectperson = fields.One2many('person.object', 'object_person', string='person')
    objectcargo = fields.One2many('cargo.object', 'object_cargo', string='cargo')
    objectgroup = fields.One2many('group.group', 'object_group', string='Group')
    test = fields.Char()
    group = fields.Boolean()


    propoasl_ids = fields.One2many("proposal.bb", "proposal_policy")
    selected_proposal = fields.One2many('proposal.bb', 'select', compute='proposalselected')
    prop_id = fields.Integer(readonly=True)
    covers = fields.One2many(related='selected_proposal.covers_rel_ids')



    @api.multi
    # @api.onchange("selected_proposal.premium")
    def _compute_t_premium(self):
        for rec in self:
            if rec.selected_proposal:

                rec.t_permimum = rec.selected_proposal.premium

    @api.multi
    # @api.onchange("selected_proposal.product_pol.brokerage", "selected_proposal.premium")
    def _compute_brokerage(self):
        for rec in self:
            if rec.selected_proposal:

                 rec.commision = (rec.selected_proposal.product_pol.brokerage.basic_commission*rec.selected_proposal.premium)/100




    @api.multi
    # @api.onchange("salesperson","onlayer","commision")
    def _compute_personcom(self):
        for rec in self:
            if rec.onlayer == "l1":
                rec.personcom = (rec.selected_proposal.product_pol.commision_id.layer1 * rec.commision) / 100
            elif rec.onlayer == "l2":
                rec.personcom = (rec.selected_proposal.product_pol.commision_id.layer2 * rec.commision) / 100
            elif rec.onlayer == "l3":
                rec.personcom = (rec.selected_proposal.product_pol.commision_id.layer3 * rec.commision) / 100
            elif rec.onlayer == "l4":
                rec.personcom = (rec.selected_proposal.product_pol.commision_id.layer4 * rec.commision) / 100
            elif rec.onlayer == "l5":
                rec.personcom = (rec.selected_proposal.product_pol.commision_id.layer5 * rec.commision) / 100
            elif rec.onlayer == "l6":
                rec.personcom = (rec.selected_proposal.product_pol.commision_id.layer6 * rec.commision) / 100
            elif rec.onlayer == "l7":
                rec.personcom = (rec.selected_proposal.product_pol.commision_id.layer7 * rec.commision) / 100
            else:
                rec.personcom = (rec.selected_proposal.product_pol.commision_id.layer8 * rec.commision) / 100

    # @api.multi
    # @api.onchange('selected_proposal ')
    # def _compute_session_costs_control(self):
    #     for record in self:
    #         record.commision = (record.selected_proposal.product_pol.commision_id.product_commision * record.t_permimum)/100

    @api.multi
    @api.onchange("salesperson")
    def onchange_objectx(self):
        # x = self.env['crm.team'].search([('user_id', '=', self.salesperson), ('member_ids', '=', self.salesperson)])
        # x = self.env["crm.team"].browse(["user_id"])
        # y = self.env["hr.department"].browse(["parent_id"])
        # for rec in self.rel_user.name:
        #     if rec.salesperson in rec.rel_user.member_ids:
        #         leader = rec.rel_user.user_id
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

class ExtraModel(models.Model):
    _name ="name.covers"


    name = fields.Char(string='Name')
    check1 =fields.Many2one('insurance.product')
    check = fields.Boolean()
    sum_insure = fields.Float(string="SI")
    rate = fields.Float(string="Rate")
    net_perimum = fields.Float(string="Net Perimum")
    rel_policy_broker_id = fields.Many2one("proposal.bb")

    @api.multi
    def _nameget(self):
          for rec in self:
              if rec.check == True:
                  rec.net_perimum = rec.sum_insure




    @api.onchange("sum_insure","rate")
    def _onchangerate(self):
        for rec in self:
            rec.net_perimum = (rec.sum_insure*rec.rate)/100




            # else:
            #     rec.net_perimum = rec.name.limit



    @api.multi
    def unlink(self):
        for rec in self:
            if rec.name.required:
                raise ValidationError(
                    ('You cannot delete this record .'))
            return super(ExtraModel, self).unlink()




class ShareCommition(models.Model):
    _name="share.commition"

    agent= fields.Many2one("res.users", string="Agent")
    share_commition = fields.Float(string="Share")
    amount = fields.Float(string="Amount" , compute="_compute_amount")
    share_commition_rel_id = fields.Many2one("policy.broker")



    @api.one
    def _compute_amount(self):
        self.amount = (self.share_commition_rel_id.personcom * self.share_commition)/100




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
    _rec_name="agent"


    agent = fields.Many2one("res.users", string="Agent")
    l1 = fields.Char(string="Layer")
    allocation_layer1 = fields.Float(string="allocation",compute="_com_sum_one_name")

    portion1 = fields.Float(string="portion",compute="_com_sum_two_name")
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
            elif record.l1 == 'l6':

                record.allocation_layer1 = record.policy_rel_do_id.propoasl_ids.product_pol.commision_id.layer6
            elif record.l1 == 'l7':

                record.allocation_layer1 = record.policy_rel_do_id.propoasl_ids.product_pol.commision_id.layer7
            else:

                record.allocation_layer1 = record.policy_rel_do_id.propoasl_ids.product_pol.commision_id.layer8


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
            elif record.l1 == 'l6':
                    record.portion1 = (record.allocation_layer1 * record.policy_rel_do_id.commision) / 100
            elif record.l1 == 'l7':
                record.portion1 = (record.allocation_layer1 * record.policy_rel_do_id.commision) / 100
            else:
                record.portion1 = (record.allocation_layer1 * record.policy_rel_do_id.commision) / 100

class CommisionSetup(models.Model):
    _name = "commision.setup"
    _rec_name="date"


    agency=fields.Char(string="Agency")
    date = fields.Date(string="Date")
    policy_relation_id = fields.Many2one("policy.broker")
    insrance_policy_type = fields.Selection(related="policy_relation_id.insurance_type" ,string="Insurance_Type")
    # product_id = fields.Many2one("insurance.product", string="Product type ")
    insurer_id = fields.Many2one("res.partner",string="Insurer")
    product_commision = fields.Float(string="Product Commision")
    layer1 = fields.Float(string="L1 ")
    layer2 = fields.Float(string="L2 ")
    layer3 = fields.Float(string="L3 ")
    layer4 = fields.Float(string="L4 ")
    layer5 = fields.Float(string="L5 ")
    layer6 = fields.Float(string="L6 ")
    layer7 = fields.Float(string="L7 ")
    layer8 = fields.Float(string="L8 ")

class InheritUsers(models.Model):
    _inherit = "res.users"

    layer = fields.Selection([("l1", "Layer 1"), ("l2", "Layer 2"), ("l3", "Layer 3"), ("l4", "Layer 4"), ("l5", "Layer 5"), ("l6", "Layer 6"),("l7", "Layer 7"), ("l8", "Layer 8")], string="Layer" , required=True)

class InheritSale(models.Model):
    _inherit = "crm.lead"


