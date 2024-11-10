# -*- coding: utf-8 -*-
{
    "name": "Vertical Hospital",
    "summary": "Este módulo  de gestionar pacientes y sus procedimientos",
    "description": """
    Este módulo de gestionar pacientes y sus procedimientos
    """,
    "author": "Asettec",
    "website": "https://youcompany.com/",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Medical",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "web", "mail"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/views.xml",
        "views/templates.xml",
        'views/settings_form_view.xml',
        'report/vertical_hospital_report_paciente.xml',
    ],
    'installable': True,
    'application': True,
    "assets": {
    },
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
}
