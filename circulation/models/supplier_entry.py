from odoo import models, fields

class SupplierEntry(models.Model):
    _name = 'supplier.entry'
    _description = 'Supplier Information'

    code = fields.Char(string="Code", readonly=True, copy=False, default='New')
    supplier_name = fields.Char(string='Supplier Name', required=True)
    short_name = fields.Char(string='Short Name')
    supplier_nid = fields.Char(string='Supplier NID')
    product_service_description = fields.Text(string='Product/Service Description')
    trade_license_no = fields.Char(string='Trade License No.')
    incorporate_certificate_no = fields.Char(string='Incorporate Certificate No.')
    supplier_type = fields.Selection([
        ('individual', 'Individual'),
        ('company', 'Company'),
        ('agency', 'Agency'),
        ('others', 'Others'),
    ], string='Supplier Type', required=True)
    business_category = fields.Selection([
        ('product', 'Product'),
        ('service', 'Service'),
        ('both', 'Both'),
    ], string='Business Category')
    location = fields.Char(string='Location')

    def create(self, vals):
        if not vals.get('code'):
            vals['code'] = self.env['ir.sequence'].next_by_code('supplier.entry.seq') or 'NEW'
        return super(SupplierEntry, self).create(vals)
