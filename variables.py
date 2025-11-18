# variables.py
from enum import IntEnum

# Tamaño del tablero
TAMANO_TABLERO = 10

# Lista de barcos (esloras)
LISTA_BARCOS = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

# --- CAMBIO: CLASE INTENUM ---
# Heredar de IntEnum permite comparar estos valores directamente con enteros si fuera necesario
class Estado(IntEnum):
    AGUA = 0
    IMPACTO = 2
    FALLO = 3
    HUNDIDO = 4

# ID inicial para los barcos (separado de los estados para evitar colisiones)
BARCO_ID_INICIO = 10