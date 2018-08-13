from odoo import api, fields, models

class Proposals(models.Model):
    _name='proposal.bb'

    proposal_policy=fields.Many2one("policy.broker")
    Company = fields.Many2one('res.partner', domain="[('insurer_type','=',1)]", string="Insurer")
    product_pol = fields.Many2one('insurance.product',domain="[('insurer','=',Company)]", string="Product")
    premium = fields.Float('Premium')
    test=fields.Char(string='type')
    group = fields.Boolean('Groups')
    # ben=fields.One2many(related='product_pol.coverage', invisible=True)
    covers_rel_ids = fields.One2many("name.covers", "rel_policy_broker_id")

    @api.multi
    @api.onchange("covers_rel_ids")
    def _check_preimum(self):
        for rec in self:
            total = 0.0
            for reco in rec.covers_rel_ids:
                total += reco.net_perimum

            rec.premium = total

    @api.multi
    @api.onchange("Company","product_pol")
    def onchange_num_covers_rel_ids(self):
        ids=self.env['insurance.product.coverage'].search([('product_id', '=',self.product_pol.id)])
       # print(ids)
        res=[]
        for rec in ids:
            res.append((0, 0, {
                            "name": rec.Name,
                            "sum_insure": rec.defaultvalue,
                            "check":rec.readonly,
                           # "rate": rec.product_id.name_cover_ids.covers_rel_ids.rate,
                            "net_perimum": rec.readonly and rec.defaultvalue
                        }))
        self.covers_rel_ids = res




    @api.onchange('Company')
    def settest(self):
        self.test = self.proposal_policy.test

    @api.onchange('Company')
    def setgroup(self):
        self.group = self.proposal_policy.group

    # car_proposal_test = fields.One2many('vehicle.object.opp', 'proposal_car_opp', compute=get_car_proposal)
    # person_proposal_test = fields.One2many('person.object.opp', 'proposal_person_opp', compute=get_person_proposal)
    # cargo_proposal_test = fields.One2many('cargo.object.opp', 'proposal_cargo_opp', compute=get_cargo_proposal)
    # group_proposal = fields.One2many('group.group.opp', 'proposal_group_opp', string='group proposal', readonly=True)

    @api.multi
    @api.depends('Company')
    def get_car_proposal(self):
        result = []
        for car in self.proposal_policy.objectvehicle:
            result.append((0, 0, {
                'Man': car.Man, ' model': car.model, 'motor_cc': car.motor_cc, "year_of_made": car.year_of_made
            }))

        self.car_proposal_test = result

    @api.multi
    @api.depends('Company')
    def get_person_proposal(self):
        result = []
        # import pdb;
        # pdb.set_trace()test check for other is it working or not
        for person in self.proposal_policy.objectperson:
            result.append((0, 0, {
                'name': person.name, 'DOB': person.DOB, 'job': person.job
            }))

        self.person_proposal_test = result

    @api.multi
    @api.depends('Company')
    def get_cargo_proposal(self):
        result = []
        for cargo in self.proposal_policy.objectcargo:
            result.append((0, 0, {
                'From': cargo.From, 'To': cargo.To, 'cargo_type': cargo.cargo_type, "weight": cargo.weight
            }))

        self.cargo_proposal_test = result

    select=fields.Many2one('policy.broker')
    car_proposal_test = fields.One2many('vehicle.object', 'proposal_car', compute=get_car_proposal)
    person_proposal_test = fields.One2many('person.object', 'proposal_person',compute=get_person_proposal )
    cargo_proposal_test = fields.One2many('cargo.object', 'proposal_cargo', compute=get_cargo_proposal)
    group_proposal = fields.One2many('group.group', 'proposal_group', string='group proposal', readonly=True)

    @api.multi
    def select_proposal(self):
        # self.proposal_policy.test1 = True
        self.proposal_policy.prop_id = self.id

    @api.onchange('Company')
    def person(self):
        ids = self.env['person.object'].search([('id', 'in',
                                                 self.proposal_policy.objectperson.ids)]).ids  # can you please let me know what are redcord the return this sarch....

        print("**********************************")
        print(ids)

        self.person_proposal = [(6, 0, ids)]

    @api.onchange('Company')
    def cargo(self):
        ids = self.env['cargo.object'].search([('id', 'in',
                                                self.proposal_policy.objectcargo.ids)]).ids  # can you please let me know what are redcord the return this sarch....


        self.cargo_proposal = [(6, 0, ids)]

    @api.onchange('Company')
    def showgroup(self):
        ids = self.env['group.group'].search([('id', 'in',
                                               self.proposal_policy.objectgroup.ids)]).ids
        self.group_proposal = [(6, 0, ids)]

    @api.onchange('Company')
    def showgroup(self):
        ids = self.env['group.group'].search([('id', 'in',
                                               self.proposal_policy.objectvehicle.ids)]).ids
        self.car_proposal = [(6, 0, ids)]



