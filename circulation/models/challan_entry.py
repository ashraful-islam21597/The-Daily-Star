import re

from odoo import models, fields,api
from odoo.exceptions import ValidationError


class ChallanEntry(models.Model):
    _name = 'challan.entry'
    _description = 'Challan Entry'
    _rec_name = 'code'

    code = fields.Char(string="Code", readonly=True, copy=False, default='New')
    date = fields.Date(string="Date",default=fields.date.today())
    agent_category = fields.Selection([
        ('non_returnable_agent', 'Non Returnable Agent'),
        ('returnable_agent', 'Returnable Agent')
    ], string="Agent Category")

    agent_id = fields.Many2one('agent.info', string="Agent")
    distribution_route_id = fields.Many2one('distribution.route','Distribution Route',related="agent_id.dist_route",store=True)
    distribution_route_bangla_name = fields.Char(related='distribution_route_id.bangla_name', string="ডিস্ট্রিবিউশন রুট")
    transport_id = fields.Many2one('transport.info', 'Transport Agency',
                                   related="agent_id.transport_agency",store=True)
    transport_bangla_name = fields.Char(related='transport_id.bangla_name',string="ট্রান্সপোর্ট এজেন্সী")

    agent_bangla_name = fields.Char('এজেন্ট',related="agent_id.bangla_name")
    agent_code_search = fields.Char('Agency Code')
    agent_address = fields.Text(related='agent_id.present_address', store=True)
    station_id = fields.Many2one("station.entry", domain="[('agent_id', '=', agent_id)]")
    station_bangla_name = fields.Char(related='station_id.bangla_name', store=True)
    sale_type = fields.Selection([
        ('general_sale','General Sale'),
        ('corporate_sale','Corporate Sale'),
        ('representative_sale','Representative Sale')
    ],string='Type',default='general_sale')

    general_sale_ids = fields.One2many('general.sale.lines','challan_entry_id')
    corporate_sale_ids = fields.One2many('corporate.sale.lines','challan_entry_id')
    representative_sale_ids = fields.One2many('representative.sale.lines','challan_entry_id')
    agent_code = fields.Char(related='agent_id.code', store=True)
    station_code = fields.Char(related='station_id.code', store=True)
    total_general_sale_qty = fields.Float(string="General Sale Qty", compute="_compute_general_sales_summary")
    total_general_discount = fields.Float(string="General Sale Discount", compute="_compute_general_sales_summary")

    @api.depends('general_sale_ids.sale_qty', 'general_sale_ids.discount')
    def _compute_general_sales_summary(self):
        for rec in self:
            rec.total_general_sale_qty = sum(line.sale_qty for line in rec.general_sale_ids)
            rec.total_general_discount = sum(line.discount for line in rec.general_sale_ids)

    def to_bangla_date(self, date_str):
        bangla_digits = {'0': '০', '1': '১', '2': '২', '3': '৩', '4': '৪', '5': '৫', '6': '৬', '7': '৭', '8': '৮',
                         '9': '৯'}
        return ''.join(bangla_digits.get(c, c) for c in date_str)

    # @api.onchange('agent_category')
    # def _onchange_agent_category(self):
    #     if self.agent_category:
    #         if self.agent_category == 'returnable_agent':
    #             self.agent_id = False
    #             domain = [('ret_category', '!=', 'none')]
    #             return {'domain': {'agent_id': domain}}
    #         else:
    #             self.agent_id = False
    #             domain = [('ret_category', '=', 'none')]
    #             return {'domain': {'agent_id': domain}}

    def action_print_report(self):
        rpt_template = 'circulation.label_challan_view'
        return self.env.ref(rpt_template).with_context(rpt_name=f'LABEL').report_action(self)




    @api.model
    def create(self, vals):
        if isinstance(vals, list):
            for v in vals:
                if not v.get('code'):
                    v['code'] = self.env['ir.sequence'].next_by_code('challan.entry.seq') or 'NEW'
        else:
            if not vals.get('code'):
                vals['code'] = self.env['ir.sequence'].next_by_code('challan.entry.seq') or 'NEW'

        return super(ChallanEntry, self).create(vals)


