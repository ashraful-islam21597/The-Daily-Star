from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class AgentEntry(models.Model):
    _name = 'agent.entry'
    _description = 'Agent Entry'
    _rec_name = 'code'

    code = fields.Char(string="Code", readonly=True, copy=False, default='New')
    date = fields.Date(string='Date', default=fields.Date.context_today)
    name = fields.Char(string='Agent Name', required=True)
    bangla_name = fields.Char(string='Bangla Name')
    name_as_nid = fields.Char(string='Name As NID')
    nid_no = fields.Char(string='NID No.')
    present_address = fields.Text(string='Present Address')
    permanent_address = fields.Text(string='Permanent Address')
    division_id = fields.Many2one('res.country.state', string='Division', domain="[('country_id.code','=','BD')]")
    district_id = fields.Many2one('res.country.district', string='District', domain="[('division_id','=',division_id)]")
    ex_discount = fields.Float(string='Ex. Discount (%)')
    security_money = fields.Float(string='Security Money')
    ret_category = fields.Selection([
        ('daily', 'Daily'),
        ('monthly', 'Monthly'),
        ('none', 'None'),
    ], string='Ret. Category')
    billing_cycle = fields.Selection([
        ('daily', 'Daily'),
        ('monthly', 'Monthly'),
    ], string='Billing Cycle')

    credit_limit_period = fields.Integer(string='Credit Limit (Period)')
    credit_limit_amt = fields.Float(string='Credit Limit (Amount)')
    discount = fields.Float(string='Discount (%)')
    dist_route = fields.Many2one('distribution.route', string='Dist. Route')
    transport_agency = fields.Many2one('transport.info', string='Transport Agency')
    mobile_no = fields.Char(string='Mobile No.')
    alt_mobile_no = fields.Char(string='Alternate Mobile No.')
    bkash_no = fields.Char(string='bKash No.')
    account_no = fields.Char(string='Account No.')
    bank_name = fields.Char(string='Bank Name')
    branch_name = fields.Char(string='Branch Name')
    routing_no = fields.Char(string='Routing No.')
    email = fields.Char(string='Email')

    # References
    reference1_name = fields.Char(string='Reference (1)')
    reference1_address = fields.Text(string='Ref. (1) Address')
    reference1_phone = fields.Char(string='Ref. (1) Phone')
    reference1_nid = fields.Char(string='Ref. (1) NID')

    reference2_name = fields.Char(string='Reference (2)')
    reference2_address = fields.Text(string='Ref. (2) Address')
    reference2_phone = fields.Char(string='Ref. (2) Phone')
    reference2_nid = fields.Char(string='Ref. (2) NID')

    photo_attachment = fields.Binary(string='Photo', attachment=True)

    # Business IDs
    bin_no = fields.Char(string='BIN')
    bin_attachment = fields.Binary(string="BIN", attachment=True)
    trade_license = fields.Char(string='Trade License No.')
    trade_license_attachment = fields.Binary(string="Trade License", attachment=True)
    cheque_leaf = fields.Char(string='Cheque Leaf')
    chq_leaf_attachment = fields.Binary(string="Chq Leaf", attachment=True)
    nid_attachment = fields.Binary(string='NID')
    tin_no = fields.Char(string='TIN')
    tin_attachment = fields.Binary(string="TIN", attachment=True)
    nid_attachment_ref2 = fields.Binary(string="NID(Ref 2)", attachment=True)
    nid_attachment_ref1 = fields.Binary(string="NID(Ref 2)", attachment=True)
    others_attachment = fields.Binary(string="Others", attachment=True)

    @api.constrains('bangla_name')
    def _check_bangla_name(self):
        bangla_pattern = re.compile(r'^[\u0980-\u09FF\s]+$')
        for rec in self:
            if rec.bangla_name and not bangla_pattern.match(rec.bangla_name):
                raise ValidationError("⚠️ Bangla Name must contain only Bengali letters.")

    def create(self, vals):
        if not vals.get('code'):
            vals['code'] = self.env['ir.sequence'].next_by_code('supplier.entry.seq') or 'NEW'
        return super(AgentEntry, self).create(vals)
