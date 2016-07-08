#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 Adrián López Tejedor <adrianlzt@gmail.com>
#
# Distributed under terms of the GNU GPLv3 license.

"""
Coge tokens de pushbullet y se los pasa a la aplicacion del usuario
"""

from bottle import Bottle, request, static_file, run
from jinja2 import Template,Environment,FileSystemLoader
import sys
import os

import logging
logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)


bottle = Bottle()
br = None

def render_template(template_name, **context):
    logger.info(sys._getframe().f_code.co_name)

    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})

    jinja_env = Environment(
            loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
            extensions=extensions,
            )
    jinja_env.globals.update(globals)

    return jinja_env.get_template(template_name).render(context)

@bottle.route('/auth_complete')
def auth_complete():
    """
    Pagina donde cargaremos un javascript que leera el token y lo registrara
    """
    logger.info(sys._getframe().f_code.co_name)

    app_url = request.params.get("app")
    try:
        body = render_template('auth.html', **locals())
    except Exception as e:
        logger.error("Excepcion renderizando auth.html: %s", e)
        return "Error rendering auth.html"

    return body

if __name__ == "__main__":
    bottle.run(host='localhost', port=8080)
