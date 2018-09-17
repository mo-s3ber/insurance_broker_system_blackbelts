from odoo import api, fields, models

class Proposals(models.Model):
    _name='proposal.bb'
    _rec_name="Company"










    proposal_policy=fields.Many2one("policy.broker")
    Company = fields.Many2one('res.partner', domain="[('insurer_type','=',1)]", string="Insurer")
    product_pol = fields.Many2one('insurance.product',domain="[('insurer','=',Company)]", string="Product")
    premium = fields.Float('Premium', compute="compute_premiume")
    test=fields.Char(string='type')
    group = fields.Boolean('Groups')
    covers_rel_ids = fields.One2many("name.covers", "rel_policy_broker_id",compute="compute_covers")
    bool = fields.Boolean()
    new_proposal_test_ids = fields.One2many("new.risks", 'proposal__risk_id',readonly=True)
    risk_proposal_select_id = fields.Many2one("new.risks")
    select = fields.Many2one('policy.broker')

    @api.multi
    @api.onchange('Company')
    def get_carrrr_proposal(self):
        result = []
        for car in self.proposal_policy.new_risk_ids:
            result.append( car.id )

        self.new_proposal_test_ids = [(6,0, result)]

    @api.onchange('product_pol')
    def setcoversweee_person(self):
        print('i enter')
        if self.new_proposal_test_ids:
            print('xxx')
            for person in self.new_proposal_test_ids:
                res = []
                person.name_cover_risk_ids=False
                ids = self.env['insurance.product.coverage'].search(
                    [('product_id', '=', self.product_pol.id)])
                for rec in ids:
                    res.append((0, 0, {
                        "name": rec.Name,
                        "sum_insure": rec.defaultvalue,
                        "check": rec.readonly,
                        "net_perimum": rec.readonly and rec.defaultvalue
                    }))
                person.name_cover_risk_ids = res

    @api.one
    def compute_covers(self):
        print("old")
        for lead in self:
            covers_ids = []
            if lead.new_proposal_test_ids:
                for rec in lead.new_proposal_test_ids:
                    covers_ids = rec[0].name_cover_risk_ids.ids
                    for record in lead.risk_proposal_select_id:
                        covers_ids = record.name_cover_risk_ids.ids
            lead.covers_rel_ids = [(6, 0, covers_ids)]



    # @api.one
    # @api.depends("product_pol")
    # def compute_premiume(self):
    #     total=0.0
    #     for line in self.new_proposal_test_ids:
    #         print("iii")
    #         for rec in line.name_cover_risk_ids:
    #             total += rec.net_perimum
    #     self.premium=total







    # @api.onchange('Company')
    # def settest(self):
    #     self.test = self.proposal_policy.test
    #
    # @api.onchange('Company')
    # def setgroup(self):
    #     self.group = self.proposal_policy.group



    #
    # @api.multi
    # def select_proposal(self):
    #     # self.proposal_policy.test1 = True
    #     self.proposal_policy.prop_id = self.id

    @api.multi
    def create_covers(self):
        self.bool = True
        return True
