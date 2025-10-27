from odoo import models, fields,api,_

class DistributionRouteEntry(models.Model):
    _name = 'distribution.route'
    _description = 'Distribution Route Entry'
    _rec_name = 'code'

    code = fields.Char(string="Code", readonly=True, copy=False, default='New')
    name = fields.Char(string="Name")
    bangla_name = fields.Char(string="Bangla Name")

    def create(self, vals):
        if not vals.get('code'):
            vals['code'] = self.env['ir.sequence'].next_by_code('distribution.route.seq') or 'NEW'
        return super(DistributionRouteEntry, self).create(vals)

