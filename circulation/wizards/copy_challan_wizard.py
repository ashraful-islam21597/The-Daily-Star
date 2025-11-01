from odoo import models, fields,api,_
from odoo.exceptions import ValidationError


class CopyChallanEntryWizard(models.TransientModel):
    _name = 'copy.challan.entry.wizard'
    _description = 'Challan Entry Wizard'

    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To",default=fields.date.today())

    def action_copy_challan(self):
            self.ensure_one()

            if self.date_to <= self.date_from:
                raise ValidationError(_("‘Date To’ must be greater than ‘Date From’."))

            challan_entries = self.env['challan.entry'].search([
                ('date', '=', self.date_from)
            ])

            if not challan_entries:
                raise ValidationError(_("No challan entries found in this date range."))

            for record in challan_entries:
                # Copy the challan entry
                new_record = record.copy({
                    'date': self.date_to,
                })

                # Manually copy One2many lines if needed
                if record.corporate_sale_ids:
                    new_lines = []
                    for line in record.corporate_sale_ids:
                        new_lines.append((0, 0, line.copy_data()[0]))
                    new_record.write({'corporate_sale_ids': new_lines})

                if record.general_sale_ids:
                    new_lines = []
                    for line in record.general_sale_ids:
                        new_lines.append((0, 0, line.copy_data()[0]))
                    new_record.write({'general_sale_ids': new_lines})

                if record.representative_sale_ids:
                    new_lines = []
                    for line in record.representative_sale_ids:
                        new_lines.append((0, 0, line.copy_data()[0]))
                    new_record.write({'representative_sale_ids': new_lines})

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _("Challan Copy Complete"),
                    'message': _("All challan entries from %s to %s have been copied to %s.") %
                               (self.date_from, self.date_to, self.date_to),
                    'sticky': False,
                }
            }


