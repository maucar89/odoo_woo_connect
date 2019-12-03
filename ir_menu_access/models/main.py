# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
# You should have received a copy of the License along with this program.
#################################################################################

from openerp import http
from openerp.addons.web.controllers.main import Home, ensure_db
from openerp.addons.web.controllers import main
from openerp.http import request
import os
import sys
import jinja2
import werkzeug.utils
import werkzeug.wrappers
import json

if hasattr(sys, 'frozen'):
    # When running on compiled windows binary, we don't have access to package loader.
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'views'))
    loader = jinja2.FileSystemLoader(path)
else:
    loader = jinja2.PackageLoader('openerp.addons.web', "views")

env = jinja2.Environment(loader=loader, autoescape=True)
env.filters["json"] = json.dumps
#----------------------------------------------------------
# OpenERP Web web Controllers
#----------------------------------------------------------
class Home(Home):

    @http.route('/web', type='http', auth="none")
    def web_client(self, s_action=None, **kw):
        ensure_db()
        if not request.session.uid:
            return werkzeug.utils.redirect('/web/login', 303)
        if kw.get('redirect'):
            return werkzeug.utils.redirect(kw.get('redirect'), 303)

        request.uid = request.session.uid
        context = request.env['ir.http'].webclient_rendering_context()
        request.env['ir.ui.menu'].clear_caches()
        menu_data = request.env['ir.ui.menu'].load_menus(request.debug)

        return request.render('web.webclient_bootstrap', qcontext=context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: