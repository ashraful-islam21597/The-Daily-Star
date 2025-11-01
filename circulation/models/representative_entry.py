import re

from odoo import models, fields,api,_
from odoo.exceptions import ValidationError


class RepresentativeEntry(models.Model):
    _name = 'representative.entry'
    _description = 'Representative Entry'
    _rec_name = 'code'

    code = fields.Char(string="Code", readonly=True, copy=False, default='New')
    name = fields.Char(string="Name")
    bangla_name = fields.Char(string="Bangla Name")
    partner_id = fields.Many2one('res.partner',string="Contact Person")
    contact_no = fields.Char(string="Contact No")
    district_id = fields.Many2one('res.country.district',string='District')
    police_station = fields.Many2one('res.country.police.station',string='Police Station')
    division_id = fields.Many2one('res.country.state', related="district_id.division_id", store=True)
    address = fields.Text(string="Address")
    nid_no = fields.Char(string="NID")
    photo_attachment = fields.Binary(string="Photo", attachment=True)
    bin_attachment = fields.Binary(string="BIN", attachment=True)
    chq_leaf_attachment = fields.Binary(string="Chq Leaf", attachment=True)
    tin_attachment = fields.Binary(string="TIN", attachment=True)
    trade_license_attachment = fields.Binary(string="Trade License", attachment=True)
    nid_attachment = fields.Binary(string="NID", attachment=True)
    nid_attachment_ref1 = fields.Binary(string="NID(Ref 1)", attachment=True)
    nid_attachment_ref2 = fields.Binary(string="NID(Ref 2)", attachment=True)
    others_attachment = fields.Binary(string="Others", attachment=True)

    @api.constrains('nid_no')
    def _check_nid_digits(self):
        for rec in self:
            if rec.nid_no and not re.match(r'^\d+$', rec.nid_no):
                raise ValidationError(_("NID must contain only numbers."))

    def create(self, vals):
        if not vals.get('code'):
            vals['code'] = self.env['ir.sequence'].next_by_code('representative.entry.seq') or 'NEW'
        return super(RepresentativeEntry, self).create(vals)