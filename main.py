# main.py
import clases
import funciones
import time

def run_game():
    """
    Función principal que orquesta el juego de Batalla Naval.
    """
    funciones.limpiar_pantalla() # Limpieza inicial
    print("="*40)
    print("🚢  ¡Bienvenido a Batalla Naval!  💥")
    print("="*40)
    print("Reglas: 🚢 Barco | 💥 Impacto | ⚫ Fallo | 🔥 Hundido")
    time.sleep(2) # Dejar leer las reglas antes de limpiar

    # --- FASE 1: CONFIGURACIÓN DEL JUGADOR ---
    tablero_jugador = None
    
    while True:
        funciones.limpiar_pantalla() # <--- LIMPIEZA 1: Borra intentos anteriores
        print("="*40)
        print("      CONFIGURACIÓN DE FLOTA      ")
        print("="*40)
        
        tablero_jugador = clases.Tablero(id_jugador='Player')
        print("\nGenerando distribución aleatoria de tu flota...")
        tablero_jugador.inicializar_barcos()
        
        print("\n--- VISTA PREVIA DE TU FLOTA ---")
        tablero_jugador.mostrar_tablero(tipo_vista='privado')
        
        confirmacion = input("\n¿Te gusta esta distribución? (s/n): ").lower()
        
        if confirmacion == 's':
            print("¡Excelente! Flota confirmada y lista para el combate.")
            time.sleep(1)
            break
        else:
            print("Reorganizando barcos...")
            time.sleep(0.5)

    # --- FASE 2: CONFIGURACIÓN DE LA IA ---
    funciones.limpiar_pantalla()
    print("\nDesplegando flota enemiga...")
    tablero_maquina = clases.Tablero(id_jugador='AI')
    tablero_maquina.inicializar_barcos()
    time.sleep(1)
    print("¡La IA está lista! Que comience la batalla.")
    time.sleep(1.5)

    # --- FASE 3: BUCLE DE JUEGO ---
    turno = 'Player'

    while True:
        funciones.limpiar_pantalla() # <--- LIMPIEZA 2: ¡Aquí está la magia!
        # Cada turno empieza con la pantalla limpia mostrando solo la info actual
        
        print("="*40)
        print(f"        TURNO: {turno.upper()}        ")
        print("="*40)
        
        if turno == 'Player':
            # Mostrar estado actual
            print("\n[TU FLOTA]")
            tablero_jugador.mostrar_tablero(tipo_vista='privado')
            print("\n[RADAR ENEMIGO]")
            tablero_maquina.mostrar_tablero(tipo_vista='publico')

            # Pedir coordenadas y disparar
            while True:
                x, y = funciones.pedir_coordenadas()
                resultado = tablero_maquina.recibir_disparo(x, y) 

                if resultado is None:
                    print("⚠️ Ya has disparado ahí. ¡Concéntrate, almirante!")
                else:
                    break

            es_impacto, es_hundido = resultado

            # Feedback del disparo del jugador
            if es_hundido is not None:
                funciones.limpiar_pantalla() # Limpiamos para dar énfasis al evento importante
                print("\n" + "🔥"*20)
                print(f"¡BOOM! Has HUNDIDO un barco enemigo (Eslora: {es_hundido})!")
                print("🔥"*20)
                
                if tablero_maquina.comprobar_victoria():
                    print("\n" + "⭐"*20)
                    print(" ¡VICTORIA! HAS DERROTADO A LA IA ")
                    print("⭐"*20)
                    tablero_maquina.mostrar_tablero(tipo_vista='privado')
                    break
                print("\n¡Tienes un disparo extra por hundimiento!") 
                time.sleep(3) # Pausa para celebrar antes de limpiar
            elif es_impacto:
                print("\n💥 ¡IMPACTO! Buen tiro. Vuelves a disparar.")
                time.sleep(1.5) # Pausa para ver el impacto
            else:
                print("\n💧 ¡AGUA! Fallaste.")
                print("Cambio de turno...")
                time.sleep(1.5) # Pausa para leer el fallo
                turno = 'AI'

        else: # Turno de la IA
            print("\n🤖 La IA está calculando coordenadas...")
            time.sleep(1.5)

            while True:
                x, y = funciones.disparo_maquina(tablero_jugador)
                print(f"La IA dispara a ({x}, {y})...")
                time.sleep(1)
                
                resultado = tablero_jugador.recibir_disparo(x, y)
                
                if resultado is not None: 
                    es_impacto, es_hundido = resultado
                    funciones.actualizar_estrategia_ia(tablero_jugador, x, y, es_impacto, es_hundido)
                    
                    if es_hundido is not None:
                        print(f"🔥 ¡MALDICIÓN! La IA ha HUNDIDO tu barco (Eslora: {es_hundido})!")
                        if tablero_jugador.comprobar_victoria():
                            print("\n💀 GAME OVER. La flota ha sido destruida.")
                            print("Así quedaron los barcos enemigos:")
                            tablero_maquina.mostrar_tablero(tipo_vista='privado')
                            return 
                        
                        print("⚡ La IA dispara de nuevo...")
                        time.sleep(2.5) 
                    elif es_impacto:
                        print("💥 ¡NOS HAN DADO! Impacto recibido.")
                        print("⚡ La IA recarga...")
                        time.sleep(2)
                    else:
                        print("🌊 ¡AGUA! El disparo enemigo cayó al mar.")
                        time.sleep(2)
                        turno = 'Player'
                        break 

if __name__ == '__main__':
    run_game()