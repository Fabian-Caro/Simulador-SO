from flask import Flask, flash, request, render_template, redirect, url_for, jsonify
from modelo.Procesos import Procesos
from modelo.Recurso import recursos as listaRecursos
from modelo.Bloqueados import Bloqueados
from modelo.Memoria import Memoria
from modelo.Hilo import Hilo
import random


app = Flask(__name__)
app.secret_key = '1234'

memoria_instance = Memoria()

procesos_creados = []
cola_nuevos = []
cola_listos = []
hilos_listos = []
hilos_con_prioridad = []
cola_prioridad1 = []
cola_bloqueados = []
proceso_ejecucion = None
hilo_ejecucion: Hilo = None
proceso_bloqueado = None
terminados = []
hilos_terminados = []
proceso_creado = []
auxiliar = 1

@app.route('/', methods=['GET'])
def index():
    bloqueados = Bloqueados.bloqueados()
    recursos = listaRecursos

    return render_template(
        'index.html',
        procesos_nuevos=cola_nuevos,
        procesos_listos=cola_listos, 
        procesos_prioridad1 = cola_prioridad1,
        proceso_ejecucion=proceso_ejecucion, 
        proceso_bloqueado=proceso_bloqueado, 
        recursos=recursos, 
        proceso_creado = proceso_creado,
        terminados=terminados,
        bloqueados=bloqueados)  # Devuelve la vista cuando es un GET

@app.route('/crear_proceso', methods=['GET', 'POST'])
def crear_proceso():
    bloqueados = Bloqueados.bloqueados()
    recursos = listaRecursos
    
    # memoria_disponible = memoria_instance.calcular_memoria_disponible(memoria_instance.memoria_virtual)
    # print(f"Memoria disponible: {memoria_disponible} KB")
    
    max_tamano = 10
    # print(f"Tamaño máximo de proceso: {max_tamano} KB")
    
    siguiente_id = id_autoincremental()

    if request.method == 'POST':
        
        if not memoria_instance.memoria_disponible(memoria_instance.memoria_principal):
            flash("No hay espacio disponible en la memoria principal. No se creará el proceso.", "danger")
            return redirect(url_for('crear_proceso'))

        id_proceso = request.form.get('id')
        nombre = request.form.get('nombre')
        
        for proceso in procesos_creados:
            if proceso.get_nombre_proceso() == nombre:
                flash("El proceso necesita un nombre distinto", "danger")
                return redirect(url_for('crear_proceso'))
        
        tamano = int(request.form.get('tamano'))
        
        if tamano > max_tamano:
            flash("El proceso no se pudo crear. Tamaño insuficiente.", "danger")
            return redirect(url_for('crear_proceso'))
        
        prioridad = int(request.form.get('prioridad',0))

        recurso_seleccionado =  request.form.getlist('recursos')

        recursos_necesarios = []

        for recurso_id in recurso_seleccionado:
            recurso = next((r for r in recursos if r.get_id_recurso() == recurso_id), None)
            if recurso:
                recursos_necesarios.append(recurso)

        print(f"ID: {id_proceso}, Nombre: {nombre}, Tamaño: {tamano}, prioridad: {prioridad} veces ejecutado: 0")
        for recurso in recursos:
           print(f"Recursos: {recurso}")

        nuevo_proceso = Procesos(id_proceso, nombre, tamano, prioridad, recursos_necesarios,"nuevo", 0, 0)
        
        nuevo_proceso.set_hilos(Hilo.crear_hilos(nuevo_proceso))
        procesos_creados.append(nuevo_proceso)
        cola_nuevos.append(nuevo_proceso)
        proceso_creado.append(nuevo_proceso)
        agregar_a_memoria(nuevo_proceso)

        flash("Proceso creado exitosamente.", "success")
        return redirect(url_for('crear_proceso'))

    return render_template(
        'creacion.html', 
        siguiente_id = siguiente_id,        
        procesos_nuevos=cola_nuevos,
        recursos=recursos, 
        proceso_creado = proceso_creado,
        bloqueados=bloqueados,
        max_tamano = max_tamano,
        cola_listos = cola_listos,
        )  # Devuelve la vista cuando es un GET

