import cherrypy
from app import app

def run_server(app,hostname,port=5000):
  cherrypy.tree.graft(app, '/')
  cherrypy.config.update({
        'engine.autoreload_on': True,
        'log.screen': True,
        'server.socket_port': port,
        'server.socket_host': hostname
    })
  cherrypy.engine.start()
  cherrypy.engine.block()

if __name__ == "__main__":
  run_server(app=app,hostname='0.0.0.0')