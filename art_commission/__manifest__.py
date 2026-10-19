{
    'name': 'Art Commission',
    'version': '19.0.1.0.0',
    'summary': "Manage an illustrator's commission requests",
    'author': 'Niboo',
    'category': 'Services',
    'license': 'LGPL-3',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/art_commission_type_views.xml',
        'views/art_commission_option_views.xml',
        'views/art_commission_menus.xml',
    ],
    'application': True,
}