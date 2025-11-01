import re

from odoo import models, fields,api
from odoo.exceptions import ValidationError


class TransportEntry(models.Model):
    _name = 'transport.info'
    _description = 'Transport Entry'
    _rec_name = 'display_name'

    code = fields.Char(string="Code", readonly=True, copy=False, default='New')
    transport_name = fields.Char(string='Transport Name', required=True)
    bangla_name = fields.Char(string='Bangla Name')

    display_name = fields.Char(string='Display Name', compute='_compute_display_name', store=True)

    @api.depends('code', 'transport_name')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.transport_name}[{rec.code}]" if rec.code and rec.transport_name else (
                        rec.transport_name or rec.code)

    @api.model
    def name_get(self):
        result = []
        for rec in self:
            name = f"{rec.transport_name}[{rec.code}]" if rec.code else rec.transport_name
            result.append((rec.id, name))
        return result

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
