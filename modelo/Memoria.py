import random

class Memoria:
    def __init__(self):
        self.memoria_principal = [["" for _ in range(4)] for _ in range(4)]
        self.memoria_virtual = [["" for _ in range(8)] for _ in range(8)]
        self.inicializar_memoria()
        
    def inicializar_memoria(self):
        self.memoria_principal[0][0] = "SO"
        self.memoria_principal[0][1] = "SO"
        self.memoria_principal[1][0] = "SO"
        self.memoria_principal[1][1] = "SO"
        
    def obtener_memoria_principal(self):
        return self.memoria_principal
    
    def obtener_memoria_virtual(self):
        return self.memoria_virtual
    
    def agregar_proceso(self, nuevo_proceso):
        print("Estado de la memoria antes de agregar:", self.memoria_principal)
        for fila in self.memoria_principal:
            if "" in fila:
                index = fila.index("")
                fila[index] = nuevo_proceso
                print("Proceso agregado a la memoria principal:", nuevo_proceso)
                break
            
        for fila in self.memoria_virtual:
            if len(fila) < 8:
                fila.append(nuevo_proceso)
                print("Proceso agregado a la memoria virtual: ", nuevo_proceso)
                return True
        return False
    
    def limpiar_memoria(self, proceso):
        print("Estado de la memoria antes de limpiarla:")
        print("Memoria principal:", self.memoria_principal)
        print("Memoria virtual:", self.memoria_virtual)
        
        for i in range(len(self.memoria_principal)):
            for j in range(len(self.memoria_principal[i])):
                if self.memoria_principal[i][j] == proceso:
                    self.memoria_principal[i][j] = ""  # Restablece a cadena vacía si coincide con el proceso
                    
        for i in range(len(self.memoria_virtual)):
            for j in range(len(self.memoria_virtual[i])):
                if self.memoria_virtual[i][j] == proceso:
                    self.memoria_virtual[i][j] = ""
    
        print("Estado de la memoria después de limpiarla:")
        print("Memoria principal:", self.memoria_principal)
        print("Memoria virtual:", self.memoria_virtual)
        
    def memoria_disponible(self, memoria):
        for fila in memoria:
            if "" in fila:
                return True
        return False
    
    def calcular_memoria_disponible(self, memoria_virtual):
        contador = 0
        for fila in memoria_virtual:
            for columna in fila:
                if columna == "":
                    contador += 1
        return contador
            
    def paginas(self, nuevo_proceso):
        auxiliar = nuevo_proceso.get_tamano_proceso()
        return (auxiliar + 2 - 1) // 2
    
    def generar_nombre_pagina(self, id_proceso, numero_pagina):
        return f"P{numero_pagina}{id_proceso}"
 
    def agregar_paginas_a_memoria_principal(self, proceso):
        print(f"Tamaño de memoria: {proceso.get_tamano_proceso()}")
        agregado_en_principal = 0
        paginas_en_pricipal = 2
        id_pagina = 1

        while agregado_en_principal < paginas_en_pricipal:
            fila_memoria_principal = random.randint(0, 3)
            columna_memoria_principal = random.randint(0, 3)
            
            if agregado_en_principal < paginas_en_pricipal:
                if self.memoria_principal[fila_memoria_principal][columna_memoria_principal] == "":
                    self.memoria_principal[fila_memoria_principal][columna_memoria_principal] = f"P{proceso.get_id_proceso()}{id_pagina}"
                    agregado_en_principal += 1
                    id_pagina += 1
                else:
                    print(f"Posición ({fila_memoria_principal}, {columna_memoria_principal}) ocupada. Buscando otra posición...")
        
        return True
                    
    def agregar_paginas_a_memoria_virtual(self, proceso):
        print(f"Tamaño en virtual: {proceso.get_tamano_proceso()}")
        valor = self.paginas(proceso)
        print(f"Paginas a virtual: {valor - 2}")
        
        agregado_en_virtual = 0
        paginas_en_pricipal = 2
        paginas_en_virtual = valor - paginas_en_pricipal
        id_pagina = 3

        while agregado_en_virtual < paginas_en_virtual:
            fila_memoria_virtual = random.randint(0,7)
            columna_memoria_virtual = random.randint(0,7)
            
            if agregado_en_virtual < paginas_en_virtual:
                if self.memoria_virtual[fila_memoria_virtual][columna_memoria_virtual] == "":
                    self.memoria_virtual[fila_memoria_virtual][columna_memoria_virtual] = f"P{proceso.get_id_proceso()}{id_pagina}"
                    agregado_en_virtual += 1
                    id_pagina += 1
                else:
                    print(f"Posición ({fila_memoria_virtual}, {columna_memoria_virtual}) ocupada. Buscando otra posición...")
                     
        return True
    
    def agregar_proceso_aleatorio(self, proceso):
        if not self.memoria_disponible(self.memoria_principal):
            print("No hay espacio disponible en la memoria principal.")
            return False
        self.agregar_paginas_a_memoria_principal(proceso)
        self.agregar_paginas_a_memoria_virutal(proceso)                
        return True