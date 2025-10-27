from odoo import models, fields,api,_

class CountryDivisions(models.Model):
    _inherit = 'res.country.state'
    _description = 'Divisions'
    _rec_name = 'name'

    code = fields.Char(string="Division Code", readonly=True, copy=False, default='New')
    bangla_name = fields.Char(string="Bangla Name")

    @api.model
    def init(self):
        updates = {
            'Dhaka': 'ঢাকা',
            'Chattogram': 'চট্টগ্রাম',
            'Khulna': 'খুলনা',
            'Rajshahi': 'রাজশাহী',
            'Barishal': 'বরিশাল',
            'Rangpur': 'রংপুর',
            'Sylhet': 'সিলেট',
            'Mymensingh': 'ময়মনসিংহ',
        }
        for name, bangla in updates.items():
            state = self.search([('name', '=', name), ('country_id.code', '=', 'BD')], limit=1)
            if state:
                state.bangla_name = bangla

class CountryDistricts(models.Model):
    _name = 'res.country.district'
    _description = 'Districts'
    _rec_name = 'name'

    code = fields.Char(string="District Code", readonly=True, copy=False, default='New')
    name = fields.Char(string="Name")
    bangla_name = fields.Char(string="Bangla Name")
    division_id = fields.Many2one('res.country.state', string='Division')

    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code('res.country.district.seq') or 'New'
        return super(CountryDistricts, self).create(vals)