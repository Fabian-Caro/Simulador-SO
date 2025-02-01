class Recurso:
    def __init__(self, id_recurso, nombre_recurso, proceso):
        self.__id_recurso = id_recurso
        self.__nombre_recurso = nombre_recurso
        self.__proceso = proceso
        
    def get_id_recurso(self):
        return self.__id_recurso
        
    def get_nombre_recurso(self):
        return self.__nombre_recurso
        
    def get_proceso(self):
        return self.__proceso
    
    def set_proceso(self, proceso):
        self.__proceso= proceso

    def __str__(self):
        # Recorremos la lista de recursos asignados y los convertimos a cadena
        return f"{self.get_nombre_recurso()}"

recursos = [
            Recurso("001", "Disco duro", None),
            Recurso("002", "Tarjeta gráfica", None),
            Recurso("003", "Impresora", None),
            Recurso("004", "Archivos", None),
            Recurso("005", "Red", None),    
        ]