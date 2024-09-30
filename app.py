from flask import Flask, request, render_template, redirect, url_for
from modelo.Procesos import Procesos
from modelo.Recurso import Recurso
<<<<<<< HEAD
import random

app = Flask(__name__)

cola_listos = []
# cola_ejecución = []
proceso_ejecucion = None

R = [
=======
from modelo.Colas import Bloqueados
from collections import deque
app = Flask(__name__)

cola_listos = []
proceso_ejecucion = None

recursos = [
>>>>>>> main
    Recurso("001", "Disco duro", None),
    Recurso("002", "Tarjeta gráfica", None),
    Recurso("003", "Impresora", None),
    Recurso("004", "Archivos", None),
    Recurso("005", "Red", None),
<<<<<<< HEAD
    Recurso("006", "Teclado", None),
    Recurso("007", "Raton", None),
    Recurso("008", "Pantalla", None),
    Recurso("009", "Parlante", None)
=======
>>>>>>> main
]

terminados = []

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', procesos_listos=cola_listos, proceso_ejecucion=proceso_ejecucion, recursos=R, terminados=terminados)

@app.route('/crear_proceso', methods=['POST'])
def crear_proceso():
    global proceso_ejecucion
    
    id_proceso = request.form.get('id')
    nombre = request.form.get('nombre')
    tamano = request.form.get('tamano')
    prioridad = request.form.get('prioridad')
<<<<<<< HEAD
    recursos_asignados = [rec for rec in R if rec.get_id_recurso() in request.form.getlist('recursos')]
    # Imprimir los datos en la consola para verificar
    print(f"ID: {id_proceso}, Nombre: {nombre}, Tamaño: {tamano}, Prioridad: {prioridad}, Recursos: {recursos_asignados[0].get_nombre_recurso()}")
    nuevo_proceso = Procesos(id_proceso, nombre, tamano, prioridad, recursos_asignados)
=======
    recurso_seleccionado =  request.form.getlist('recursos')
    
    recursos_asignados = []
    recursos_necesarios = []
    
    # for recurso in recurso_seleccionado:
    #     recursos_necesarios.append(recurso)
    for recurso_id in recurso_seleccionado:
        recurso = next((r for r in recursos if r.get_id_recurso() == recurso_id), None)
        if recurso:
            recursos_necesarios.append(recurso)

    print(f"ID: {id_proceso}, Nombre: {nombre}, Tamaño: {tamano}, Prioridad: {prioridad}, Recursos: {recursos}")
    nuevo_proceso = Procesos(id_proceso, nombre, tamano, prioridad, recursos_asignados, recursos_necesarios)
>>>>>>> main
    
    cola_listos.append(nuevo_proceso)
    
    if not proceso_ejecucion and cola_listos:
        posible_proceso = cola_listos.pop(0)
        
        proceso_ejecucion = posible_proceso
        
    return redirect(url_for('index'))
    
@staticmethod
def ver_si_estan_disponibles_recursos():
    recursos =  proceso_ejecucion.get_recursos()
    flag = True
    for r in recursos:
        if R[r].get_disponibilidad_recurso() != proceso_ejecucion and R[r].get_disponibilidad_recurso() != None:
            flag = False
            break
    return flag

@staticmethod
def de_ejecucion_a_listos():
    recursos_liberados = proceso_ejecucion.liberar_recursos()
    # recursos_asginados = proceso_ejecucion.get_recursos_asignados()
    # recursos_necesarios = proceso_ejecucion.get_recursos_necesarios()
    # for recurso in recursos_liberados:
    #     print(f"Recurso { recurso.get_nombre_recurso() } liberado.")
    # for recurso in recursos_asginados:
    #     print(f"Recurso { recurso.get_nombre_recurso() } asignado.")
    # for recurso in recursos_necesarios:
    #     print(f"Recurso { recurso.get_nombre_recurso() } necesarios.") 
    cola_listos.append(proceso_ejecucion)

@staticmethod
def liberar_o_no_recurso():
    recursos =  proceso_ejecucion.get_recursos()
    i = 0
    for r in recursos:
        se_libera = random.randint(True,False)
        if se_libera:
            proceso_ejecucion.get_recursos().pop(i)
            R[r] = None

@staticmethod
def de_ejecucion_a_terminados():
    terminados.append(proceso_ejecucion.get_nombre_proceso())

@app.route('/ejecutar_proceso', methods=['POST'])
def ejecutar_proceso():
    global proceso_ejecucion
    
    proceso_ejecucion.set_tamano_proceso(int (proceso_ejecucion.get_tamano_proceso())-2)
    if cola_listos:
<<<<<<< HEAD
        if proceso_ejecucion.get_tamano() > 0:
            if ver_si_estan_disponibles_recursos(proceso_ejecucion):
                de_ejecucion_a_listos()
            # else:
            #     enviar_a_bloqueados()
=======
        if proceso_ejecucion.get_tamano_proceso() > 0:
            no_pasa_a_bloqueados,id_recursos = proceso_ejecucion.no_pasa_a_bloqueados()

            if no_pasa_a_bloqueados:
                de_ejecucion_a_listos()
            else:
                for idR in id_recursos:
                    Bloqueados.enviar_a_cola_bloqueados(idR,proceso_ejecucion.get_nombre_proceso())
                #cola_bloqueados.append(proceso_ejecucion.get_nombre_proceso())
>>>>>>> main
        else:
            de_ejecucion_a_terminados()
        if cola_listos:
            proceso_ejecucion = cola_listos.pop(0)
    else:
        if proceso_ejecucion.get_tamano_proceso() == 0:
            de_ejecucion_a_terminados()
            proceso_ejecucion.terminar_ejecucion()
            proceso_ejecucion = None
    # if len(terminados>0):
    resultado = ', '.join(map(str, terminados))
    print("Cola de bloqueados Disco duro: " + str(list(Bloqueados.r1)))
    print("Cola de bloqueados Tarjeta gráfica: " + str(list(Bloqueados.r2)))
    print("Cola de bloqueados Impresora: " + str(list(Bloqueados.r3)))
    print("Cola de bloqueados Archivos: " + str(list(Bloqueados.r4)))
    print("Cola de bloqueados Red: " + str(list(Bloqueados.r5)))
    print("procesos terminados: "+str(resultado))
    
    # else:
    #     print("No hay ningun proceso terminado") 
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)