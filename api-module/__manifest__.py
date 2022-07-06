{
    'name': 'Odoo PDF',
    'sumary': 'Bottling Experts: Custom Quotation and Invoice Qweb PDF Reports',
    'description': """
        odoo PDF customize the PDF report of Quotation and Invoice
    """,
    'author': 'Odoo PS',
    'category': 'Sales',
    'version': '15.0.1.0.0',
    'depends': ['sale', 'web'],
    'license': 'OPL-1',
    'data': [
        'views/view_base_automation_inherit.xml'
    ],
    'external_dependencies': {
        'python': ['xmltodict'],
    }
}
