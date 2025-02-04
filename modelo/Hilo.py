from dataclasses import dataclass

@dataclass
class Hilo:
    id_hilo: int
    nombre_hilo: str
    tamano_hilo: int
    prioridad_hilo: int
    recursos_necesarios_hilo: list
    estado_hilo: str
    veces_ejecutado_hilo: int
    
    def __init__ (self, 
                  id_hilo,
                  nombre_hilo,
                  tamano_hilo,
                  prioridad_hilo,
                  recursos_necesarios_hilo,
                  estado_hilo,
                  veces_ejecutado_hilo
                  ):
        self.id_hilo = id_hilo
        self.nombre_hilo = nombre_hilo
        self.tamano_hilo = tamano_hilo
        self.prioridad_hilo = prioridad_hilo
        self.recursos_necesarios_hilo = recursos_necesarios_hilo
        self.estado_hilo = estado_hilo
        self.veces_ejecutado_hilo = veces_ejecutado_hilo
        
    def get_id_hilo(self):
        return self.id_hilo
    
    def set_id_hilo(self, id_hilo):
        if isinstance(id_hilo, int):
            self.id_hilo = id_hilo
        else:
            raise ValueError("ID_hilo debe ser un número entero.")
        
    def get_nombre_hilo(self):
        return self.nombre_hilo
    
    def set_nombre_hilo(self, nombre_hilo):
        if isinstance(nombre_hilo, str):
            self.nombre_hilo = nombre_hilo
        else:
            raise ValueError("nombre_hilo debe ser una cadena de texto.")
        
    def get_tamano_hilo(self):
        return self.tamano_hilo
    
    def set_tamano_hilo(self, tamano_hilo):
        if isinstance(tamano_hilo, (int, float)):
            if tamano_hilo >= 0:
                self.tamano_hilo = tamano_hilo
            else:
                self.tamano_hilo = 0
        else:
            raise ValueError("Tamaño_hilo debe ser un número.")
        
    def get_prioridad_hilo(self):
        return self.prioridad_hilo
    
    def set_priorida_hilo(self,prioridad_hilo):
        self.prioridad_hilo = prioridad_hilo
        
    def get_nombre_recursos(self):
        return [recurso.get_nombre_recurso() for recurso in self.recursos_asignados]
    
    def get_recursos_necesarios_hilo(self):
        # Devuelve una lista, asegúrate de que nunca devuelva None
        return self.recursos_necesarios_hilo if self.recursos_necesarios_hilo is not None else []
    
    def set_recursos_necesarios_hilo(self, recursos_necesarios_hilo):
        self.recursos_necesarios_hilo = recursos_necesarios_hilo
    
    def get_estado_hilo(self):
        return self.estado_hilo
    
    def set_estado_hilo(self,estado_hilo):
        self.estado = estado_hilo
        
    def get_veces_ejecutado_hilo(self):
        return self.veces_ejecutado_hilo
    
    def set_veces_ejecutado_hilo(self,veces_ejecutado_hilo):
        self.veces_ejecutado_hilo = veces_ejecutado_hilo