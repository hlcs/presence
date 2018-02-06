'''
Created on 09/giu/2015

@author: spax
Edited on 2017/12/05 by Alivin70
'''

import asyncio
import importlib
import os

import django


import django.core.handlers.wsgi
import tornado.httpserver
from tornado.ioloop import IOLoop
from tornado.platform.asyncio import AsyncIOMainLoop
import tornado.wsgi


from tornado.options import define, options



"""definisce le opzioni globali di settaggio da presence.settings"""
define("settings", default="presence.settings", help="Django settings module")

"""definisce la porta di settaggio"""
define("port", default=8000, help="linsten port")

""" Funzione di setup delle porte 
    @param settings: settaggi/impostazioni delle porte """
def setup_gates(settings):
    gate_setup_func = getattr(settings, 'GATE_SETUP_FUNCTION', None)
    if gate_setup_func:
        module_name, function_name = gate_setup_func.rsplit(".", 1)
        the_function = getattr(importlib.import_module(module_name), function_name)
        the_function()

"""tornado mischiato alla parte wsgi di django"""
def setup_server(settings):
    """spax pigro"""
    import gatecontrol.handlers as handlers
    """tornado wrappa la parte WSGI di django nella propria"""
    wsgi_app = tornado.wsgi.WSGIContainer(django.core.handlers.wsgi.WSGIHandler())
    """definizione della web app tornado composta da..."""
    tornado_app = tornado.web.Application([
            """... tornado che gestisce i file statici"""
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path':'static'}),
            """... gatecontrol che gestisce i socket""" 
            (r"/socket", handlers.SocketHandler),
            """... gatecontrol che gestisce i token"""
            (r"/token", handlers.TokenHandler),
            """... ogni altra URL la gestisce django"""
            ('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app))], 
        debug=settings.DEBUG)
    """avvio web server completo"""
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(options.port, '0.0.0.0')

""" Dovrebbe settare i task periodicamente"""
def setup_periodical_tasks(settings):
    import gatecontrol.monitor as monitor
    callback_time = getattr(settings, 'PERIODIC_CALLBACK_TIME', 100)
    scheduler = tornado.ioloop.PeriodicCallback(monitor.StateMonitor().notify_changes, callback_time, io_loop=IOLoop.instance())
    scheduler.start()

""" Avvio del server """
def runserver():
    tornado.options.parse_command_line()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", options.settings)
    django.setup() #setup di django
    from django.conf import settings
    setup_gates(settings) #installa le porte
    AsyncIOMainLoop().install()
    setup_server(settings)
    setup_periodical_tasks(settings)
    asyncio.get_event_loop().run_forever()


""" MAIN esegue la runserver """
if __name__ == '__main__':
    runserver()
