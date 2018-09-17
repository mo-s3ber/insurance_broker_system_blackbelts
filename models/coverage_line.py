from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class Covers(models.Model):
    _name='coverage.line'

    _rec_name='proposal_id'

    covers_crm=fields.Many2one('crm.lead','covers opp')
    proposal_id=fields.Many2one('proposal.opp.bb','proposal id')
    risk_id_covers=fields.Many2one('risks.opp','Risk id')
    risk_desc=fields.Char('')
    # Company = fields.Many2one('res.partner', domain="[('insurer_type','=',1)]", string="Insurer")
    # product_pol = fields.Many2one('insurance.product', domain="[('insurer','=',Company)]", string="Product")
    insurer = fields.Many2one(related='proposal_id.Company')
    product = fields.Many2one(related='proposal_id.product_pol',domain="[('insurer','=',insurer)]")
    covers=fields.Many2one('insurance.product.coverage',domain="[('product_id','=',product)]")
    sum_insured=fields.Float('SI')
    rate=fields.Float('Rate')
    net_premium=fields.Float('Net Premium')
    check=fields.Boolean(related='covers.readonly')

    @api.onchange('proposal_id')
    def onchange_proposal_id(self):
        if self.covers_crm :
            return {'domain':{'proposal_id': [('id','in',self.covers_crm.proposal_opp.ids)]}}

    @api.onchange('risk_id_covers')
    def onchange_risk_id(self):
        if self.covers_crm:
            return {'domain': {'risk_id_covers': [('id', 'in', self.covers_crm.objectrisks.ids)]}}

    @api.onchange('covers')
    def onchange_covers(self):
            if self.covers:
               self.sum_insured=self.covers.defaultvalue

    @api.onchange('rate')
    def compute_premium(self):
        if self.covers:
               self.net_premium=(self.sum_insured*self.rate)/100



    @api.onchange('risk_id_covers')
    def onchange_risc_desc(self):
        if self.risk_id_covers:
            self.risk_desc=self.risk_id_covers.risk_desc