@app.route('/modelo', methods=['GET', 'POST'])
def modelo():
    bloqueados = Bloqueados.bloqueados()
    recursos = listaRecursos
    
    if request.method == 'POST':
        ejecutar_proceso()

    return render_template('modelo.html',        
        procesos_nuevos=cola_nuevos,
        procesos_listos=cola_listos, 
        procesos_prioridad1 = cola_prioridad1,
        proceso_ejecucion=proceso_ejecucion, 
        proceso_bloqueado=proceso_bloqueado, 
        recursos=recursos, 
        proceso_creado = proceso_creado,
        terminados=terminados,
        bloqueados=bloqueados,
        cola_listos = cola_listos,
        hilos_listos = hilos_listos,
        hilos_con_prioridad = hilos_con_prioridad,
        hilo_ejecucion = hilo_ejecucion,
        )  # Devuelve la vista cuando es un GET)

@app.route('/memoria', methods=['GET'])
def memoria():
    memoria_principal = memoria_instance.obtener_memoria_principal()
    memoria_virtual = memoria_instance.obtener_memoria_virtual()
    return render_template('memoria.html', memoria_principal=memoria_principal, memoria_virtual = memoria_virtual)

def id_autoincremental():
    if not len(cola_nuevos):
        return len(cola_listos) + (len(Bloqueados.recurso1) + len(Bloqueados.recurso2) 
                                    + len(Bloqueados.recurso3) + len(Bloqueados.recurso4) 
                                    + len(Bloqueados.recurso5)) + len(terminados) + 1
    else:
        return len(cola_nuevos) + len(terminados) + 1   
    
def agregar_a_memoria(nuevo_proceso):
    if not memoria_instance.agregar_paginas_a_memoria_principal(nuevo_proceso):
        print("No se pudo agregar el proceso a la memoria principal.")

    if not memoria_instance.agregar_paginas_a_memoria_virtual(nuevo_proceso):
        print("No se pudo agregar el proceso a la memoria virtual.")

@app.route('/ejecutar_proceso', methods=['POST'])
def ejecutar_proceso():
    global proceso_ejecucion
    global hilo_ejecucion
    de_nuevo_a_listo()
     
    if not proceso_ejecucion:
        if Bloqueados.interbloqueados:
            romper_interbloqueo()
        else:
            de_listos_a_ejecucion()
            
            if proceso_ejecucion:
                proceso_ejecucion.set_veces_ejecutado(proceso_ejecucion.get_veces_ejecutado() + 1)
                
                if hilo_ejecucion:
                    hilo_ejecucion.set_veces_ejecutado(hilo_ejecucion.get_veces_ejecutado() + 1)

                buscar_en_memoria(proceso_ejecucion.get_veces_ejecutado())
    else:
        if cola_prioridad1 and proceso_ejecucion.get_prioridad()==0 and cola_prioridad1[0].get_prioridad()==2:
            expulsar_un_proceso_e_ingresar_otro() # envia el proceso en ejecucion a listo sin descontar el tamano
        else:
            proceso_ejecucion = enviar_a_listo_o_bloqueado_o_terminado()

    
    Bloqueados.mostrar_estado_colas(terminados)
    verificar_bloqueados()        
    return redirect(url_for('modelo'))

def buscar_en_memoria(indice_pagina):
    global proceso_ejecucion
    global auxiliar
    nombre_pagina_buscada = f"P{proceso_ejecucion.get_id_proceso()[-2:]}{indice_pagina}"
    print(f"Verificando la página {nombre_pagina_buscada}...")

    # Verificar si la página está en la memoria
    estado = memoria_instance.buscar_en_memoria(nombre_pagina_buscada)
    
    if estado == "memoria_principal":
        print(f"La página {nombre_pagina_buscada} está en la memoria principal.")
    elif estado == "memoria_virtual":
        print(f"La página {nombre_pagina_buscada} está en la memoria virtual.")
        memoria_instance.agregar_pagina_necesitada(nombre_pagina_buscada, proceso_ejecucion)
    else:
        print(f"La página {nombre_pagina_buscada} NO está en ninguna memoria.")
        # Agregar página a la lista de necesarias si no está en la memoria
        
    
    # Procesar páginas que necesiten ser cargadas
    memoria_instance.manejar_pagina_necesitada()

    # Imprimir el estado de las memorias
    memoria_principal = memoria_instance.obtener_memoria_principal()
    memoria_virtual = memoria_instance.obtener_memoria_virtual()
    print(f"Memoria principal: {memoria_principal}")
    print(f"Memoria virtual: {memoria_virtual}")
    auxiliar += 1


