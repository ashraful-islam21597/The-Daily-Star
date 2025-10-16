from odoo import models, fields

class CountryDivisions(models.Model):
    _inherit = 'res.country.state'
    _description = 'Divisions'

    bangla_name = fields.Char(string="Bangla Name")

class CountryDistricts(models.Model):
    _name = 'country.district'
    _description = 'Districts'

    name = fields.Char(string="Name")
    bangla_name = fields.Char(string="Bangla Name")
    division_id = fields.Many2one('res.country.state', string='Division')