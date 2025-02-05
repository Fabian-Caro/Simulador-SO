import random
from dataclasses import dataclass

@dataclass
class Procesos:
    id_proceso: int
    nombre_proceso: str
    tamano_proceso: int
    prioridad: int
    recursos_necesarios: list
    estado: str
    veces_ejecutado: int
    hilos: list
    
    def __init__(
        self,
        id_proceso,
        nombre_proceso,
        tamano_proceso,
        prioridad,
        recursos_necesarios,
        estado,
        veces_ejecutado,
        hilos,
    ):
        self.id_proceso = id_proceso
        self.nombre_proceso = nombre_proceso
        self.tamano_proceso = tamano_proceso
        self.prioridad = prioridad
        self.recursos_necesarios = recursos_necesarios
        self.estado = estado
        self.veces_ejecutado = veces_ejecutado
        self.hilos = hilos
        

    def get_id_proceso(self):
        return self.id_proceso
    
    def set_id_proceso(self, id_proceso):
        if isinstance(id_proceso, str):
            self.id_proceso = id_proceso
        else:
            raise ValueError("ID_proceso debe ser una cadena de texto.")
        
    def get_nombre_proceso(self):
        return self.nombre_proceso
    
    def set_nombre_proceso(self, nombre_proceso):
        if isinstance(nombre_proceso, str):
            self.nombre_proceso = nombre_proceso
        else:
            raise ValueError("nombre_proceso debe ser una cadena de texto.")
        
    def get_tamano_proceso(self):
        return self.tamano_proceso
    
    def set_tamano_proceso(self, tamano_proceso):
        if isinstance(tamano_proceso, (int, float)):
            if tamano_proceso >= 0:
                self.tamano_proceso = tamano_proceso
            else:
                self.tamano_proceso = 0
        else:
            raise ValueError("Tamaño_proceso debe ser un número.")
        
    def get_prioridad(self):
        return self.prioridad
    
    def set_priorida(self,prioridad):
        self.prioridad = prioridad
    
    def get_nombre_recursos(self):
        return [recurso.get_nombre_recurso() for recurso in self.recursos_asignados]
    
    def get_recursos_necesarios(self):
        # Devuelve una lista, asegúrate de que nunca devuelva None
        return self.recursos_necesarios if self.recursos_necesarios is not None else []
    
    def set_recursos_necesarios(self, recursos_necesarios):
        self.recursos_necesarios = recursos_necesarios
    
    def get_estado(self):
        return self.estado
    
    def set_estado(self,estado):
        self.estado = estado
        
    def get_veces_ejecutado(self):
        return self.veces_ejecutado
    
    def set_veces_ejecutado(self,veces_ejecutado):
        self.veces_ejecutado = veces_ejecutado
        
    def get_hilos(self):
        return self.hilos
    
    def set_hilos(self, hilos):
        self.hilos = hilos
    
    def no_pasa_a_bloqueados(self):
        pasa_a_bloqueado = True
        recursos_no_disponibles = []
        for recurso in self.recursos_necesarios:
            if recurso.get_proceso() != self and recurso.get_proceso() != None:
                pasa_a_bloqueado = False
                recursos_no_disponibles.append(int(recurso.get_id_recurso()))
        return pasa_a_bloqueado,recursos_no_disponibles
    
    def liberar_recursos_L(self):
        recursos_libres = []
        for recurso in self.recursos_necesarios:
            if random.random() < 0.5:
                recurso.set_proceso(None)
                recursos_libres.append(recurso)
            else:
                recurso.set_proceso(self)
        # self.recursos_asignados = [r for r in self.recursos_necesarios if r not in recursos_libres]
        self.recursos_necesarios = [r for r in self.recursos_necesarios if r not in recursos_libres]
        return recursos_libres

    def liberar_recursos_B(self):
        # recursos_libres = []
        for recurso in self.recursos_necesarios:
            if recurso.get_proceso() == self:
                if random.random() < 0.5:
                    recurso.set_proceso(None)
                    # recursos_libres.append(recurso)
                    
        # self.recursos_necesarios = [r for r in self.recursos_necesarios if r not in recursos_libres]
        # return recursos_libres
    
    def liberar_todos_recursos(self):
        for recurso in self.recursos_necesarios:
            if recurso.get_proceso()==self:
                recurso.set_proceso(None)