def enviar_a_listo_o_bloqueado_o_terminado():
    global proceso_ejecucion
    global hilo_ejecucion

    no_pasa_a_bloqueados = True
    
    if proceso_ejecucion.get_prioridad()==0:
        no_pasa_a_bloqueados,id_recursos = proceso_ejecucion.no_pasa_a_bloqueados()
    
    if no_pasa_a_bloqueados:
        tam_proceso = proceso_ejecucion.get_tamano_proceso()
        tam_proceso = tam_proceso - proceso_ejecucion.get_veces_ejecutado()
        if int (tam_proceso) > 0:
            de_ejecucion_a_listos()
        else:
            de_ejecucion_a_terminados()
    else:
        de_ejecucion_a_bloqueado(id_recursos)
    return None

def de_ejecucion_a_listos():
    recursos_liberados = proceso_ejecucion.liberar_recursos_L()
    recursos_necesarios = proceso_ejecucion.get_recursos_necesarios()
    proceso_ejecucion.set_estado("listo")
    # hilo_ejecucion.set_estado("listo")
    if proceso_ejecucion.get_prioridad()==0:
        cola_listos.append(proceso_ejecucion)
        hilos_listos.append(hilo_ejecucion)
    else:
        cola_prioridad1.append(proceso_ejecucion)
        hilos_con_prioridad.append(hilo_ejecucion)

def de_ejecucion_a_bloqueado(id_recursos):
    proceso_ejecucion.liberar_recursos_B()
    proceso_ejecucion.set_estado("bloqueado")
    for idR in id_recursos:
        Bloqueados.enviar_a_cola_bloqueados(idR,proceso_ejecucion)

@app.route('/a_listos', methods=['POST'])
def a_listos():
    de_nuevo_a_listo()
    return redirect(url_for('modelo'))

def de_ejecucion_a_terminados():
    global hilo_ejecucion
    proceso_ejecucion.set_estado("terminado")
    
    for hilo in proceso_ejecucion.get_hilos():
        hilo.set_estado("terminado")
        hilos_terminados.append(hilo)
        
        if hilo in hilos_listos:
            hilos_listos.remove(hilo)
        if hilo in hilos_con_prioridad:
            hilos_con_prioridad.remove(hilo)
            
        
    hilo_ejecucion = None
    terminados.append(proceso_ejecucion)
    memoria_instance.limpiar_memoria(proceso_ejecucion)
    proceso_ejecucion.liberar_todos_recursos()

def de_listos_a_ejecucion():
    global proceso_ejecucion
    global hilo_ejecucion
    
    if not cola_prioridad1 and not cola_listos:
        return
    
    if cola_prioridad1:
        proceso_ejecucion = cola_prioridad1.pop(0)
        hilos_del_proceso = [hilos for hilos in hilos_con_prioridad if hilos.get_proceso() == proceso_ejecucion]
        
        if hilos_del_proceso:
            hilo_ejecucion = hilos_del_proceso.pop(0)
            hilos_con_prioridad.remove(hilo_ejecucion)
            hilo_ejecucion.set_estado("ejecucion")
            
        else:
            hilo_ejecucion = None
    elif cola_listos:
        proceso_ejecucion = cola_listos.pop(0)
        hilos_del_proceso = [hilos for hilos in hilos_listos if hilos.get_proceso() == proceso_ejecucion]
        
        if hilos_del_proceso:
            hilo_ejecucion = hilos_del_proceso.pop(0)
            hilos_listos.remove(hilo_ejecucion)
            hilo_ejecucion.set_estado("ejecucion")
            
        else:
            hilo_ejecucion = None
        
    else:
        print("Error: No se pudo asignar un proceso a ejecución.")

def de_nuevo_a_listo():
                    
    while cola_nuevos:
        proceso_nuevo = cola_nuevos.pop(0)
        proceso_nuevo.set_estado("listo")
        if proceso_nuevo.get_prioridad()==0:
            cola_listos.append(proceso_nuevo)

        else:
            cola_prioridad1.append(proceso_nuevo)
            
        for hilo in proceso_nuevo.get_hilos():
            hilo_nuevo = hilo
            hilo_nuevo.set_estado("listo")
            
            if hilo_nuevo.get_prioridad() == 0:
                hilos_listos.append(hilo_nuevo)
                
            else:
                hilos_con_prioridad.append(hilo_nuevo)

