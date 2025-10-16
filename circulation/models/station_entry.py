from odoo import models, fields

class StationEntry(models.Model):
    _name = 'station.entry'
    _description = 'Station Entry'

    code = fields.Char(string='Code', readonly=True)
    station_name = fields.Char(string='Station Name', required=True)
    bangla_name = fields.Char(string='Bangla Name')
    division_id = fields.Many2one('res.country.state', string='Division',domain="[('country_id.code', '=', 'BD')]")
    division_bangla = fields.Char(string='Division Bangla')
    district = fields.Many2one('country.district',string='District')
    district_bangla = fields.Char(string='District Bangla',related='district.bangla_name',store=True)
    country_id = fields.Many2one('res.country',string='Country',default=lambda self: self.env.ref('base.bd'))

    def create(self, vals):
        if not vals.get('code'):
            vals['code'] = self.env['ir.sequence'].next_by_code('station.entry') or 'NEW'
        return super(StationEntry, self).create(vals)
