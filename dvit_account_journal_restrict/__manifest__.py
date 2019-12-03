# -*- coding: utf-8 -*-

{
    'name': "Journal Restrictions",
    'summary': """Restrict users to certain journals""",
    'description': """Restrict users to certain journals.""",
    'author': "DVIT.ME",
    'website': "http://www.dvit.me",
    'license': 'AGPL-3',
    'category': 'account',
    'version': '10.0.2.0',
    'depends': ['account'],
    'data': [
        'views/users.xml',
        'security/security.xml',
    ],
    "images": [
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
}
