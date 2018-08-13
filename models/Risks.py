from odoo import models, fields, api


class car_object(models.Model):
    _name='vehicle.object'
    object_vehicle = fields.Many2one("policy.broker", string='Vehicle')


    # car# ok now
    motor_cc = fields.Char("Motor cc")
    year_of_made = fields.Date("Year of Made")
    model = fields.Char("Motor Model")
    Man = fields.Char('Manifactor')
    proposal_car = fields.Many2one('proposal.bb', string='proposal')
    # covers_car=fields.One2many(related='proposal_car.product_pol.TOB')




    # proposal_car = fields.One2many('proposal.bb', 'car_proposal', string='proposal')
    # btn1=fields.Boolean('')
    #
    # # @api.multi
    # # def create_proposal_car(self):
    # #     # write tree and form view id here.
    # #     # proposal_car_tree  form_proposal
    # #     #view = self.env.ref('crm__black_belts.proposal_car_tree')
    # #     form_view = self.env.ref('crm__black_belts.form_proposal')
    # #     return {
    # #         'name': 'Proposals',
    # #         'type': 'ir.actions.act_window',
    # #         'view_type': 'form',
    # #         'view_mode': ' form',
    # #         'views': [(form_view.id, 'form')],
    # #         'res_model': 'proposalcar.bb',
    # #         'target': 'new',
    # #         'context': {'default_proposal_id_car': self.id},
    # #         'flags': {'tree': {'action_buttons': True},'form': {'action_buttons': True}, 'action_buttons':True},
    # #
    # #
    # #     }
    #
    #
    #
    #
    # @api.multi
    # def get_proposal_car(self):
    #     self.object_car.objectcar_selected = self.id








#ok test test
# please give 10 mins nice but still i cant add anew proposal a want to appeqred in same view
#need check on browser how its works
#add new button in form view and set display string as save


#what about res_model sorry that now ok what that error which eror ? i can not edit in list view  hi


#here hi yes hello can you please explain explain what ?that one 2many where ? 't udnetstand the model of related field is person_object hi
#got it? no
#what your question




class person_object(models.Model):
    _name='person.object'
    object_person = fields.Many2one("policy.broker", string='person')


    # person#
    name = fields.Char('Name')
    DOB = fields.Date('Date Of Birth')
    job = fields.Char('Job Tiltle')
    btn1 = fields.Boolean('')
    proposal_person = fields.Many2one('proposal.bb', string='proposal')
    # covers_person = fields.One2many(related='proposal_person.product_pol.TOB')
    # # ..........#

    # proposal_person = fields.One2many('proposalperson.bb', 'proposal_id_person', string='proposal')
    # # ok why not working might be limitation of odoo using onchange can't set parenet field can use depends no try to use button will refresh the page
    # #ok i will try
    #
    # @api.onchange('btn1')
    # def cc(self):
    #     self.object_person.test1='ali'
    #     print(self.object_person.test1)
    #
    # @api.multi
    # def get_proposal_person(self):
    #     self.object_person.objectperson_selected=self.id
    #    # print(self.object_person.objectperson_selected)


class cargo_object(models.Model):
    _name='cargo.object'
    object_cargo = fields.Many2one("policy.broker", string='cargo')


    From = fields.Char('From')
    To = fields.Char('To')
    cargo_type = fields.Char("Type Of Cargo")
    weight = fields.Float('Weight')
    #
    proposal_cargo = fields.Many2one('proposal.bb', string='proposal')
    # covers_cargo = fields.One2many(related='proposal_cargo.product_pol.TOB')
    # # ......#

    # proposal_cargo = fields.One2many('proposalcargo.bb', 'proposal_id_cargo', string='proposal')

    # def get_proposal_cargo(self):
    #     self.object_carg.objectcargo_selected = self.id


class group(models.Model):
    _name='group.group'


    object_group = fields.Many2one("policy.broker", string='cargo')


    group_name=fields.Char('Name')

    count=fields.Char('Group Count')

    file = fields.Binary(string='Group Details File')

    proposal_group = fields.Many2one('proposal.bb', string='proposal')
    # covers_group = fields.One2many(related='proposal_group.product_pol.TOB')


    # proposal_group = fields.One2many('proposalgroup.bb', 'proposal_id_group', string='proposal')
    #
    # def get_proposal_group(self):
    #     self.object_group.objectgroup_selected = self.id





