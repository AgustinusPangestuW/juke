# -*- coding: utf-8 -*-
{
    'name': "juke_mobile_service",

    'summary': "Juke Mobile Service - Test",

    'description': """
Long description of module's purpose
    """,

    'author': "Agustinus Pangestu Wijaya",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['mail', 'product', 'account'],

    # always loaded
    'data': [
        'datas/groups.xml',

        'security/ir.model.access.csv',

        'views/mobile_service_brand.xml',
        'views/mobile_service_model.xml',
        'views/mobile_service_complaint_type.xml',
        'views/mobile_service_complaint_template.xml',
        'views/mobile_service_terms_and_conditions.xml',
        'views/inherit_product_template.xml',
        'views/mobile_service_service_request.xml',
        'wizards/mobile_service_wizard.xml',
        'views/menuitems.xml',

        'reports/invoice_report.xml',

        'datas/mobile_service_brand.xml',
        'datas/mobile_service_model.xml',
        'datas/complaint_type.xml',
        'datas/complaint_template.xml',
        'datas/mobile_service_terms_and_conditions.xml',
        'datas/product_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

