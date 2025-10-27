import re

from odoo import models, fields,api
from odoo.exceptions import ValidationError


class TransportEntry(models.Model):
    _name = 'transport.info'
    _description = 'Transport Entry'
    _rec_name = 'code'

    code = fields.Char(string="Code", readonly=True, copy=False, default='New')
    transport_name = fields.Char(string='Transport Name', required=True)
    bangla_name = fields.Char(string='Bangla Name')

    @api.constrains('bangla_name')
    def _check_bangla_name(self):
        bangla_pattern = re.compile(r'^[\u0980-\u09FF\s]+$')
        for record in self:
            if record.bangla_name and not bangla_pattern.match(record.bangla_name):
                raise ValidationError("This field must contains only Bengali letters.")

    def create(self, vals):
        if not vals.get('code'):
            vals['code'] = self.env['ir.sequence'].next_by_code('transport.info.seq') or 'NEW'
        return super(TransportEntry, self).create(vals)
