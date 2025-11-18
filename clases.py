# clases.py
import numpy as np
import variables as var
import random

class Tablero:
    """
    Clase que gestiona el estado del tablero de un jugador en Batalla Naval.
    """
    def __init__(self, id_jugador):
        self.id_jugador = id_jugador
        # Inicializamos las matrices usando el Enum Estado.AGUA
        self.tablero_privado = np.full((var.TAMANO_TABLERO, var.TAMANO_TABLERO), var.Estado.AGUA)
        self.tablero_publico = np.full((var.TAMANO_TABLERO, var.TAMANO_TABLERO), var.Estado.AGUA)
        self.barcos = var.LISTA_BARCOS.copy()
        
        # --- Atributos para IA y Detección de Hundimiento ---
        self.registro_barcos = {}  
        self.barco_id_counter = var.BARCO_ID_INICIO 
        self.objetivo_impactado = None
        self.proximos_disparos = []

    def inicializar_barcos(self):
        """
        Coloca los barcos de forma aleatoria en el tablero privado.
        """
        for eslora in self.barcos:
            colocado = False
            while not colocado:
                x = random.randint(0, var.TAMANO_TABLERO - 1)
                y = random.randint(0, var.TAMANO_TABLERO - 1)
                orientacion = random.choice(["H", "V"])

                if self._puede_colocar(x, y, eslora, orientacion):
                    self._colocar(x, y, eslora, orientacion)
                    colocado = True

    def _puede_colocar(self, x, y, eslora, orientacion):
        """
        Verifica si un barco se puede colocar en las coordenadas dadas sin solaparse.
        """
        if orientacion == "H":
            if x + eslora > var.TAMANO_TABLERO:
                return False
            # Comprobamos contra var.Estado.AGUA
            return np.all(self.tablero_privado[y, x:x+eslora] == var.Estado.AGUA)
        else: # "V"
            if y + eslora > var.TAMANO_TABLERO:
                return False
            return np.all(self.tablero_privado[y:y+eslora, x] == var.Estado.AGUA)

    def _colocar(self, x, y, eslora, orientacion):
        """
        Coloca un barco en el tablero privado y lo registra con un ID único.
        """
        barco_id = self.barco_id_counter
        coordenadas = set()

        if orientacion == "H":
            for i in range(eslora):
                self.tablero_privado[y, x + i] = barco_id
                coordenadas.add((x + i, y))
        else: # "V"
            for i in range(eslora):
                self.tablero_privado[y + i, x] = barco_id
                coordenadas.add((x, y + i))

        self.registro_barcos[barco_id] = {
            'eslora': eslora, 
            'coordenadas': coordenadas, 
            'impactos': set(),
            'hundido': False
        }
        self.barco_id_counter += 1

    def recibir_disparo(self, x, y):
        """
        Registra un disparo, comprueba si es un hundimiento y actualiza el estado.
        Devuelve: (es_impacto, eslora_hundido) o None.
        """
        casilla_id = self.tablero_privado[y, x]

        # 1. CASILLA YA DISPARADA (IMPACTO, FALLO, HUNDIDO)
        # Usamos el Enum para verificar si la casilla ya fue atacada
        if casilla_id in (var.Estado.IMPACTO, var.Estado.FALLO, var.Estado.HUNDIDO):
            return None  
        
        # 2. CASILLA AGUA
        if casilla_id == var.Estado.AGUA:
            self.tablero_privado[y, x] = var.Estado.FALLO
            self.tablero_publico[y, x] = var.Estado.FALLO
            return (False, None) 

        # 3. CASILLA BARCO (Es un ID de barco)
        if casilla_id in self.registro_barcos:
            
            # Marcar el impacto
            self.tablero_privado[y, x] = var.Estado.IMPACTO 
            self.tablero_publico[y, x] = var.Estado.IMPACTO
            
            barco = self.registro_barcos[casilla_id]
            barco['impactos'].add((x, y))

            # Comprobar Hundimiento
            if len(barco['impactos']) == barco['eslora']:
                barco['hundido'] = True
                
                # Marcar todas las coordenadas del barco como HUNDIDO
                for bx, by in barco['coordenadas']:
                    self.tablero_privado[by, bx] = var.Estado.HUNDIDO
                    self.tablero_publico[by, bx] = var.Estado.HUNDIDO
                
                return (True, barco['eslora'])
            
            return (True, None)


    def comprobar_victoria(self):
        """
        Comprueba si todos los barcos del jugador han sido hundidos.
        """
        return all(barco['hundido'] for barco in self.registro_barcos.values())

    def mostrar_tablero(self, tipo_vista='publico'):
        """
        Muestra el tablero en consola con un formato legible y alineado.
        """
        # Mapeo de valores Enums a caracteres
        mapa_simbolos = {
            var.Estado.AGUA: "🌊 ",
            var.Estado.IMPACTO: "💥 ", 
            var.Estado.FALLO: "⚫ ",
            var.Estado.HUNDIDO: "🔥 " 
        }
        
        tablero_a_mostrar = self.tablero_publico if tipo_vista == 'publico' else self.tablero_privado

        # 1. CABECERA DE COLUMNAS
        cabecera_indices = "  " + " ".join([str(n).center(2) for n in range(var.TAMANO_TABLERO)])
        print(cabecera_indices)
        
        # 2. IMPRIMIR FILAS
        for i, fila in enumerate(tablero_a_mostrar):
            linea = f"{str(i).ljust(2)}"
            for celda in fila:
                
                # Mapeo directo para estados (AGUA, IMPACTO, FALLO, HUNDIDO)
                # Al ser IntEnum, celda funciona como clave perfectamente
                simbolo = mapa_simbolos.get(celda)
                
                # LÓGICA DE CORRECCIÓN CRÍTICA:
                if simbolo is None:
                    # Si el valor no es un estado (es un ID de barco intacto),
                    # Solo lo mostramos en el tablero privado.
                    if tipo_vista == 'privado':
                        simbolo = "🚢 "
                    # En el tablero público, este ID no se ha atacado, así que es AGUA.
                    else: 
                        simbolo = "🌊 "
                
                linea += simbolo
            print(linea.strip())