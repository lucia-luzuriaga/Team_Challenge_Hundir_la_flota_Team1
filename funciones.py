# funciones.py
import random
import variables as var
import os

def pedir_coordenadas():
    """
    Pide al jugador que introduzca coordenadas para un disparo.
    Valida que las coordenadas estén dentro del tablero y sean numéricas.

    Devuelve:
        - tuple (int, int): Coordenadas (x, y) validadas.
    """
    while True:
        try:
            x_str = input(f"Coordenada X (columna, 0-{var.TAMANO_TABLERO - 1}): ")
            if not x_str: continue
            x = int(x_str)

            y_str = input(f"Coordenada Y (fila, 0-{var.TAMANO_TABLERO - 1}): ")
            if not y_str: continue
            y = int(y_str)

            if not (0 <= x < var.TAMANO_TABLERO and 0 <= y < var.TAMANO_TABLERO):
                print("Coordenadas fuera del tablero. Inténtalo de nuevo.")
                continue

            return x, y

        except ValueError:
            print(f"Entrada no válida. Introduce números enteros entre 0 y {var.TAMANO_TABLERO - 1}.")
        except IndexError:
            print("Error inesperado con las coordenadas. Inténtalo de nuevo.")


def actualizar_estrategia_ia(tablero_oponente, x, y, es_impacto, es_hundido):
    """
    Actualiza el estado interno de la IA (proximos_disparos) después de un resultado.
    """
    # CASO 1: HUNDIDO
    if es_hundido is not None:
        # Reseteamos el objetivo actual porque este barco ya cayó.
        tablero_oponente.objetivo_impactado = None
        return
        
    # CASO 2: IMPACTO (Pero no hundido)
    if es_impacto:
        tablero_oponente.objetivo_impactado = (x, y)
        
        # Añadimos los 4 vecinos a la cola de posibles objetivos
        posibles_vecinos = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        
        for nx, ny in posibles_vecinos:
            # Verificar límites
            if 0 <= nx < var.TAMANO_TABLERO and 0 <= ny < var.TAMANO_TABLERO:
                # Solo añadimos si es AGUA desconocida (usando Enum)
                # Y evitamos duplicados si ya está en la cola
                if (tablero_oponente.tablero_publico[ny, nx] == var.Estado.AGUA and 
                    (nx, ny) not in tablero_oponente.proximos_disparos):
                    
                    tablero_oponente.proximos_disparos.append((nx, ny))


def disparo_maquina(tablero_oponente):
    """
    Genera coordenadas para el disparo de la máquina.
    Implementa una estrategia inteligente si hay objetivos en cola.
    
    Devuelve:
        - tuple (int, int): Coordenadas (x, y) de disparo.
    """
    # 1. ESTRATEGIA: Barrido de objetivos pendientes
    while tablero_oponente.proximos_disparos:
        # Sacamos el primer objetivo de la cola
        x, y = tablero_oponente.proximos_disparos.pop(0)
        
        # Validación extra: Asegurarnos de que esa casilla sigue siendo válida (AGUA)
        # Usamos Enum para la validación
        if tablero_oponente.tablero_publico[y, x] == var.Estado.AGUA:
            return x, y
        # Si no es válida, el while continúa y saca la siguiente coordenada
    
    # 2. ESTRATEGIA: Disparo Aleatorio (Si no hay objetivos claros)
    while True: 
        x = random.randint(0, var.TAMANO_TABLERO - 1)
        y = random.randint(0, var.TAMANO_TABLERO - 1)
        
        # Solo disparamos donde hay AGUA (desconocido), usando Enum
        if tablero_oponente.tablero_publico[y, x] == var.Estado.AGUA: 
            return x, y

def limpiar_pantalla():
    """
    Limpia la consola de comandos según el sistema operativo.
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')