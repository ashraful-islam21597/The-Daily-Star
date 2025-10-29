from odoo import models, fields,api

class StationEntry(models.Model):
    _name = 'station.entry'
    _description = 'Station Entry'
    _rec_name = 'code'

    code = fields.Char(string="Code", readonly=True, copy=False, default='New')
    name = fields.Char(string='Station Name', required=True)
    bangla_name = fields.Char(string='Bangla Name')
    division_id = fields.Many2one('res.country.state', string='Division',domain="[('country_id.code', '=', 'BD')]")
    division_bangla = fields.Char(string='Division Bangla',related='division_id.bangla_name')
    district_id = fields.Many2one('res.country.district',string='District',domain="[('division_id', '=',division_id)]")
    district_bangla = fields.Char(string='District Bangla',related='district_id.bangla_name',store=True)
    country_id = fields.Many2one('res.country',string='Country',default=lambda self: self.env.ref('base.bd'))
    agent_id = fields.Many2one('agent.info',string='Agent', domain="[('district_id', '=', district_id)]")
    agent_bangla_name = fields.Char( related="agent_id.bangla_name")

    def create(self, vals):
        if not vals.get('code'):
            vals['code'] = self.env['ir.sequence'].next_by_code('station.entry.seq') or 'NEW'
        return super(StationEntry, self).create(vals)

    display_name = fields.Char(string='Display Name', compute='_compute_display_name', store=True)

    @api.depends('code', 'name')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"[{rec.code}] {rec.name}" if rec.code and rec.name else (
                    rec.name or rec.code)

    @api.model
    def name_get(self):
        result = []
        for rec in self:
            name = f"[{rec.code}] {rec.name}" if rec.code else rec.name
            result.append((rec.id, name))
        return result