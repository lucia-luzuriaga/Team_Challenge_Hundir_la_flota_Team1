# 🚢 Batalla Naval (Battleship Game)  


### Este proyecto implementa el clásico juego de Batalla Naval con una estructura orientada a objetos (OOP) y utilizando la biblioteca numpy para una gestión eficiente del tablero. Esta versión incluye lógica de IA inteligente y detección precisa de hundimientos.  




## 💾 Estructura del Proyecto  


El código está organizado en archivos modulares:  
- main.py: Punto de entrada y orquestación principal del juego.  
- clases.py: Contiene la clase Tablero para la gestión de los estados del juego (colocación, disparos, detección de hundimiento).  
- funciones.py: Contiene funciones utilitarias como pedir_coordenadas y la lógica de la IA inteligente.  
- variables.py: Almacena las constantes del juego (tamaño del tablero, esloras de los barcos y marcadores de estado).requirements.txt: Lista de dependencias necesarias.

## 🚀 Guía de Instalación y Ejecución  
Sigue estos pasos para descargar el repositorio, instalar las dependencias necesarias y empezar a jugar.  


Paso 1: Clonar el Repositorio  


Abre tu terminal y clona el proyecto de GitHub: git clone [URL_DEL_REPOSITORIO]  | cd Hundir-La-Flota  
(Asegúrate de reemplazar [URL_DEL_REPOSITORIO] con la URL real de tu proyecto).  


Paso 2: Configurar el Entorno Virtual (venv)  


Es una buena práctica de Python aislar las dependencias del proyecto.  


Crear el Entorno Virtual: python3 -m venv .venv


Activar el Entorno : source .venv/bin/activate


(Tu terminal debería mostrar (.venv) al inicio del prompt, indicando que está activo.)  


Paso 3: Instalar DependenciasInstala todas las bibliotecas necesarias (principalmente numpy) listadas 
en requirements.txt: pip install -r requirements.txt  


Paso 4: ¡Ejecutar el Juego!  
Una vez que las dependencias estén instaladas, puedes iniciar el juego directamente: python3 main.py  




## 🕹️ Reglas y Símbolos del Juego   
Símbolo |Significado |Estado   
🌊AguaCasilla no disparada   
🚢BarcoCasilla de barco intacto   
💥ImpactoBarco tocado (la IA intentará hundirlo)  
🔥HundidoBarco completamente destruido  
⚫FalloDisparo en agua  
El juego te guiará en cada turno. Si logras un Impacto (💥) o Hundes (🔥) un barco, vuelves a disparar.  
# ¡Mucha Suerte!
