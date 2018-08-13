from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Policy_Info(models.Model):
    _name ="insurance.line.business"
    _rec_name = 'line_of_business'

    insurance_type = fields.Selection([('life', 'Life'),
                          ('p&c', 'P&C'),
                          ('health', 'Health'), ],
                         'Insurance Type', track_visibility='onchange', required=True)
    line_of_business = fields.Char(string='Line of Business', required=True)
    object= fields.Selection([('person', 'Person'),
                          ('vehicle', 'Vehicle'),
                          ('cargo', 'Cargo'),
                          ('location', 'Location'),],
                         'Object', track_visibility='onchange', required=True)
    policy_desc = fields.Char(string='Description')


class Product(models.Model):
    _name='insurance.product'
    _rec_name = 'product_name'

    product_name=fields.Char('Product Name',required=True)
    insurer=fields.Many2one('res.partner', string="Insurer",domain="[('insurer_type','=',1)]")
    line_of_bus=fields.Many2one('insurance.line.business','Line of Business')
    income_account=fields.Many2one('account.account','Income Account')
    expense_account = fields.Many2one('account.account','Expense Account')
    coverage=fields.One2many('insurance.product.coverage','product_id',string='Coverage')
    brokerage=fields.One2many('insurance.product.brokerage','product_id',string='Brokerage')
    commision_id = fields.Many2one("commision.setup")

class coverage(models.Model):
    _name='insurance.product.coverage'

    Name=fields.Char('Name')
    defaultvalue=fields.Char('Default Value')
    required=fields.Boolean('Required')
    limit=fields.Integer('Limit')
    readonly=fields.Boolean('Read Only')
    product_id=fields.Many2one('insurance.product')
    lop_id=fields.Many2one('insurance.line.business',string='Line of Business')


class Brokerage(models.Model):
    _name='insurance.product.brokerage'

    datefrom=fields.Date('Date from')
    dateto=fields.Date('Date to')
    perorfixed=fields.Boolean('% or Fixed')
    basic_commission = fields.Float('Basic Commission')
    complementary_commission = fields.Float('Complementary Commission')
    fixed_commission = fields.Float('Fixed Commission')
    product_id = fields.Many2one('insurance.product')

    @api.constrains('datefrom')
    def _constrain_date(self):
        for record in self:
            if record.dateto < record.datefrom:
                raise ValidationError('Error! Date to Should be After Date from')


class inhertResPartner(models.Model):
    _inherit = 'res.partner'

    insurer_type=fields.Boolean('Insurer')
