from odoo import models, fields, api
from odoo.exceptions import ValidationError


class New_Risks(models.Model):
    _name="new.risks"
    _rec_name="risk"


    @api.multi
    def Show_covers(self):
        form_view = self.env.ref('insurance_broker_system_blackbelts.my_view_for_covers_edit')
        form_view2 = self.env.ref('insurance_broker_system_blackbelts.my_view_for_covers_edit_cover')

        return {
            'name': ('poroposal '),
            'view_type': 'form',
            'view_mode': 'tree',
            'views': [(form_view.id, 'tree'),(form_view2.id,'form')],
            'res_model': 'name.covers',
            'target': 'current',
            'type': 'ir.actions.act_window',
            'context': {"default_proposal__risk_id.covers_rel_ids": self.id},
            'flags': {'tree': {'action_buttons': True}, 'form': {'action_buttons': True},
                                  'action_buttons': True},
            'domain': [('id', 'in', self.name_cover_risk_ids.ids)]


        }

    @api.multi
    def get_covers(self):
        self.proposal__risk_id.risk_proposal_select_id = self.id

    @api.multi
    def _compute_risk_description(self):
        for rec in self:
            if rec.test == "person":
                rec.risk_description = str(rec.name) + "  " + str(rec.DOB)+ "  " + str(rec.job)

            if rec.test == "vehicle":
                rec.risk_description = str(rec.car_tybe) + "  " +str(rec.motor_cc) + "  " +str(rec.year_of_made)+ "  " + str(rec.model)+ "  " + str(rec.Man)

            if rec.test == "cargo":
                rec.risk_description = str(rec.From)+ "  " + str(rec.To) + "  " + str(rec.cargo_type) + "  " + str(rec.weight)
            if rec.test == "location":
                rec.risk_description = str(rec.group_name)  + "  " + str(rec.count)

    policy_risk_id = fields.Many2one("policy.broker")


    risk = fields.Char("Risk ID")
    risk_description = fields.Char("Risk Description" ,compute="_compute_risk_description")
    proposal__risk_id = fields.Many2one('proposal.bb')
    name_cover_risk_ids=fields.One2many("name.covers", "risk_brokerd_id")
    test = fields.Char(related="policy_risk_id.test")


    #group car
    car_tybe = fields.Char(string="Vehicle Type")
    motor_cc = fields.Char("Motor cc")
    year_of_made = fields.Date("Year of Made")
    model = fields.Char("Motor Model")
    Man = fields.Char(string='Vehicle Brande')



    #group person
    name = fields.Char('Name')
    DOB = fields.Date('Date Of Birth')
    job = fields.Char('Job Tiltle')




    #group cargo
    From = fields.Char('From')
    To = fields.Char('To')
    cargo_type = fields.Char("Type Of Cargo")
    weight = fields.Float('Weight')


    #gropu group
    group_name=fields.Char('Name')

    count=fields.Char('Group Count')

    file = fields.Binary(string='Group Details File')
