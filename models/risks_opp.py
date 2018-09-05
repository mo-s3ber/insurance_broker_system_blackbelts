from odoo import models, fields, api


class Risks_object(models.Model):
    _name='risks.opp'
    risks_crm = fields.Many2one("crm.lead",string='Risks')
    risk_id=fields.Char('Risk Id')
    risk_desc=fields.Char('Risk Description',compute='set_risk_desc',store=True)
    type_risk=fields.Char(related='risks_crm.test')
    proposal_risks_opp = fields.Many2one('proposal.opp.bb', string='proposal')
    risks_covers=fields.One2many('name.covers','risks',force_save=True)




    motor_cc = fields.Char("Motor cc")
    year_of_made = fields.Date("Year of Made")
    model = fields.Char("Motor Model")
    Man = fields.Char('Manifactor')

    name = fields.Char('Name')
    DOB = fields.Date('Date Of Birth')
    job = fields.Char('Job Tiltle')

    From = fields.Char('From')
    To = fields.Char('To')
    cargo_type = fields.Char("Type Of Cargo")
    weight = fields.Float('Weight')

    @api.one
    @api.depends('type_risk')
    def set_risk_desc(self):
        print('entered')
        if self.risk_id:
            self.risk=''
            if self.type_risk=='person':
                self.risk_desc=str(self.name)+str(self.DOB)+str(self.job)

            if self.type_risk == 'vechile':
                self.risk_desc = str(self.motor_cc) + str(self.year_of_made) + str(self.model)+str(self.Man)

            if self.type_risk == 'cargo':
                self.risk_desc = str(self.From) + str(self.To) + str(self.cargo_type) + str(self.weight)

    @api.multi
    def get_covers_risk(self):
        self.proposal_risks_opp.risk_cover_selected = self.id







