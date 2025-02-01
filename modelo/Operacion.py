from modelo.Colas import Bloqueados
from Prueba.Variables import Variables

class Cambio_estado:
    def __init__(self):
        pass  # No se necesitan variables de instancia, ya que usamos variables estáticas
    @staticmethod
    def enviar_a_listo_o_bloqueado_o_terminado():
        no_pasa_a_bloqueados = True
        
        if Variables.proceso_ejecucion.get_prioridad()==0:
            no_pasa_a_bloqueados,id_recursos = Variables.proceso_ejecucion.no_pasa_a_bloqueados()
        
        if no_pasa_a_bloqueados:
            Variables.proceso_ejecucion.set_tamano_proceso(int (Variables.proceso_ejecucion.get_tamano_proceso())-2)
            if int (Variables.proceso_ejecucion.get_tamano_proceso()) > 0:
                Cambio_estado.de_ejecucion_a_listos()
            else:
                Cambio_estado.de_ejecucion_a_terminados()
        else:
            Cambio_estado.de_ejecucion_a_bloqueado(id_recursos)
        return None
    @staticmethod
    def de_ejecucion_a_listos():
        recursos_liberados = Variables.proceso_ejecucion.liberar_recursos_L()
        # recursos_asginados = proceso_ejecucion.get_recursos_asignados()
        recursos_necesarios = Variables.proceso_ejecucion.get_recursos_necesarios()
        # for recurso in recursos_liberados:
        #     print(f"Recurso { recurso.get_nombre_recurso() } liberado.")
        # # for recurso in recursos_asginados:
        # #     print(f"Recurso { recurso.get_nombre_recurso() } asignado.")
        # for recurso in recursos_necesarios:
        #     print(f"Recurso { recurso.get_nombre_recurso() } necesarios.") 
        Variables.proceso_ejecucion.set_estado("listo")
        if Variables.proceso_ejecucion.get_prioridad()==0:
            Variables.cola_listos.append(Variables.proceso_ejecucion)
        else:
            Variables.cola_prioridad1.append(Variables.proceso_ejecucion)

    @staticmethod
    def de_ejecucion_a_bloqueado(id_recursos):
        Variables.proceso_ejecucion.liberar_recursos_B()
        Variables.proceso_ejecucion.set_estado("bloqueado")
        for idR in Variables.id_recursos:
            Bloqueados.enviar_a_cola_bloqueados(idR,Variables.proceso_ejecucion)

    @staticmethod
    def de_ejecucion_a_terminados():
        Variables.proceso_ejecucion.set_estado("terminado")
        Variables.terminados.append(Variables.proceso_ejecucion)
        Variables.memoria_instance.limpiar_memoria(Variables.proceso_ejecucion)
        Variables.proceso_ejecucion.liberar_todos_recursos()

    @staticmethod
    def de_listos_a_ejecucion():
        if Variables.cola_prioridad1:
            proceso_ejecucion = Variables.cola_prioridad1.pop(0)
        elif Variables.cola_listos:
            proceso_ejecucion = Variables.cola_listos.pop(0)
        proceso_ejecucion.set_estado("ejecucion")

    @staticmethod
    def de_nuevo_a_listo():
        while Variables.cola_nuevos:
            proceso_nuevo = Variables.cola_nuevos.pop(0)
            proceso_nuevo.set_estado("listo")
            if proceso_nuevo.get_prioridad()==0:
                Variables.cola_listos.append(proceso_nuevo)
            elif proceso_nuevo.get_prioridad()==1:
                Variables.cola_prioridad1.append(proceso_nuevo)
            else:
                Variables.cola_prioridad1.append(proceso_nuevo)
            # print(f"Proceso {proceso_nuevo.get_id_proceso()} movido a cola de listos.")

    @staticmethod
    def romper_interbloqueo():
        for i in Bloqueados.recursos_interbloqueos(Bloqueados.interbloqueados,Variables.cola_listos):
            Variables.recursos[i-1].set_proceso(None)
        Bloqueados.interbloqueados = []

    @staticmethod
    def expulsar_un_proceso_e_ingresar_otro(): # envia el proceso en ejecucion a listo sin descontar el tamano

        Variables.cola_listos.insert(0,Variables.proceso_ejecucion)
        Variables.proceso_ejecucion.liberar_recursos_B()
        Variables.proceso_ejecucion.set_estado("listo")

        Variables.proceso_ejecucion = Variables.cola_prioridad1.pop(0)
        Variables.proceso_ejecucion.set_estado("ejecucion")