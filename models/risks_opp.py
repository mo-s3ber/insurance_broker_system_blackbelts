from odoo import models, fields, api


class Risks_object(models.Model):
    _name='risks.opp'

    _rec_name='risk_id'

    @api.one
    @api.depends('risks_crm')
    def _set_risk_desc(self):
                self.risk_desc = ''
                str_desc=''
                if self.type_risk == 'person':
                    str_desc = str(self.name) +'-'+ str(self.DOB) + '-'+str(self.job)

                if self.type_risk == 'vechile':
                    str_desc = str(self.motor_cc) + str(self.year_of_made) + str(self.model) + str(self.Man)

                if self.type_risk == 'cargo':
                    str_desc = str(self.From) + str(self.To) + str(self.cargo_type) + str(self.weight)

                strsplit=str_desc.split('-')
                for i in  range (len(strsplit)):
                    if strsplit[i]=='False':
                        strsplit[i]=''



                self.risk_desc='-'.join(strsplit)

    # @api.one
    # def _get_risk_desc(self):
    #     # self.risk_id = self.risk_desc





    risks_crm = fields.Many2one("crm.lead",string='Risks')
    risk_id=fields.Char('Risk Id')
    risk_desc=fields.Char('Risk Description',compute=_set_risk_desc,store=True)
    type_risk=fields.Char(related='risks_crm.test')
    proposal_risks_opp = fields.Many2one('proposal.opp.bb', string='proposal')
    risks_covers=fields.One2many('name.covers','risks',force_save=True)

    my_button = fields.Boolean('Label')






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


    @api.multi
    def saverecord(self):
        return True

    @api.multi
    def saverecord(self,vals):
        return super(Risks_object, self).create(vals)

    @api.multi
    def get_covers_risk(self):
        self.proposal_risks_opp.risk_cover_selected = self.id

    @api.multi
    def save(self,vals):
        form_view2 = self.env.ref('crm.crm_case_form_view_oppor')
        print (self._context)
        return {
            'name': (' Opp'),
            'view_type': 'form',
            'view_mode': ('form'),
            'views': [ (form_view2.id, 'form')],
            'res_model': 'crm.lead',
            'target': 'current',
            'type': 'ir.actions.act_window',
            'res_id':self.risks_crm.id ,
            # 'context': {"default_risks": self.id},
            # 'flags': {'tree': {'action_buttons': True}, 'form': {'action_buttons': True},
            #           'action_buttons': True},

        }
    # @api.depends('risk_id')
    # def _set_risk_desc(self):
    #         print('eslam function')
    #
    #         self.risk_desc = ''
    #         str_desc=''
    #         if self.type_risk == 'person':
    #             str_desc = str(self.name) +'-'+ str(self.DOB) + '-'+str(self.job)
    #
    #         if self.type_risk == 'vechile':
    #             str_desc = str(self.motor_cc) + str(self.year_of_made) + str(self.model) + str(self.Man)
    #
    #         if self.type_risk == 'cargo':
    #             str_desc = str(self.From) + str(self.To) + str(self.cargo_type) + str(self.weight)
    #
    #         strsplit=str_desc.split('-')
    #         for i in  range (len(strsplit)):
    #             if strsplit[i]=='False':
    #                 strsplit[i]=''
    #
    #
    #
    #         self.risk_desc='-'.join(strsplit)



    # @api.multi
    # @api.onchange('my_button')
    # def onchange_my_button(self):
    #     if self.my_button:
    #         form_view2 = self.env.ref('crm.crm_case_form_view_oppor')
    #         print (self._context)
    #         dict1 = {
    #             'name': (' Opp'),
    #             'view_type': 'form',
    #             'view_mode': ('form'),
    #             'views': [(form_view2.id, 'form')],
    #             'res_model': 'crm.lead',
    #             'target': 'current',
    #             'type': 'ir.actions.act_window',
    #             'res_id': self.risks_crm.id,
    #             # 'res_id': self.risks_crm.id,
    #             # 'context': {"default_risks": self.id},
    #             # 'flags': {'form': {'action_buttons': False},
    #             #           'action_buttons': False},
    #
    #         }
    #         return (dict1)

    # @api.multi
    # def cancel(self):
    #     form_view2 = self.env.ref('crm.crm_case_form_view_oppor')
    #     print (self._context)
    #     dict1= {
    #         'name': (' Opp'),
    #         'view_type': 'form',
    #         'view_mode': ('form'),
    #         'views': [(form_view2.id, 'form')],
    #         'res_model': 'crm.lead',
    #         'target': 'current',
    #         'type': 'ir.actions.act_window',
    #         'res_id': self.risks_crm.id,
    #         # 'res_id': self.risks_crm.id,
    #         # 'context': {"default_risks": self.id},
    #         'flags': { 'form': {'action_buttons': False},
    #                   'action_buttons': False},
    #
    #     }
    #     return (dict1)

    @api.multi
    def edit_risks(self, vals):
        form_view2 = self.env.ref('insurance_broker_system_blackbelts.Risks_form')
        print (self._context)
        return {
            'name': ('Risks'),
            'view_type': 'form',
            'view_mode': ('form'),
            'views': [(form_view2.id, 'form')],
            'res_model': 'risks.opp',
            'target': 'inline',
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            # 'context': {"default_risks": self.id},
            # 'flags': {'tree': {'action_buttons': True}, 'form': {'action_buttons': True},
            #           'action_buttons': True},

        }







    @api.multi
    def edit_covers_risk(self):
        form_view = self.env.ref('insurance_broker_system_blackbelts.tree_covers')
        form_view2 = self.env.ref('insurance_broker_system_blackbelts.my_view_for_covers_edit_cover')
        return {
            'name': (' Covers'),
            'view_type': 'form',
            'view_mode': ('tree','form'),
            'views': [(form_view.id, 'tree'), (form_view2.id, 'form')],
            'res_model': 'name.covers',
            'target': 'current',
            'type': 'ir.actions.act_window',
            'context': {"default_risks": self.id},
            # 'flags': {'tree': {'action_buttons': True}, 'form': {'action_buttons': True},
            #           'action_buttons': True},
            'domain': [('id', 'in', self.risks_covers.ids)]
        }







