# -*- coding: utf-8 -*-
{
    'name': "Bangladesh VAT Mushak 6.3",

    'summary': """
        Implements Bangladesh VAT Mushak 6.3 Tax Challan with auto-sequence numbering.""",

    'description': """
        Implements the Bangladesh VAT Mushak 6.3 (Tax Challan) for Odoo.
        Features:
        - BIN field on Company and Partner
        - Mushak 6.3 challan number with auto-sequence (M63/YYYY/XXXXX)
        - One-click Generate Challan Number button on customer invoices
        - Print VAT 6.3 challan PDF report (English or Bangla)
        - Supplementary Duty per invoice line (editable on invoice form)
    """,

    'author': "SM Ashraf",
    'website': "http://www.eagle_erp.com",

    'category': 'Accounting/Localizations',
    'version': '18.0.1.1.0',

    'depends': ['base', 'account'],
    'license': 'LGPL-3',

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'views/views.xml',
        'reports/report.xml',
        'reports/vat_63_challan.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
