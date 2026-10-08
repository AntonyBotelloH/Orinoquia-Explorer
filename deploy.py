import os
import ssl
import ftplib
from pathlib import Path

# Configuración de Servidor FTP
HOST = '44.211.14.38'
PORT = 1257
USER = 'adso_user@bbingenieros.online'
PASS = '@c3lm8xxvGESTOR'

REMOTE_APP_ROOT = '/orinoquiaxp'
REMOTE_PUB_ROOT = '/public_html/orinoquiaxp'

BASE_DIR = Path(__file__).resolve().parent

# Carpetas y archivos a subir al core de la aplicación (/home/bbingeni/orinoquiaxp/)
CORE_DIRS = [
    'app',
    'usuarios',
    'experiencias',
    'turismo',
    'reservas',
    'aliados',
    'templates',
    'static',
    'media',
]

CORE_FILES = [
    ('manage.py', 'manage.py'),
    ('passenger_wsgi.py', 'passenger_wsgi.py'),
    ('requirements.txt', 'requirements.txt'),
    ('.env.production', '.env'),
    ('.htaccess', '.htaccess'),
]

def make_dirs(ftp, remote_dir):
    """Crea la estructura de carpetas remota si no existe."""
    parts = [p for p in remote_dir.replace('\\', '/').split('/') if p]
    current = ''
    for part in parts:
        current += '/' + part
        try:
            ftp.cwd(current)
        except Exception:
            try:
                ftp.mkd(current)
                ftp.cwd(current)
            except Exception as e:
                pass

def upload_file(ftp, local_path, remote_file_path):
    """Sube un archivo local a una ruta remota garantizando su carpeta."""
    remote_file_path = remote_file_path.replace('\\', '/')
    remote_dir = '/'.join(remote_file_path.split('/')[:-1])
    file_name = remote_file_path.split('/')[-1]

    if remote_dir:
        make_dirs(ftp, remote_dir)
        ftp.cwd(remote_dir)
    else:
        ftp.cwd('/')

    with open(local_path, 'rb') as f:
        ftp.storbinary(f'STOR {file_name}', f)

def upload_directory_tree(ftp, local_dir_path, remote_base_dir):
    """Sube recursivamente todo el contenido de una carpeta local."""
    local_dir = Path(local_dir_path)
    if not local_dir.exists():
        return

    count = 0
    for root, dirs, files in os.walk(local_dir):
        # Excluir carpetas temporales y cache
        if '__pycache__' in root or '.git' in root or '.venv' in root:
            continue

        rel_root = os.path.relpath(root, local_dir_path)
        if rel_root == '.':
            target_remote_dir = remote_base_dir
        else:
            target_remote_dir = f"{remote_base_dir}/{rel_root.replace(os.sep, '/')}"

        for file in files:
            if file.endswith('.pyc') or file == '.DS_Store':
                continue
            local_file = Path(root) / file
            remote_file = f"{target_remote_dir}/{file}"
            print(f"  -> {remote_file}")
            upload_file(ftp, local_file, remote_file)
            count += 1
    print(f"Total archivos subidos en {local_dir_path}: {count}")

def main():
    print("==================================================================")
    print("INICIANDO DESPLIEGUE DE ORINOQUIA EXPLORER A BBINGENIEROS.ONLINE")
    print(f"Destino Web: https://bbingenieros.online{REMOTE_APP_ROOT}/")
    print("==================================================================")

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    print(f"Conectando por FTPS a {HOST}:{PORT}...")
    ftp = ftplib.FTP_TLS(context=ctx)
    ftp.connect(HOST, PORT)
    ftp.login(USER, PASS)
    ftp.prot_p()
    ftp.set_pasv(True)
    print("Conexión FTP establecida con éxito.")

    # 1. Asegurar directorios base
    print("\n1. Verificando directorios en el servidor...")
    make_dirs(ftp, REMOTE_APP_ROOT)
    make_dirs(ftp, REMOTE_PUB_ROOT)
    make_dirs(ftp, f"{REMOTE_APP_ROOT}/tmp")
    make_dirs(ftp, f"{REMOTE_PUB_ROOT}/static")
    make_dirs(ftp, f"{REMOTE_PUB_ROOT}/media")

    # 2. Subir archivos raíz a /home/bbingeni/orinoquiaxp/
    print("\n2. Subiendo archivos de configuración raíz a la app...")
    for local_name, remote_name in CORE_FILES:
        local_p = BASE_DIR / local_name
        if local_p.exists():
            remote_p = f"{REMOTE_APP_ROOT}/{remote_name}"
            print(f"  Subiendo {local_name} -> {remote_p}")
            upload_file(ftp, local_p, remote_p)

    # 3. Subir módulos y código fuente a /home/bbingeni/orinoquiaxp/
    print("\n3. Subiendo código fuente y módulos Django...")
    for dir_name in CORE_DIRS:
        local_d = BASE_DIR / dir_name
        if local_d.exists():
            remote_d = f"{REMOTE_APP_ROOT}/{dir_name}"
            print(f"\nSubiendo directorio {dir_name}/...")
            upload_directory_tree(ftp, local_d, remote_d)

    # 4. Subir .htaccess a /public_html/orinoquiaxp/.htaccess
    print("\n4. Configurando public_html/orinoquiaxp/.htaccess...")
    htaccess_p = BASE_DIR / '.htaccess'
    if htaccess_p.exists():
        upload_file(ftp, htaccess_p, f"{REMOTE_PUB_ROOT}/.htaccess")
        print("  .htaccess desplegado exitosamente en public_html.")

    # 5. Sincronizar static y media en public_html
    print("\n5. Sincronizando estáticos y multimedia en public_html...")
    upload_directory_tree(ftp, BASE_DIR / 'static', f"{REMOTE_PUB_ROOT}/static")
    upload_directory_tree(ftp, BASE_DIR / 'media', f"{REMOTE_PUB_ROOT}/media")

    # 6. Reiniciar Passenger
    print("\n6. Reiniciando servidor Passenger (reload)...")
    restart_local = BASE_DIR / 'restart.txt'
    with open(restart_local, 'w') as f:
        f.write('restart')
    upload_file(ftp, restart_local, f"{REMOTE_APP_ROOT}/tmp/restart.txt")
    if restart_local.exists():
        os.remove(restart_local)
    print("  Archivo restart.txt colocado en tmp/. Servidor reiniciado.")

    ftp.quit()
    print("\n==================================================================")
    print("DESPLIEGUE FINALIZADO EXITOSAMENTE")
    print("URL: https://bbingenieros.online/orinoquiaxp/")
    print("==================================================================")

if __name__ == '__main__':
    main()
