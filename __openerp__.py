# -*- coding: utf-8 -*-
{
    'name': "Product info lines for stores",
    'author': "Simbioz, Yury Stasovsky",
    'license': 'LGPL-3',
    'website' : "https://qarea.us",
    'category': 'Custom integration',
    'version': '1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product'],
#    'depends': ['sale', 'purchase', 'mrp', 'sce'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        #'security/groups.xml',
       # 'wizard/wiz_view.xml',
        'views/partner.xml',
        #'views/menu.xml',
    ],
    'installable': True,
}
