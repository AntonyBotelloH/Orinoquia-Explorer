import os
import sys

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_DIR)

# Agregar rutas de paquetes (incluyendo lib64 para extensiones binarias como Pillow)
sys.path.insert(0, '/home/bbingeni/virtualenv/enchilamebb/3.12/lib64/python3.12/site-packages')
sys.path.insert(0, '/home/bbingeni/virtualenv/enchilamebb/3.12/lib/python3.12/site-packages')
sys.path.insert(0, '/home/bbingeni/virtualenv/orinoquiaxp/3.12/lib64/python3.12/site-packages')
sys.path.insert(0, '/home/bbingeni/virtualenv/orinoquiaxp/3.12/lib/python3.12/site-packages')

os.chdir(PROJECT_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

try:
    from app.wsgi import application
except Exception as e:
    import traceback
    tb = traceback.format_exc()
    def application(environ, start_response):
        start_response('500 Internal Server Error', [('Content-Type', 'text/html; charset=utf-8')])
        html = f"""
        <html>
        <head><title>Error al Iniciar Orinoquia Explorer</title></head>
        <body style="font-family: monospace; padding: 25px; background: #fff5f5; color: #991b1b;">
            <h2>Error al iniciar la aplicacion Django (Orinoquia Explorer) en cPanel</h2>
            <pre style="background: white; padding: 15px; border: 1px solid #fecaca; border-radius: 8px; overflow-x: auto;">{tb}</pre>
        </body>
        </html>
        """
        return [html.encode('utf-8')]
