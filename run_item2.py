"""
Punto de entrada para ejecutar análisis del Item 2
Este script proporciona formas convenientes de ejecutar los análisis
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(__file__))

def mostrar_menu():
    print("\n" + "="*70)
    print("ANÁLISIS DEL ITEM 2 - EFECTO DOPPLER")
    print("="*70)
    print("\nOpciones disponibles:")
    print("  1. Analizar Item 2 completo")
    print("  2. Comparar FFT completa vs ventanas")
    print("  3. Salir")
    print("\nEscribe el número de la opción: ", end="")

def main():
    while True:
        mostrar_menu()
        opcion = input().strip()
        
        if opcion == "1":
            print("\nEjecutando análisis del Item 2...")
            from src.analizar_item2 import main as analizar_item2
            analizar_item2()
            
        elif opcion == "2":
            print("\nGenerando comparativa...")
            from src.comparar_metodos_fft import main as comparar_metodos
            comparar_metodos()
            
        elif opcion == "3":
            print("Saliendo...")
            break
        else:
            print("Opción inválida. Intenta de nuevo.\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Permitir ejecutar con argumentos: python run_item2.py 1 o 2
        if sys.argv[1] == "1":
            from src.analizar_item2 import main as analizar_item2
            analizar_item2()
        elif sys.argv[1] == "2":
            from src.comparar_metodos_fft import main as comparar_metodos
            comparar_metodos()
    else:
        main()