class GeneralSaleLines(models.Model):
    _name = 'general.sale.lines'
    _description = 'General Sales'
    _rec_name = 'code'

    code = fields.Char(string="Code", readonly=True, copy=False, default='New')
    challan_entry_id = fields.Many2one('challan.entry')
    rate = fields.Float(string="Rate")
    sale_qty = fields.Integer(string="Sales Quantity")
    specimen_qty = fields.Integer(string="Specimen Quantity")
    discount = fields.Float(string="Discount")
    extra_discount = fields.Float(string="Extra Discount")
    packet_number = fields.Integer(string="Packet No")

    @api.model
    def create(self, vals):
        if isinstance(vals, list):
            for v in vals:
                if not v.get('code'):
                    v['code'] = self.env['ir.sequence'].next_by_code('general.sale.seq') or 'NEW'
        else:
            if not vals.get('code'):
                vals['code'] = self.env['ir.sequence'].next_by_code('general.sale.seq') or 'NEW'

        return super(GeneralSaleLines, self).create(vals)

class CorporateSaleLines(models.Model):
    _name = 'corporate.sale.lines'
    _description = 'Corporate Sales'
    _rec_name = 'code'

    code = fields.Char(string="Code", readonly=True, copy=False, default='New')
    client_name = fields.Char(string="Client")
    bangla_name = fields.Char(string="ক্লায়েন্টের নাম")
    project = fields.Char(string="Project")
    challan_entry_id = fields.Many2one('challan.entry')
    rate = fields.Float(string="Rate")
    sale_qty = fields.Integer(string="Sales Quantity")
    specimen_qty = fields.Integer(string="Specimen Quantity")
    discount = fields.Float(string="Discount")
    extra_discount = fields.Float(string="Extra Discount")
    packet_number = fields.Integer(string="Packet No")

    @api.model
    def create(self, vals):
        if isinstance(vals, list):
            for v in vals:
                if not v.get('code'):
                    v['code'] = self.env['ir.sequence'].next_by_code('corporate.sale.seq') or 'NEW'
        else:
            if not vals.get('code'):
                vals['code'] = self.env['ir.sequence'].next_by_code('corporate.sale.seq') or 'NEW'

        return super(CorporateSaleLines, self).create(vals)

    @api.constrains('bangla_name')
    def _check_bangla_name(self):
        bangla_pattern = re.compile(r'^[\u0980-\u09FF\s]+$')
        for rec in self:
            if rec.bangla_name and not bangla_pattern.match(rec.bangla_name):
                raise ValidationError("Bangla Name must contain only Bengali letters.")

class RepresentativeSaleLines(models.Model):
    _name = 'representative.sale.lines'
    _description = 'Representative Sales'
    _rec_name = 'code'

    code = fields.Char(string="Code", readonly=True, copy=False, default='New')
    representative_id = fields.Many2one("representative.entry",string="Representative")
    bangla_name = fields.Char(related="representative_id.bangla_name",string="রিপ্রেসেন্টেটিভের নাম")
    challan_entry_id = fields.Many2one('challan.entry')
    sale_qty = fields.Integer(string="Sales Quantity")
    packet_number = fields.Integer(string="Packet No")

    @api.model
    def create(self, vals):
        if isinstance(vals, list):
            for v in vals:
                if not v.get('code'):
                    v['code'] = self.env['ir.sequence'].next_by_code('representative.sale.seq') or 'NEW'
        else:
            if not vals.get('code'):
                vals['code'] = self.env['ir.sequence'].next_by_code('representative.sale.seq') or 'NEW'

        return super(RepresentativeSaleLines, self).create(vals)

    @api.constrains('bangla_name')
    def _check_bangla_name(self):
        bangla_pattern = re.compile(r'^[\u0980-\u09FF\s]+$')
        for rec in self:
            if rec.bangla_name and not bangla_pattern.match(rec.bangla_name):
                raise ValidationError("Bangla Name must contain only Bengali letters.")