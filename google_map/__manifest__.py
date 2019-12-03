# -*- coding: utf-8 -*-
######################################################################################################
#
# Copyright (C) B.H.C. sprl - All Rights Reserved, http://www.bhc.be
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# This code is subject to the BHC License Agreement
# Please see the License.txt file for more information
# All other rights reserved
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied,
# including but not limited to the implied warranties
# of merchantability and/or fitness for a particular purpose
######################################################################################################
{
    'name': 'Google Maps',
    'version': '1.0',
    'category': 'Extra Tools',
    'description': """This module adds a Map button on the partner’s form in order to open its address directly in the Google Maps view""",
    'author': 'BHC & OpenERP',
    'website': 'www.bhc.be',
    'depends': ['base'],
    'init_xml': [],
    'images': ['static/description/banner.png','images/google_map.png','images/map.png','images/earth.png'],
    'data': [
            'views/google_map_view.xml',
            ],
    'installable': True,
    'auto_install': False,
    'license': 'AGPL-3',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: