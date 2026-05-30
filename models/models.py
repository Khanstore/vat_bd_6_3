# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResCompanyBin(models.Model):
    _inherit = "res.company"
    bin = fields.Char("BIN")


class ResPartnerBin(models.Model):
    _inherit = 'res.partner'
    bin = fields.Char("BIN")


class AccountMove(models.Model):
    _inherit = 'account.move'

    time_invoice = fields.Datetime(
        string="Invoice Time",
        default=lambda self: fields.Datetime.now(),
    )
    vat_challan_no = fields.Char(
        string="Mushak 6.3 No.",
        readonly=True,
        copy=False,
        index=True,
    )
    challan_print_lang = fields.Selection([
        ('en_US', 'English'),
        ('bn_IN', 'বাংলা (Bangla)'),
    ], string="Challan Print Language", default='en_US', copy=False)

    def action_generate_vat_challan_no(self):
        """Generate Mushak 6.3 sequence, stamp time_invoice to now, lock it."""
        for record in self:
            if record.vat_challan_no:
                raise UserError(
                    _("A Mushak 6.3 number (%s) is already assigned to this invoice.")
                    % record.vat_challan_no
                )
            if record.move_type not in ('out_invoice', 'out_refund'):
                raise UserError(_("Mushak 6.3 challan is only applicable to customer invoices."))
            seq = self.env['ir.sequence'].with_company(record.company_id).next_by_code('vat.mushak.6.3') or '/'
            record.vat_challan_no = seq
            record.time_invoice = fields.Datetime.now()

    def action_print_vat_challan_wizard(self):
        """Open language selection wizard before printing."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Print VAT 6.3 Challan'),
            'res_model': 'vat.challan.print.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_invoice_id': self.id,
                'default_lang': self.challan_print_lang or 'en_US',
            },
        }


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    invoice_line_supplementary_tax = fields.Monetary(
        string='Supplementary Duty',
        currency_field='company_currency_id',
        default=0.0,
    )


class VatChallanPrintWizard(models.TransientModel):
    _name = 'vat.challan.print.wizard'
    _description = 'VAT 6.3 Challan Language Selection'

    invoice_id = fields.Many2one('account.move', string='Invoice', required=True)
    lang = fields.Selection([
        ('en_US', 'English'),
        ('bn_IN', 'বাংলা (Bangla)'),
    ], string='Print Language', default='en_US', required=True)

    def action_print(self):
        self.ensure_one()
        # Write the chosen language onto the invoice so it survives the
        # HTTP round-trip that Odoo makes when it fetches the PDF.
        # The QWeb template reads o.challan_print_lang directly.
        self.invoice_id.challan_print_lang = self.lang
        report = self.env.ref('vat_bd_6_3.account_vat_63_challan')
        return report.report_action(self.invoice_id, config=False)
