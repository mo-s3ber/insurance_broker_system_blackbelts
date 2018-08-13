from odoo import models, fields, api
from odoo.exceptions import  ValidationError


class crm_leads(models.Model):
    _inherit = "crm.lead"

    planned_revenue = fields.Float('Expected Premium in Company Currency', track_visibility='always')
    c_type = fields.Many2one('res.currency', string='Expected Premium in Currency')
    ammount = fields.Float(string='Ammount')
    user_id = fields.Many2one('res.users', string='Lead Operator', index=True, track_visibility='onchange',
                              default=lambda self: self.env.user )
    create_uid = fields.Many2one('res.users', string='Lead Generator')
    policy_number = fields.Char( string='Policy Number')

    insurance_type = fields.Selection([('life', 'Life'),
                                       ('p&c', 'p&c'),
                                       ('health', 'Health'), ],
                                      'Insurance Type', track_visibility='onchange')
    ins_type = fields.Selection([('Individual', 'Individual'),
                                 ('Group', 'Group'),],
                                'insured type', track_visibility='onchange')
    policy_dur = fields.Selection([('Every 6 Months', 'Every 6 Months'),
                                   ('Every Year', 'Every Year'), ],
                                  'Policy Duration', track_visibility='onchange')
    LOB = fields.Many2one('insurance.line.business', string='Line of business', domain="[('insurance_type','=',insurance_type)]")

    oppor_type = fields.Char(
        string='Opportunity type',
        compute='_changeopp',
        store=False,
        compute_sudo=True,
    )

    #pol=fields.Many2one(related='Policy_type.insured_type' , string='insured type')
    test=fields.Char('')
    group=fields.Boolean('Groups')
    individual = fields.Boolean('Item by Item')
    test1=fields.Boolean(readonly=True)

    objectcar = fields.One2many('vehicle.object.opp', 'object_vehicle_crm', string='car')#where you are using this fiedl ? in xml
    objectperson = fields.One2many('person.object.opp', 'object_person_crm', string='person')
    objectcargo = fields.One2many('cargo.object.opp', 'object_cargo_crm', string='cargo')
    objectgroup = fields.One2many('group.group.opp', 'object_group_crm', string='Group')

    proposal_opp=fields.One2many('proposal.opp.bb','proposal_crm',string='Final proposla')

    selected_proposal=fields.One2many('proposal.opp.bb','select_crm' ,compute='proposalselected')
    prop_id=fields.Integer('',readonly=True)
    my_notes=fields.Text('Under writting')

    covers=fields.One2many(related='selected_proposal.proposals_covers')

    policy_opp=fields.Many2one('policy.broker')








    def proposalselected(self):
        print('5555555')
        ids = self.env['proposal.opp.bb'].search([('id', '=',self.prop_id)]).ids
        self.selected_proposal = [(6, 0, ids)]

    # objectcar_selected = fields.Many2one('car.object', string='car')
    # objectperson_selected = fields.Many2one('person.object', string='Person')
    # objectcargo_selected = fields.Many2one('cargo.object', string='cargo')
    # objectgroup_selected = fields.Many2one('group.group', string='Group')





    # @api.onchange('user_id')
    # def get_car_proposal_crm(self):
    #     for lead in self:
    #         proposal_ids = []
    #         for car in self.objectcar:
    #             if car.btn1:
    #                 proposal_ids = proposal_ids+car.proposal_car.ids
    #         lead.prop_car = [(6,0, proposal_ids)]



    # @api.multi
    # def button_action(self):
    #     return {
    #         'type': 'ir.actions.act_url',
    #         'url': 'http://167.99.243.240/moodle/login/index.php?username=%{0}&password=Admin%40123&Submit=Login' .format(self.env.user.name),
    #         'target': 'self',
    #         'res_id': self.id,
    #     }



    #prop_car=fields.One2many(related='objectcar')
    # prop_person = fields.One2many(related='objectperson_selected.proposal_person')
    # prop_cargo = fields.One2many(related='objectcargo_selected.proposal_cargo')
    # prop_group = fields.One2many(related='objectgroup_selected.proposal_group')

    @api.multi
    def create_policy(self):
        form_view = self.env.ref('insurance_broker_blackbelts.my_view_for_policy_form_kmlo1')
        if self.policy_number:
            return {
                'name': ('Policy'),
                'view_type': 'form',
                'view_mode': 'form',
                'views': [(form_view.id, 'form')],
                'res_model': 'policy.broker',
                'target': 'current',
                'type': 'ir.actions.act_window',
                'context': {},
            }
        else:
            raise ValidationError(
                ('You Must Enter the Policy Number .'))

                # , 'default_objectperson':records_person ,'default_objectcar':records_car},

        # # write tree and form view id here.
        # proposal_car_tree  form_proposal
        # view = self.env.ref('crm__black_belts.proposal_car_tree')
        # form_view = self.env.ref('insurance_broker_blackbelts.my_view_for_policy_form_kmlo1')
        # print(self.objectperson.ids)
        #
        # #self.policy_opp.test=self.test
        # return {
        #     'name': 'Policy',
        #     'type': 'ir.actions.act_window',
        #     'view_type': 'form',
        #     'view_mode': ' form',
        #     'views': [(form_view.id, 'form')],
        #     'res_model': 'policy.broker',
        #     'target': 'current',
        #     'context': {'default_policy_opp':self,'default_insurance_type': self.insurance_type, 'default_line_of_bussines': self.LOB.id,
        #                 'default_ins_type': self.ins_type
        #         , 'default_objectvehicle': self.objectcar.ids, 'default_objectperson':  self.objectperson.ids},
        #
        #
        #
        #
        # }





    @api.onchange('LOB')
    def _compute_comment(self):
        for record in self:
            record.test = record.LOB.object
            print (record.test)






    #@api.onchange('user_id')
    #def onchange_user_id(self):
    #   if self.user_id and self.env.uid != 1 :
    #        return {'domain':{'user_id': [('id','in',[self.env.uid,1])]}}


    @api.onchange('user_id', 'create_uid')
    def _changeopp(self):
        for record in self:
            if record.create_uid:
                if record.create_uid == record.user_id:
                    record['oppor_type'] = 'Own'

                else:
                    record['oppor_type'] = 'Network'
            else :
                record.create_uid=self.env.uid





    @api.onchange('ammount', 'c_type')
    def _change(self):
        if self.c_type.id:
            self.planned_revenue = self.ammount / self.c_type.rate




class crm_leads_currency(models.Model):
    _inherit = 'res.currency'
    # currency_type=fields.One2many('crm.lead','currency_type ',string='currency')
    c = fields.One2many('crm.lead', 'c_type', string='currency')

class partner(models.Model):
    _inherit='res.partner'
    # name=fields.Char(readonly=True,required=False)
    DOB=fields.Date('Date of Birth')
    martiual_status = fields.Selection([('Single', 'Single'),
                                        ('Married', 'Married'),],
                                       'marital status', track_visibility='onchange')
    last_time_insure = fields.Date('last_time_insure')

    C_industry = fields.Selection([('Software', 'Software'),
                                   ('Engineering', 'Engineering'), ],
                                  'Industry', track_visibility='onchange')
    holding=fields.Many2one('res.partner',string='Holding Company')












