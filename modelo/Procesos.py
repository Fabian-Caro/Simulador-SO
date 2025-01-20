import random

class Procesos:
    def __init__(self, id_proceso, nombre_proceso, tamano_proceso, prioridad, recursos_necesarios,estado):
        self.__id_proceso = id_proceso
        self.__nombre_proceso = nombre_proceso
        self.__tamano_proceso = tamano_proceso
        self.__prioridad = prioridad
        # self.__recursos_asignados = recursos_asignados
        self.__recursos_necesarios = recursos_necesarios
        self.estado = estado

    def get_id_proceso(self):
        return self.__id_proceso
    
    def set_id_proceso(self, id_proceso):
        if isinstance(id_proceso, str):
            self.__id_proceso = id_proceso
        else:
            raise ValueError("ID_proceso debe ser una cadena de texto.")
        
    def get_nombre_proceso(self):
        return self.__nombre_proceso
    
    def set_nombre_proceso(self, nombre_proceso):
        if isinstance(nombre_proceso, str):
            self.__nombre_proceso = nombre_proceso
        else:
            raise ValueError("nombre_proceso debe ser una cadena de texto.")
        
    def get_tamano_proceso(self):
        return self.__tamano_proceso
    
    def set_tamano_proceso(self, tamano_proceso):
        if isinstance(tamano_proceso, (int, float)):
            if tamano_proceso >= 0:
                self.__tamano_proceso = tamano_proceso
            else:
                self.__tamano_proceso = 0
        else:
            raise ValueError("Tamaño_proceso debe ser un número.")
        
    def get_prioridad(self):
        return self.__prioridad
    
    def set_priorida(self,prioridad):
        self.__prioridad = prioridad
    
    def get_nombre_recursos(self):
        return [recurso.get_nombre_recurso() for recurso in self.__recursos_asignados]
    
    def get_recursos_necesarios(self):
        # Devuelve una lista, asegúrate de que nunca devuelva None
        return self.__recursos_necesarios if self.__recursos_necesarios is not None else []
    
    def set_recursos_necesarios(self, recursos_necesarios):
        self.__recursos_necesarios = recursos_necesarios
    
    def get_estado(self):
        return self.estado
    
    def set_estado(self,estado):
        self.estado = estado
    
    def no_pasa_a_bloqueados(self):
        pasa_a_bloqueado = True
        recursos_no_disponibles = []
        for recurso in self.__recursos_necesarios:
            if recurso.get_proceso() != self and recurso.get_proceso() != None:
                pasa_a_bloqueado = False
                recursos_no_disponibles.append(int(recurso.get_id_recurso()))
        return pasa_a_bloqueado,recursos_no_disponibles
    
    def liberar_recursos_L(self):
        recursos_libres = []
        for recurso in self.__recursos_necesarios:
            if random.random() < 0.5:
                recurso.set_proceso(None)
                recursos_libres.append(recurso)
            else:
                recurso.set_proceso(self)
        # self.__recursos_asignados = [r for r in self.__recursos_necesarios if r not in recursos_libres]
        self.__recursos_necesarios = [r for r in self.__recursos_necesarios if r not in recursos_libres]
        return recursos_libres

    def liberar_recursos_B(self):
        # recursos_libres = []
        for recurso in self.__recursos_necesarios:
            if recurso.get_proceso() == self:
                if random.random() < 0.5:
                    recurso.set_proceso(None)
                    # recursos_libres.append(recurso)
                    
        # self.__recursos_necesarios = [r for r in self.__recursos_necesarios if r not in recursos_libres]
        # return recursos_libres
    
    def liberar_todos_recursos(self):
        for recurso in self.__recursos_necesarios:
            if recurso.get_proceso()==self:
                recurso.set_proceso(None)