def romper_interbloqueo():
    for i in Bloqueados.recursos_interbloqueos(Bloqueados.interbloqueados,cola_listos):
        listaRecursos[i-1].set_proceso(None)
    Bloqueados.interbloqueados = []

def expulsar_un_proceso_e_ingresar_otro(): # envia el proceso en ejecucion a listo sin descontar el tamano
    global proceso_ejecucion

    cola_listos.insert(0,proceso_ejecucion)
    proceso_ejecucion.liberar_recursos_B()
    proceso_ejecucion.set_estado("listo")

    proceso_ejecucion = cola_prioridad1.pop(0)
    proceso_ejecucion.set_estado("ejecucion")

def verificar_bloqueados():
    global proceso_bloqueado
    recursos = listaRecursos

    for recurso_actual in recursos:
        if recurso_actual.get_proceso() is None:
            if recurso_actual.get_id_recurso() == "001" and Bloqueados.recurso1:
                print(f"Recurso 1: Por aquí es, { Bloqueados.recurso1 }")
                proceso_bloqueado = Bloqueados.recurso1.popleft()
                asignar_recurso(proceso_bloqueado, recurso_actual)
                verificar_si_esta_bloqueado(proceso_bloqueado)
            elif recurso_actual.get_id_recurso() == "002" and Bloqueados.recurso2:
                print(f"Recurso 2: Por aquí es, { Bloqueados.recurso2 }")
                proceso_bloqueado = Bloqueados.recurso2.popleft()
                asignar_recurso(proceso_bloqueado, recurso_actual)
                verificar_si_esta_bloqueado(proceso_bloqueado)
            elif recurso_actual.get_id_recurso() == "003" and Bloqueados.recurso3:
                print(f"Recurso 3: Por aquí es, { Bloqueados.recurso3 }")
                proceso_bloqueado = Bloqueados.recurso3.popleft()
                asignar_recurso(proceso_bloqueado, recurso_actual)
                verificar_si_esta_bloqueado(proceso_bloqueado)
            elif recurso_actual.get_id_recurso() == "004" and Bloqueados.recurso4:
                print(f"Recurso 4: Por aquí es, { Bloqueados.recurso4 }")
                proceso_bloqueado = Bloqueados.recurso4.popleft()
                asignar_recurso(proceso_bloqueado, recurso_actual)
                verificar_si_esta_bloqueado(proceso_bloqueado)
            elif recurso_actual.get_id_recurso() == "005" and Bloqueados.recurso5:
                print(f"Recurso 5: Por aquí es, { Bloqueados.recurso5 }")
                proceso_bloqueado = Bloqueados.recurso5.popleft()
                asignar_recurso(proceso_bloqueado, recurso_actual)
                verificar_si_esta_bloqueado(proceso_bloqueado)
            else:
                print(f"Recurso '{recurso_actual.get_nombre_recurso()}' libre")
    
def asignar_recurso(proceso_bloqueado, recurso_actual):
    for recurso_necesitado in proceso_bloqueado.get_recursos_necesarios():
        print(f"Recursos necesarios de {proceso_bloqueado.get_nombre_proceso()}: {recurso_necesitado.get_nombre_recurso()}")
    
    recurso_actual.set_proceso(proceso_bloqueado)
    
    if not verificar_si_esta_bloqueado(proceso_bloqueado):
        print(f"Proceso {proceso_bloqueado.get_nombre_proceso()} tiene todos los recursos necesarios, moviéndolo a cola de listos.")
        cola_listos.append(proceso_bloqueado)
    else:
        print(f"Proceso {proceso_bloqueado.get_nombre_proceso()} aún necesita más recursos.")
        
def verificar_si_esta_bloqueado(proceso):
    for recurso_bloqueado in [Bloqueados.recurso1, Bloqueados.recurso2, Bloqueados.recurso3, Bloqueados.recurso4, Bloqueados.recurso5]:
        if proceso in recurso_bloqueado:
            return True
        
    return False
   
if __name__ == '__main__':
    app.run(debug=True)