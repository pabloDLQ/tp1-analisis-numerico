from src.cargar_sirenas import cargar_sirenas
from src.graficador import graficar_comparacion_seniales, graficar_tiempo_frecuencia
from src.filtro_paso_banda import aplicar_filtro_paso_banda
import os

def main():
    # Crear la carpeta de graficos si no existe
    carpeta_graficos = os.path.join(os.path.dirname(__file__), "graficos-creados")
    if not os.path.exists(carpeta_graficos):
        os.makedirs(carpeta_graficos)
    
    # Cargar las sirenas
    sirenas = cargar_sirenas()

    # Verificar que ambas se cargaron correctamente
    if sirenas['sirena1'] is None or sirenas['sirena2'] is None:
        print("Error: no se pudieron cargar los archivos.")
        return

    # Extraer datos
    fs1, data1 = sirenas['sirena1']['fs'], sirenas['sirena1']['data']
    fs2, data2 = sirenas['sirena2']['fs'], sirenas['sirena2']['data']

    # Mostrar informacion basica
    print("\n--- Informacion de las senales ---")
    print(f"Sirena 1: fs = {fs1} Hz, duracion = {len(data1)/fs1:.2f} s")
    print(f"Sirena 2: fs = {fs2} Hz, duracion = {len(data2)/fs2:.2f} s")
    print("\n" + "="*70 + "\n")
    
    # ============================================================
    # FILTRADO PASO BANDA - CON ENTRADA DEL USUARIO
    # ============================================================
    print("CONFIGURACION DEL FILTRO PASO BANDA")
    print("="*70)
    
    nyquist1 = fs1 / 2
    nyquist2 = fs2 / 2
    
    # --- FILTRO PARA SIRENA 1 ---
    print(f"\n*** FILTRO PARA SIRENA 1 ***")
    print(f"Opciones disponibles:")
    print(f"  1. PREDETERMINADA: 940 Hz - 1050 Hz")
    print(f"  2. PERSONALIZADA: Ingresa tus propios valores")
    
    while True:
        try:
            opcion1 = input(f"\nSelecciona opcion (1 o 2): ").strip()
            if opcion1 == "1":
                freq_min1 = 940.0
                freq_max1 = 1050.0
                print(f"\u2713 Seleccionado: PREDETERMINADA (940 - 1050 Hz)")
                break
            elif opcion1 == "2":
                print(f"\nFrecuencia minima y maxima permitidas: 1 Hz - {nyquist1:.1f} Hz")
                
                while True:
                    try:
                        freq_min1 = float(input(f"Frecuencia minima Sirena 1 (1-{nyquist1:.1f}): "))
                        if 1 <= freq_min1 <= nyquist1:
                            break
                        else:
                            print(f"Error: Debes ingresar un valor entre 1 y {nyquist1:.1f}")
                    except ValueError:
                        print("Error: Ingresa un numero valido")
                
                while True:
                    try:
                        freq_max1 = float(input(f"Frecuencia maxima Sirena 1 ({freq_min1:.1f}-{nyquist1:.1f}): "))
                        if freq_min1 <= freq_max1 <= nyquist1:
                            break
                        else:
                            print(f"Error: Debes ingresar un valor entre {freq_min1:.1f} y {nyquist1:.1f}")
                    except ValueError:
                        print("Error: Ingresa un numero valido")
                
                print(f"\u2713 Seleccionado: PERSONALIZADA")
                break
            else:
                print("Error: Selecciona 1 o 2")
        except KeyboardInterrupt:
            print("\n[!] Cancelado por el usuario")
            return
    
    print(f"\u2713 Filtro Sirena 1: {freq_min1:.1f} Hz - {freq_max1:.1f} Hz")
    
    # --- FILTRO PARA SIRENA 2 ---
    print(f"\n*** FILTRO PARA SIRENA 2 ***")
    print(f"Frecuencia minima y maxima permitidas: 1 Hz - {nyquist2:.1f} Hz")
    
    while True:
        try:
            freq_min2 = float(input(f"Frecuencia minima Sirena 2 (1-{nyquist2:.1f}): "))
            if 1 <= freq_min2 <= nyquist2:
                break
            else:
                print(f"Error: Debes ingresar un valor entre 1 y {nyquist2:.1f}")
        except ValueError:
            print("Error: Ingresa un numero valido")
    
    while True:
        try:
            freq_max2 = float(input(f"Frecuencia maxima Sirena 2 ({freq_min2:.1f}-{nyquist2:.1f}): "))
            if freq_min2 <= freq_max2 <= nyquist2:
                break
            else:
                print(f"Error: Debes ingresar un valor entre {freq_min2:.1f} y {nyquist2:.1f}")
        except ValueError:
            print("Error: Ingresa un numero valido")
    
    print(f"✓ Filtro Sirena 2: {freq_min2:.1f} Hz - {freq_max2:.1f} Hz")
    
    # Aplicar filtros independientes a cada sirena
    print(f"\nAplicando filtros...")
    data1_filtrada = aplicar_filtro_paso_banda(data1, fs1, freq_min1, freq_max1)
    data2_filtrada = aplicar_filtro_paso_banda(data2, fs2, freq_min2, freq_max2)
    print(f"✓ Filtros aplicados")
    
    print("\n" + "="*70 + "\n")
    
    # ============================================================
    # GRAFICOS
    # ============================================================
    print("\n" + "="*70)
    print("GENERANDO GRAFICOS")
    print("="*70)
    
    # Graficar seniales originales
    archivo_sirena1_original = os.path.join(carpeta_graficos, "Sirena1_Original.png")
    archivo_sirena2_original = os.path.join(carpeta_graficos, "Sirena2_Original.png")
    
    graficar_tiempo_frecuencia(fs1, data1, 
                               titulo="Sirena 1 - Original",
                               color='blue', 
                               archivo_salida=archivo_sirena1_original)
    
    graficar_tiempo_frecuencia(fs2, data2, 
                               titulo="Sirena 2 - Original",
                               color='red', 
                               archivo_salida=archivo_sirena2_original)
    
    # Graficar seniales filtradas
    archivo_sirena1_filtrada = os.path.join(carpeta_graficos, "Sirena1_Filtrada.png")
    archivo_sirena2_filtrada = os.path.join(carpeta_graficos, "Sirena2_Filtrada.png")
    
    graficar_tiempo_frecuencia(fs1, data1_filtrada, 
                               titulo="Sirena 1 - Filtro Paso Banda",
                               color='blue', 
                               archivo_salida=archivo_sirena1_filtrada)
    
    graficar_tiempo_frecuencia(fs2, data2_filtrada, 
                               titulo="Sirena 2 - Filtro Paso Banda",
                               color='red', 
                               archivo_salida=archivo_sirena2_filtrada)
    
    print(f"\n[OK] Los graficos han sido guardados en la carpeta '{carpeta_graficos}'")
    print(f"\nCada archivo contiene:")
    print(f"  - Grafico en Dominio del Tiempo")
    print(f"  - FFT Completa (0 - Frecuencia Nyquist)")
    print(f"  - FFT Acotada [0 - 5000 Hz]")
    print(f"\nArchivos generados:")
    print(f"  - {archivo_sirena1_original}")
    print(f"  - {archivo_sirena2_original}")
    print(f"  - {archivo_sirena1_filtrada}")
    print(f"  - {archivo_sirena2_filtrada}")


if __name__ == "__main__":
    main()