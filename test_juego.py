# test_juego.py
import unittest
import numpy as np
import clases
import variables as var

class TestTablero(unittest.TestCase):

    def setUp(self):
        """
        Este método se ejecuta AUTOMÁTICAMENTE antes de CADA test.
        Nos asegura que siempre empezamos con un tablero limpio.
        """
        self.tablero = clases.Tablero(id_jugador="TestPlayer")

    def test_inicializacion_tablero(self):
        """Verifica que el tablero se crea vacío (todo AGUA)"""
        # Comprobamos que todas las celdas son Estado.AGUA
        self.assertTrue(np.all(self.tablero.tablero_privado == var.Estado.AGUA))
        self.assertEqual(len(self.tablero.registro_barcos), 0)

    def test_colocacion_barco_valida(self):
        """Verifica que se puede colocar un barco en coordenadas válidas"""
        # Intentamos colocar un barco de eslora 3 en (0,0) Horizontal
        posible = self.tablero._puede_colocar(0, 0, 3, "H")
        self.assertTrue(posible, "Debería ser posible colocar el barco aquí")

        # Lo colocamos de verdad
        self.tablero._colocar(0, 0, 3, "H")
        
        # Verificamos que en (0,0), (1,0) y (2,0) ya no hay AGUA
        # Nota: Usamos var.Estado.AGUA para comparar
        self.assertNotEqual(self.tablero.tablero_privado[0, 0], var.Estado.AGUA)
        self.assertNotEqual(self.tablero.tablero_privado[0, 1], var.Estado.AGUA)
        self.assertNotEqual(self.tablero.tablero_privado[0, 2], var.Estado.AGUA)

    def test_colocacion_fuera_limites(self):
        """Verifica que NO deja colocar barcos que se salen del mapa"""
        # Barco de 2 en la posición (9, 9) Horizontal -> Se saldría por la derecha
        posible = self.tablero._puede_colocar(9, 9, 2, "H")
        self.assertFalse(posible, "No debería dejar colocar un barco fuera del límite")

    def test_colocacion_solapada(self):
        """Verifica que NO deja poner un barco encima de otro"""
        # 1. Colocamos un barco primero
        self.tablero._colocar(0, 0, 3, "H") # Ocupa (0,0), (1,0), (2,0)

        # 2. Intentamos poner otro que cruce en (1,0) Vertical
        posible = self.tablero._puede_colocar(1, 0, 3, "V") 
        self.assertFalse(posible, "No debería permitir solapamiento de barcos")

    def test_disparo_agua(self):
        """Verifica que disparar al agua devuelve (False, None) y marca FALLO"""
        x, y = 5, 5
        resultado = self.tablero.recibir_disparo(x, y)
        
        # Esperamos: (False, None) -> (No impacto, No hundido)
        self.assertEqual(resultado, (False, None))
        
        # Verificamos que el tablero marque FALLO
        self.assertEqual(self.tablero.tablero_privado[y, x], var.Estado.FALLO)

    def test_disparo_impacto_sin_hundir(self):
        """Verifica que disparar a un barco devuelve (True, None)"""
        # Colocamos barco de 2 posiciones en (0,0) y (1,0)
        self.tablero._colocar(0, 0, 2, "H")
        
        # Disparamos solo a la primera parte (0,0)
        resultado = self.tablero.recibir_disparo(0, 0)
        
        # Esperamos: (True, None) -> (Impacto, Aún no hundido)
        self.assertEqual(resultado, (True, None))
        
        # Verificamos que el tablero marque IMPACTO
        self.assertEqual(self.tablero.tablero_privado[0, 0], var.Estado.IMPACTO)

    def test_hundir_barco(self):
        """Verifica la lógica completa de hundimiento"""
        # Colocamos un barco pequeño de eslora 2
        self.tablero._colocar(0, 0, 2, "H") # Ocupa (0,0) y (1,0)
        
        # 1. Primer disparo (Impacto)
        self.tablero.recibir_disparo(0, 0)
        
        # 2. Segundo disparo (Hundido)
        resultado = self.tablero.recibir_disparo(1, 0)
        
        # Esperamos: (True, 2) -> (Impacto, Eslora del hundido es 2)
        es_impacto, eslora = resultado
        self.assertTrue(es_impacto)
        self.assertEqual(eslora, 2)
        
        # Verificamos que AMBAS celdas ahora son HUNDIDO
        self.assertEqual(self.tablero.tablero_privado[0, 0], var.Estado.HUNDIDO)
        self.assertEqual(self.tablero.tablero_privado[0, 1], var.Estado.HUNDIDO)

    def test_condicion_victoria(self):
        """Verifica que ganamos cuando todos los barcos están hundidos"""
        # Colocamos SOLO UN barco para el test
        self.tablero._colocar(5, 5, 1, "H")
        
        # Al principio no hemos ganado
        self.assertFalse(self.tablero.comprobar_victoria())
        
        # Hundimos el único barco
        self.tablero.recibir_disparo(5, 5)
        
        # Ahora deberíamos haber ganado
        self.assertTrue(self.tablero.comprobar_victoria())

if __name__ == '__main__':
    print("Ejecutando baterías de pruebas (Versión Enum)...")
    unittest.main()