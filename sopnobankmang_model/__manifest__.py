# -*- coding: utf-8 -*-
{
    'name': "sopnobankmangModel",

    'summary': """
        A Simple Bank Mange in Rangpur""",

    'description': """
        Shopno Choa Consumers CO-Operative Limited
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/customer.xml',
        'views/customer_loan.xml',
        'views/daily_payment.xml',
        'views/paid_loan.xml',
        'views/customer_status.xml',
        'views/customer_savings.xml',
        'views/customer_savings_stutas.xml',
        'views/paid_savings.xml',
        'views/daily_savings.xml',
        'views/daily_earn_loan.xml',
        'views/daily_cash_drawer.xml',
        'views/daily_earn_cash.xml',
        'views/annual_income.xml',
        'views/dashboard_view.xml',
        'views/templates.xml',
        'data/sequence.xml',


        'reports/cus_reg.xml',
        'reports/cus_loan.xml',
        'reports/paid_loan.xml',
        'reports/cus_payment.xml',
        'reports/daily_earn.xml',
        'reports/customer_savings.xml',
        'reports/withdraw_savings.xml',
        'reports/daily_earn_savings.xml',
        'reports/daily_earn_cash.xml',
        'reports/final_cash_drawer.xml',
        'reports/anual_income_report.xml',
        'reports/customer_payment_report.xml',

        'wizards/customer_payment_wizard_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}