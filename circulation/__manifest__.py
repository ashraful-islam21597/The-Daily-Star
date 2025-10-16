
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
        'data/divisions.xml',
        'data/districts.xml',
        'views/menu.xml',
        'views/station_entry.xml',
    ],
}

