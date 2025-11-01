
{
    'name': "circulation",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','contacts'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/districts.xml',
        'views/menu.xml',
        'views/district_entry.xml',
        'views/division_entry.xml',
        'views/station_entry.xml',
        'views/distribution_route_entry.xml',
        'views/representative_entry.xml',
        'views/police_station_entry.xml',
        'views/supplier_entry.xml',
        'views/transport_entry.xml',
        'views/agent_entry.xml',
        'views/challan_entry.xml',
        'wizards/copy_challan_wizard.xml',
        'wizards/update_challan_wizard.xml',
        'reports/label/challan_entry_label_pdf.xml',
        # 'reports/reports_actions.xml',
    ],
    'assets': {
            'web.assets_backend': [
                'circulation/static/src/components/js/**/*.js',
                'circulation/static/src/components/xml/**/*.xml'
            ],
        },
}

