import math
from modelo.Procesos import Procesos
from dataclasses import dataclass
@dataclass
class Hilo:
    id: int
    nombre: str
    tamano: int
    prioridad: int
    recursos_necesarios: str
    estado: str
    veces_ejecutado: int
    proceso: Procesos
    
    def __init__ (
        self,
        id,
        nombre,
        tamano,
        prioridad,
        recursos_necesarios,
        estado,
        veces_ejecutado,
        proceso,
    ):
        self.id = id
        self.nombre = nombre
        self.tamano = tamano
        self.prioridad = prioridad
        self.recursos_necesarios = recursos_necesarios
        self.estado = estado
        self.veces_ejecutado = veces_ejecutado
        self.proceso = proceso
        
    def get_id (self):
        return self.id
    
    def get_nombre (self):
        return self.nombre
    
    def get_tamano (self):
        return self.tamano
    
    def get_prioridad (self):
        return self.prioridad
    
    def get_recursos_necesarios (self):
        return self.recursos_necesarios
    
    def get_estado (self):
        return self.estado
    
    def get_veces_ejecutado (self):
        return self.veces_ejecutado
    
    def get_proceso (self):
        return self.proceso
    
    def set_id (self, id):
        self.id = id
        
    def set_nombre (self, nombre):
        self.nombre = nombre
    
    def set_tamano (self, tamano):
        self.tamano = tamano
    
    def set_prioridad (self, prioridad):
        self.prioridad = prioridad
    
    def set_recursos_necesarios (self, recursos_necesarios):
        self.recursos_necesarios = recursos_necesarios
    
    def set_estado (self, estado):
        self.estado = estado
    
    def set_veces_ejecutado (self, veces_ejecutado):
        self.veces_ejecutado = veces_ejecutado
        
    def set_proceso (self, proceso):
        self.proceso = proceso
        
    def crear_hilos(nuevo_proceso):
        hilos: list = []
        recursos_disponibles = nuevo_proceso.get_recursos_necesarios()  # Lista de recursos
        recursos_asignados = []  # Para rastrear los recursos ya usados
        
        i: int = 1
        while i <= math.ceil(nuevo_proceso.get_tamano_proceso()/2):
            
            id_hilo=f"{nuevo_proceso.get_id_proceso()}-{i}"
            nombre_hilo=f"Hilo{i}{nuevo_proceso.get_nombre_proceso()}"
            
            if i == math.ceil(nuevo_proceso.get_tamano_proceso()/2) and nuevo_proceso.get_tamano_proceso()%2!=0:
                tamano_hilo=1
            else:
                tamano_hilo=2

            prioridad_hilo=nuevo_proceso.get_prioridad()
            
            if i - 1 < len(recursos_disponibles):
                recursos_necesarios_hilo = [recursos_disponibles[i - 1]]  # Convertir en lista
                recursos_asignados.append(recursos_disponibles[i - 1])  # Marcarlo como asignado
            else:
                recursos_necesarios_hilo = []  # Si ya no hay recursos, lista vacía
                
            estado = "Nuevo"
            veces_ejecutado_hilo = 0
            nuevo_hilo = Hilo(id_hilo, nombre_hilo, tamano_hilo, prioridad_hilo, recursos_necesarios_hilo, estado, veces_ejecutado_hilo, nuevo_proceso)        
            
            if i == math.ceil(nuevo_proceso.get_tamano_proceso() / 2):
                recursos_sobrantes = [r for r in recursos_disponibles if r not in recursos_asignados]
                nuevo_hilo.set_recursos_necesarios(nuevo_hilo.get_recursos_necesarios() + recursos_sobrantes)

            hilos.append(nuevo_hilo)

            i+=1
            
        return hilos
        
        
        
    
    