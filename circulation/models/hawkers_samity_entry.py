from odoo import models, fields,api,_

class PoliceStation(models.Model):
    _name = '.station'
    _description = 'Police Stations'
    _rec_name = 'name'

    code = fields.Char(string="PS Code", readonly=True, copy=False, default='New')
    name = fields.Char(string='Station Name', required=True)
    bangla_name = fields.Char(string="Bangla Name")
    division_id = fields.Many2one('res.country.state', string='Division', domain="[('country_id.code', '=', 'BD')]")
    district_id = fields.Many2one('res.country.district', string='District', domain="[('division_id', '=',division_id)]")

    def create(self, vals):
        if not vals.get('code'):
            vals['code'] = self.env['ir.sequence'].next_by_code('res.country.police.station.entry.seq') or 'NEW'
        return super(PoliceStation, self).create(vals)