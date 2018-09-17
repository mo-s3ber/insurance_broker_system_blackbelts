from odoo import models, fields, api
from odoo.exceptions import ValidationError


class New_Risks(models.Model):
    _name="new.risks"
    _rec_name="risk"

    # @api.multi
    # def generate_covers(self):
    #     return True
    #
    #
    # #
    # # @api.multi
    # # def get_covers(self):
    # #     self.proposal__risk_id.risk_proposal_select_id = self.id

    @api.multi
    @api.onchange('risk')
    def _compute_risk_descriptionn(self):
        for rec in self:

            if rec.test == "person":
                rec.risk_description = (str(rec.name) if rec.name  else " "+"_") + "  " + (str(rec.DOB) if rec.DOB else " "+"_")+ "  " + (str(rec.job) if rec.job  else " "+"_")

            if rec.test == "vehicle":
                rec.risk_description = (str(rec.car_tybe)  if rec.car_tybe  else " "+"_") + "  " +(str(rec.motor_cc)  if rec.motor_cc else " "+"_") + "  " +(str(rec.year_of_made)  if rec.year_of_made  else " "+"_")+ "  " + (str(rec.model)  if rec.model  else " "+"_") + "  " + (str(rec.Man)  if rec.Man  else" "+"_")

            if rec.test == "cargo":
                rec.risk_description = (str(rec.From)  if rec.From else " "+"_")+ "  " + (str(rec.To)  if rec.To else " "+"_") + "  " + (str(rec.cargo_type)  if rec.cargo_type  else " "+"_") + "  " + (str(rec.weight)  if rec.weight else " "+"_")
            if rec.test == "location":
                rec.risk_description = (str(rec.group_name)  if rec.group_name  else" "+"_")  + "  " + (str(rec.count)  if rec.count  else " "+"_")


    policy_risk_id = fields.Many2one("policy.broker")

<<<<<<< HEAD
    risk = fields.Char("Risk ID")
    risk_description = fields.Char("Risk Description" ,compute="_compute_risk_description")
=======
    risk = fields.Char("Risk ID" ,required=True)
<<<<<<< HEAD
    risk_description = fields.Text("Risk Description")
=======
    risk_description = fields.Text("Risk Description",compute="_compute_risk_descriptionn",store=True)
>>>>>>> 60da00b23ccb9222cf1ccd4ce21144593f9a4117
>>>>>>> 04c237543c50c9224795509ef5da60e0ab3603fc
    proposal__risk_id = fields.Many2one('proposal.bb')
    name_cover_risk_ids=fields.One2many("name.covers", "risk_brokerd_id")
    test = fields.Char(related="policy_risk_id.check_item")



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


    # @api.model
    # def create(self,vals):
    #     self.env["policy.broker"].create({"new_risk_ids.risk":self.risk,"new_risk_ids.risk_description":self.risk_description})
    #
    #
    #     return super(New_Risks, self).create(vals)

