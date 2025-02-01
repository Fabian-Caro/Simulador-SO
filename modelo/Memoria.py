import random
import re
class Memoria:
    def __init__(self):
        self.memoria_principal = [["" for _ in range(4)] for _ in range(4)]
        self.memoria_virtual = [["" for _ in range(8)] for _ in range(4)]
        self.paginas_necesitadas = set()
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
    
    def limpiar_memoria(self, proceso):
        print("Estado de la memoria antes de limpiarla:")
        print("Memoria principal:", self.memoria_principal)
        print("Memoria virtual:", self.memoria_virtual)
        
        for i in range(len(self.memoria_principal)):
            for j in range(len(self.memoria_principal[i])):
                pattern = rf"P{proceso.get_id_proceso()}.*"
                if re.fullmatch(pattern, self.memoria_principal[i][j]):
                    self.memoria_principal[i][j] = ""
                    
        for i in range(len(self.memoria_virtual)):
            for j in range(len(self.memoria_virtual[i])):
                pattern = rf"P{proceso.get_id_proceso()}.*"
                if re.fullmatch(pattern, self.memoria_virtual[i][j]):
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
                    print(f"Pagina {id_pagina} agregada a la memoria principal")
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
            fila_memoria_virtual = random.randint(0,3)
            columna_memoria_virtual = random.randint(0,7)
            
            print(f"Intentando agregar en {fila_memoria_virtual}, {columna_memoria_virtual}")
            
            if agregado_en_virtual < paginas_en_virtual:
                if self.memoria_virtual[fila_memoria_virtual][columna_memoria_virtual] == "":
                    self.memoria_virtual[fila_memoria_virtual][columna_memoria_virtual] = f"P{proceso.get_id_proceso()}{id_pagina}"
                    agregado_en_virtual += 1
                    print(f"Pagina {id_pagina} agregada a la memoria virtual en {fila_memoria_virtual}, {columna_memoria_virtual}")
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
    
    def agregar_pagina_necesitada(self, pagina, proceso):
        self.paginas_necesitadas.add(pagina)  # Agregar página a las páginas necesitadas
        print(f"La página {pagina} ha sido agregada a las páginas necesitadas")

    def cargar_pagina(self, nombre_pagina):
        print(f"Cargando la página {nombre_pagina}...")
        if nombre_pagina not in self.memoria_principal:
            print(f"La página {nombre_pagina} no se encuentra en la memoria principal")
            pagina_en_memoria_virtual = self.buscar_en_memoria(nombre_pagina)
            print(f"esta es la pagina en memoria virtual {nombre_pagina}")
            
            if pagina_en_memoria_virtual:
                self.reemplazar_pagina_en_memoria_principal(nombre_pagina)
                print(f"La página {nombre_pagina} se carga en la memoria principal")
                
            else:
                print(f"La página {nombre_pagina} no se encuentra en la memoria virtual")
    
    def reemplazar_pagina_en_memoria_principal(self, pagina):
        # Buscar la página más antigua en memoria principal (FIFO)
        print("Reemplazando página en memoria principal...")
        print("la pagina es", pagina)
        for i in range(len(self.memoria_principal)):
            for j in range(len(self.memoria_principal[i])):
                print("valor en el espacio: ", self.memoria_principal[i][j])
                if self.memoria_principal[i][j] == "":
                    pagina_a_reemplazar = self.memoria_principal[i][j]
                    self.memoria_principal[i][j] = pagina
                    print(f"Reemplazando la página {pagina_a_reemplazar} por la página {pagina}.")
                    if self.bajar_pagina_de_memoria_virtual(pagina):
                        self.politica_de_reemplazo(pagina)
                    return

    def manejar_pagina_necesitada(self):
        # Comprobar si hay páginas que necesitan ser cargadas
        if self.paginas_necesitadas:
            pagina = self.paginas_necesitadas.pop()
            print(f"Manejando la página {pagina}")
            self.cargar_pagina(pagina)
        else:
            print("No hay páginas necesitadas en este momento.")
    
    def buscar_en_memoria(self, nombre_pagina_buscada):
    # Primero buscamos en la memoria principal
        for fila in self.memoria_principal:
            for columna in fila:
                if columna == nombre_pagina_buscada:
                    return "memoria_principal"  # Página encontrada en la memoria principal
        
        # Si no la encontramos, buscamos en la memoria virtual
        for fila in self.memoria_virtual:
            for columna in fila:
                if columna == nombre_pagina_buscada:
                    return "memoria_virtual"  # Página encontrada en la memoria virtual
                 
        return None  # Página no encontrada

    def bajar_pagina_de_memoria_virtual(self, pagina):
        print(f"Bajando la página {pagina} de la memoria virtual...")
        for i in range(len(self.memoria_virtual)):
            for j in range(len(self.memoria_virtual[i])):
                if self.memoria_virtual[i][j] == pagina:
                    self.memoria_virtual[i][j] = ""
                    print(f"La página {pagina} ha sido eliminada de la memoria virtual")
                    return True
                
    def politica_de_reemplazo(self, pagina):
        print("politica de reemplazo")
        print(f"pagina: {pagina}")
        
        aux = int(pagina[2])-2
        pagina = pagina[0] + pagina[1] + str(aux)
        print(f"Nueva pagina: {pagina}")
        
        for i in range(len(self.memoria_principal)):
            for j in range(len(self.memoria_principal[i])):
                if self.memoria_principal[i][j] == pagina:
                    self.memoria_principal[i][j] = ""
                    if self.reemplazar_pagina_en_memoria_virtual(pagina):
                        return True
                    
    def reemplazar_pagina_en_memoria_virtual(self, pagina):
        print("Reemplazando página en memoria virtual...")
        print("la pagina es", pagina)
        for i in range(len(self.memoria_virtual)):
            for j in range(len(self.memoria_virtual[i])):
                print("valor en el espacio: ", self.memoria_virtual[i][j])
                if self.memoria_virtual[i][j] == "":
                    pagina_a_reemplazar = self.memoria_virtual[i][j]
                    self.memoria_virtual[i][j] = pagina
                    print(f"Reemplazando la página {pagina_a_reemplazar} por la página {pagina}.")
                    return
        
            