{
    "name": "Telegram Base",
    "summary": "Generic Telegram API connector",
    "version": "18.0.1.0.0",
    "category": "Social",
    "author": "Anmol Garg, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/social",
    "license": "LGPL-3",
    "depends": [
        "base",
        "mail",
        "mail_gateway_telegram",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/mail_gateway_views.xml",
    ],
    "installable": True,
    "application": False,
}