class UpdateChallanEntryWizard(models.TransientModel):
    _name = 'update.challan.entry.wizard'
    _description = 'Challan Entry Wizard'

    date = fields.Date(string="Date")
    agent_id = fields.Many2one('agent.info', string="Agent")
    station_id = fields.Many2one("station.entry", domain="[('agent_id', '=', agent_id)]")
    challan_entry_id = fields.Many2one("challan.entry", domain="[('station_id', '=', station_id),('date', '=', date)]")

    #general sale
    general_sale_rate = fields.Float(string="Rate")
    general_sale_qty = fields.Integer(string="Sales Quantity")
    general_sale_specimen_qty = fields.Integer(string="Specimen Quantity")
    general_sale_discount = fields.Float(string="Discount")
    general_sale_extra_discount = fields.Float(string="Extra Discount")
    general_sale_packet_number = fields.Integer(string="Packet No")

    # corporate sale
    client_name = fields.Char(string="Client")
    client_bangla_name = fields.Char(string="ক্লায়েন্টের নাম")
    project = fields.Char(string="Project")
    corporate_sale_rate = fields.Float(string="Rate")
    corporate_sale_qty = fields.Integer(string="Sales Quantity")
    corporate_sale_specimen_qty = fields.Integer(string="Specimen Quantity")
    corporate_sale_discount = fields.Float(string="Discount")
    corporate_sale_extra_discount = fields.Float(string="Extra Discount")
    corporate_sale_packet_number = fields.Integer(string="Packet No")

    #representative sale
    representative_id = fields.Many2one("representative.entry", string="Representative")
    representative_bangla_name = fields.Char(related="representative_id.bangla_name", string="রিপ্রেসেন্টেটিভের নাম")
    representative_sale_qty = fields.Integer(string="Sales Quantity")
    representative_sale_packet_number = fields.Integer(string="Packet No")

    @api.onchange('station_id')
    def _onchange_station_id(self):
        if self.station_id:
            challan_entry_id = self.env['challan.entry'].search([('date','=',self.date),('station_id','=',self.station_id.id)])
            self.challan_entry_id = challan_entry_id

            for gs in challan_entry_id.general_sale_ids:
                self.general_sale_rate = gs.rate
                self.general_sale_qty = gs.sale_qty
                self.general_sale_specimen_qty = gs.specimen_qty
                self.general_sale_discount = gs.discount
                self.general_sale_extra_discount = gs.extra_discount
                self.general_sale_packet_number = gs.packet_number

            for cs in challan_entry_id.corporate_sale_ids:
                self.client_name = cs.client_name
                self.client_bangla_name = cs.bangla_name
                self.project = cs.project
                self.corporate_sale_rate = cs.rate
                self.corporate_sale_qty = cs.sale_qty
                self.corporate_sale_specimen_qty = cs.specimen_qty
                self.corporate_sale_discount = cs.discount
                self.corporate_sale_extra_discount = cs.extra_discount
                self.corporate_sale_packet_number = cs.packet_number

            for rs in challan_entry_id.representative_sale_ids:
                self.representative_id = rs.representative_id
                self.representative_bangla_name = rs.bangla_name
                self.representative_sale_qty = rs.sale_qty
                self.representative_sale_packet_number = rs.packet_number




    def action_update_challan(self):
            for gs in self.challan_entry_id.general_sale_ids:
                vals={}
                if gs.sale_qty != self.general_sale_qty:
                    vals['sale_qty'] = self.general_sale_qty
                if gs.rate != self.general_sale_rate:
                    vals['rate'] = self.general_sale_rate
                if gs.specimen_qty != self.general_sale_specimen_qty:
                    vals['specimen_qty'] = self.general_sale_specimen_qty
                if gs.discount != self.general_sale_discount:
                    vals['specimen_qty'] = self.general_sale_specimen_qty
                if gs.extra_discount != self.general_sale_extra_discount:
                    vals['extra_discount'] = self.general_sale_extra_discount
                if gs.packet_number != self.general_sale_packet_number:
                    vals['packet_number'] = self.general_sale_packet_number
                gs.update(vals)

            for cs in self.challan_entry_id.corporate_sale_ids:
                vals={}
                if cs.sale_qty != self.general_sale_qty:
                    vals['sale_qty'] = self.general_sale_qty
                if cs.client_name != self.client_name:
                    vals['client_name'] = self.client_name
                if cs.bangla_name != self.client_bangla_name:
                    vals['bangla_name'] = self.client_bangla_name
                if cs.project != self.project:
                    vals['project'] = self.project
                if cs.rate != self.corporate_sale_rate:
                    vals['rate'] = self.corporate_sale_rate
                if cs.specimen_qty != self.corporate_sale_specimen_qty:
                    vals['specimen_qty'] = self.corporate_sale_specimen_qty
                if cs.discount != self.corporate_sale_discount:
                    vals['specimen_qty'] = self.corporate_sale_specimen_qty
                if cs.extra_discount != self.corporate_sale_extra_discount:
                    vals['extra_discount'] = self.corporate_sale_extra_discount
                if cs.packet_number != self.corporate_sale_packet_number:
                    vals['packet_number'] = self.corporate_sale_packet_number
                cs.update(vals)

            for rs in self.challan_entry_id.representative_sale_ids:
                vals = {}

                if rs.sale_qty != self.general_sale_qty:
                    vals['sale_qty'] = self.general_sale_qty
                if rs.representative_id != self.representative_id:
                    vals['representative_id'] = self.representative_id
                if rs.bangla_name != self.representative_bangla_name:
                    vals['bangla_name'] = self.representative_bangla_name
                if rs.sale_qty != self.representative_sale_qty:
                    vals['sale_qty'] = self.representative_sale_qty
                if rs.packet_number != self.representative_sale_packet_number:
                    vals['packet_number'] = self.representative_sale_packet_number
                rs.update(vals)



            reset_vals = {
                'date': self.date,
                'agent_id': self.agent_id.id,
                'challan_entry_id': False,
                'station_id': False,
                'general_sale_rate': False,
                'general_sale_qty': False,
                'general_sale_specimen_qty': False,
                'general_sale_discount': False,
                'general_sale_extra_discount': False,
                'general_sale_packet_number': False,

                # corporate sale
                'client_name': False,
                'client_bangla_name': False,
                'project': False,
                'corporate_sale_rate': False,
                'corporate_sale_qty': False,
                'corporate_sale_specimen_qty': False,
                'corporate_sale_discount': False,
                'corporate_sale_extra_discount': False,
                'corporate_sale_packet_number': False,

                # representative sale
                'representative_id': False,
                'representative_sale_qty': False,
                'representative_sale_packet_number': False,
            }
            self.write(reset_vals)

            return {
                'type': 'ir.actions.act_window',
                'res_model': self._name,
                'view_mode': 'form',
                'res_id': self.id,
                'target': 'new',
            }