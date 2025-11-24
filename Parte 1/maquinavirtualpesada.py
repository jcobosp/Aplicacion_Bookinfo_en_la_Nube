# David Calvo Muñoz, Samuel Ignacio Limón Riesgo, Jesús Cobos Pozo
import os
import subprocess
import re
from multiprocessing import Process

# Clonar el repositorio de GitHub
def clone_github_repository(url_del_repositorio):
    subprocess.run(["git", "clone", url_del_repositorio])

# Instalar todos los requisitos y extensiones de la práctica
def install_requirements_dependencies(path_requirements):
    subprocess.run(['sudo', 'apt-get', 'update'])
    subprocess.run(['sudo', 'apt', 'install', 'python3-pip'])
    subprocess.run(['pip3', 'install', '-r', path_requirements])

# Definir el nombre de nuestro grupo como variable
def set_group_name_variable(numero_de_grupo):
    os.environ['GRUPO_NUMERO'] = numero_de_grupo

# Modificar la función getProducts en el archivo productpage_monolith.py
def inspect_and_modify_code(path_monolith, numero_de_grupo):
    with open(path_monolith, 'r') as file:
       contenido_fichero = file.read()

    donde_empieza_getProducts = r"(def getProducts\(\):[\s\S]*?])"
    change_line1_get_products = f"numero_de_grupo = os.getenv('GRUPO_NUMERO', '{numero_de_grupo}')"
    change_line2_get_products = r"\1"
    change_function_getProducts = f"{change_line1_get_products}\n{change_line2_get_products}"

    cambiar_el_codigo = re.sub(donde_empieza_getProducts, change_function_getProducts,contenido_fichero, flags=re.MULTILINE)

    # Modificar la línea del título para añadirle el nombre del grupo
    donde_empieza_titulo = r"'title': '(.*?)',"
    change_title = f"'title': '\\1 {numero_de_grupo}',"

    cambiar_el_codigo = re.sub(donde_empieza_titulo, change_title, cambiar_el_codigo)

    with open(path_monolith, 'w') as file:
        file.write(cambiar_el_codigo)

# Para desplegar los dos puertos y que funcionen a la vez
def start_application_in_both_ports(path_monolith, ports):
    ejecucion = [Process(target=start_application, args=(path_monolith, port)) for port in ports]

    for process in ejecucion:
        process.start()

    for process in ejecucion:
        process.join()

# Arrancar la aplicación mediante el comando: python3 productpage_monolith.py puerto 
def start_application(path_monolith, port):
    subprocess.run(['python3', path_monolith, str(port)])

# Ejecución de todas las funciones a la vez para la configuración y arranque de la aplicación
def launch_application(numero_de_grupo, url_del_repositorio, path_monolith,nombre_practica, ports, path_requirements):
    if not os.path.exists(nombre_practica):
        clone_github_repository(url_del_repositorio)
        install_requirements_dependencies(path_requirements)
        set_group_name_variable(numero_de_grupo)
        inspect_and_modify_code(path_monolith, numero_de_grupo)

        start_application_in_both_ports(path_monolith, ports)
    
    else:
        print(f"El directorio '{nombre_practica}' ya existe. No se realizarán cambios.")
        start_application_in_both_ports(path_monolith, ports)

if __name__ == '__main__':
    numero_de_grupo = 'Grupo34'
    url_del_repositorio = 'https://github.com/CDPS-ETSIT/practica_creativa2.git'
    path_monolith = 'practica_creativa2/bookinfo/src/productpage/productpage_monolith.py'
    path_requirements = 'practica_creativa2/bookinfo/src/productpage/requirements.txt'
    nombre_practica = 'practica_creativa2'
    puertos = [9080, 9081]

    launch_application(numero_de_grupo, url_del_repositorio, path_monolith, nombre_practica, puertos, path_requirements)