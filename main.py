from src.cargar_sirenas import cargar_sirenas
from src.graficador import graficar_comparacion_seniales, graficar_tiempo_frecuencia
from src.filtro_paso_banda import aplicar_filtro_paso_banda
from src.generar_FFT_temporales import generar_fft_ventanas
from src.analisis_doppler import analizar_fft_ventanas_temporales, calcular_velocidades_por_ventana
import numpy as np
import os

def menu_principal():
    #comment
    """Muestra el menú principal y retorna la opción seleccionada."""
    print("\n" + "="*70)
    print("ANALISIS DE SENIALES DE SIRENAS - MENU PRINCIPAL")
    print("="*70)
    print("\n1. Analizar Sirenas (Filtrado y gráficos básicos)")
    print("2. Generar FFT en Ventanas Temporales")
    print("3. Análisis Doppler (Calcular velocidad ambulancia)")
    print("4. Salir")
    print("\n" + "-"*70)
    
    while True:
        try:
            opcion = input("\nSelecciona una opción (1-4): ").strip()
            if opcion in ['1', '2', '3', '4']:
                return opcion
            else:
                print("Opción inválida. Intenta de nuevo.")
        except KeyboardInterrupt:
            print("\n\nPrograma cancelado.")
            return '4'


def analizar_fft_ventanas_menu(sirenas):
    """Menú interactivo para análisis FFT en ventanas temporales."""
    print("\n" + "="*70)
    print("GENERAR FFT EN VENTANAS TEMPORALES")
    print("="*70)
    
    # Seleccionar sirena
    print("\nSelecciona la sirena a analizar:")
    print("  1. Sirena 1")
    print("  2. Sirena 2")
    
    while True:
        try:
            opcion_sirena = input("\nOpción (1 o 2): ").strip()
            if opcion_sirena == '1':
                if sirenas['sirena1'] is None:
                    print("Error: Sirena 1 no disponible.")
                    return
                fs = sirenas['sirena1']['fs']
                data = sirenas['sirena1']['data']
                nombre_sirena = 'Sirena1'
                break
            elif opcion_sirena == '2':
                if sirenas['sirena2'] is None:
                    print("Error: Sirena 2 no disponible.")
                    return
                fs = sirenas['sirena2']['fs']
                data = sirenas['sirena2']['data']
                nombre_sirena = 'Sirena2'
                break
            else:
                print("Opción inválida. Intenta de nuevo.")
        except KeyboardInterrupt:
            print("\n\nOperación cancelada.")
            return
    
    # Seleccionar tamaño de ventana
    print("\nSelecciona el tamaño de ventana temporal (en segundos):")
    print("  1. 0.25 segundos (32 ventanas)")
    print("  2. 0.5 segundos (16 ventanas)")
    print("  3. 1.0 segundos (8 ventanas)")
    print("  4. Personalizado")
    
    while True:
        try:
            opcion_ventana = input("\nOpción (1-4): ").strip()
            if opcion_ventana == '1':
                tamaño_ventana_s = 0.25
                break
            elif opcion_ventana == '2':
                tamaño_ventana_s = 0.5
                break
            elif opcion_ventana == '3':
                tamaño_ventana_s = 1.0
                break
            elif opcion_ventana == '4':
                try:
                    tamaño_str = input("Ingresa el tamaño en segundos: ").strip()
                    tamaño_ventana_s = float(tamaño_str)
                    if tamaño_ventana_s <= 0 or tamaño_ventana_s > len(data) / fs:
                        print(f"Error: El tamaño debe estar entre 0 y {len(data) / fs:.2f} segundos.")
                        continue
                    break
                except ValueError:
                    print("Entrada inválida. Intenta de nuevo.")
                    continue
            else:
                print("Opción inválida. Intenta de nuevo.")
        except KeyboardInterrupt:
            print("\n\nOperación cancelada.")
            return
    
    # Generar los gráficos
    print(f"\n[INFO] Generando FFT para {nombre_sirena} con ventanas de {tamaño_ventana_s}s...")
    
    carpeta_graficos = os.path.join(os.path.dirname(__file__), "graficos-creados")
    
    generar_fft_ventanas(
        fs, data,
        tamaño_ventana_s=tamaño_ventana_s,
        nombre_sirena=nombre_sirena,
        color='b',
        carpeta_salida=carpeta_graficos
    )
    
    print(f"\n[OK] FFT generado exitosamente.")
    print(f"Los gráficos se encuentran en: {os.path.abspath(carpeta_graficos)}/")


def analizar_doppler_menu(sirenas):
    """Menú interactivo para análisis Doppler (cálculo de velocidad)."""
    print("\n" + "="*70)
    print("ANÁLISIS DOPPLER - CALCULAR VELOCIDAD DE AMBULANCIA")
    print("="*70)
    
    # Seleccionar sirena
    print("\nSelecciona la sirena a analizar:")
    print("  1. Sirena 1")
    print("  2. Sirena 2")
    
    while True:
        try:
            opcion_sirena = input("\nOpción (1 o 2): ").strip()
            if opcion_sirena == '1':
                if sirenas['sirena1'] is None:
                    print("Error: Sirena 1 no disponible.")
                    return
                fs = sirenas['sirena1']['fs']
                data = sirenas['sirena1']['data']
                nombre_sirena = 'Sirena 1'
                numero_sirena = 1
                break
            elif opcion_sirena == '2':
                if sirenas['sirena2'] is None:
                    print("Error: Sirena 2 no disponible.")
                    return
                fs = sirenas['sirena2']['fs']
                data = sirenas['sirena2']['data']
                nombre_sirena = 'Sirena 2'
                numero_sirena = 2
                break
            else:
                print("Opción inválida. Intenta de nuevo.")
        except KeyboardInterrupt:
            print("\n\nOperación cancelada.")
            return
    
    # Tamaño de ventana por defecto
    tamaño_ventana = 0.5
    
    print(f"\n[INFO] Analizando {nombre_sirena} con ventanas de {tamaño_ventana}s...")
    
    # Generar análisis FFT en ventanas
    info_ventanas = analizar_fft_ventanas_temporales(
        fs, data,
        titulo=f"{nombre_sirena} - FFT en Ventanas Temporales",
        tamaño_ventana_s=tamaño_ventana,
        color='blue',
        archivo_salida=None
    )
    
    # Extraer frecuencias pico
    frecuencias_pico = [info['freq_pico'] for info in info_ventanas]
    
    # Estadísticas
    freq_min = np.min(frecuencias_pico)
    freq_max = np.max(frecuencias_pico)
    freq_promedio = np.mean(frecuencias_pico)
    variacion = freq_max - freq_min
    
    # Análisis de variación de frecuencia
    print("\n" + "-"*70)
    print("ANÁLISIS DE CAMBIO DE FRECUENCIA EN EL TIEMPO")
    print("-"*70)
    print(f"\n{'Ventana':<10} {'Tiempo (s)':<20} {'Frecuencia Pico (Hz)':<25}")
    print("-" * 55)
    
    for info in info_ventanas:
        tiempo_inicio = info['tiempo_inicio']
        tiempo_fin = info['tiempo_fin']
        freq_pico = info['freq_pico']
        print(f"{info['ventana']+1:<10} {tiempo_inicio:.2f}-{tiempo_fin:.2f}s{'':<8} {freq_pico:.2f}")
    
    print("\n" + "-"*70)
    print(f"Frecuencia mínima: {freq_min:.2f} Hz")
    print(f"Frecuencia máxima: {freq_max:.2f} Hz")
    print(f"Frecuencia promedio: {freq_promedio:.2f} Hz")
    print(f"Variación total: {variacion:.2f} Hz ({(variacion/freq_promedio)*100:.1f}%)")
    
    # Explicar efecto Doppler
    print("\n" + "="*70)
    print("EFECTO FÍSICO OBSERVADO: EFECTO DOPPLER")
    print("="*70)
    print(f"""
La variación de frecuencia de {variacion:.2f} Hz indica el efecto Doppler.

¿Qué está ocurriendo?
- Cuando la ambulancia SE ACERCA: la frecuencia AUMENTA a {freq_max:.2f} Hz
- Cuando la ambulancia SE ALEJA: la frecuencia DISMINUYE a {freq_min:.2f} Hz

Esto ocurre porque:
1. Las ondas sonoras se comprimen cuando la fuente se acerca
2. Las ondas sonoras se expanden cuando la fuente se aleja
3. El observador percibe frecuencias diferentes según el movimiento
""")
    
    # Calcular velocidad por ventana
    print("="*70)
    print("CÁLCULO DE VELOCIDAD DE LA AMBULANCIA")
    print("="*70)
    
    velocidades_acerca, velocidades_aleja = calcular_velocidades_por_ventana(frecuencias_pico, freq_promedio)
    
    # Filtrar velocidades válidas (no None)
    v_acerca_validas = [v for v in velocidades_acerca if v is not None]
    v_aleja_validas = [v for v in velocidades_aleja if v is not None]
    
    # Calcular promedios
    v_acerca_promedio = np.mean(v_acerca_validas) if v_acerca_validas else 0
    v_aleja_promedio = np.mean(v_aleja_validas) if v_aleja_validas else 0
    v_promedio_total = (v_acerca_promedio + v_aleja_promedio) / 2 if (v_acerca_validas or v_aleja_validas) else 0
    
    print(f"""
Método: Cálculo de velocidades por ventana individual

Parámetros:
- Velocidad del sonido: 343 m/s (a 20°C)
- Frecuencia de reposo (f₀): {freq_promedio:.2f} Hz
- Frecuencia máxima (acercamiento): {freq_max:.2f} Hz
- Frecuencia mínima (alejamiento): {freq_min:.2f} Hz

Fórmula aplicada por ventana:
- Si f_pico > f_promedio: v = v_sonido × (1 - f_promedio / f_pico)
- Si f_pico < f_promedio: v = v_sonido × (f_promedio / f_pico - 1)

RESULTADOS:
""")
    
    print(f"Velocidad promedio acercándose:  {v_acerca_promedio:.2f} m/s ({v_acerca_promedio * 3.6:.2f} km/h)")
    print(f"Velocidad promedio alejándose:   {v_aleja_promedio:.2f} m/s ({v_aleja_promedio * 3.6:.2f} km/h)")
    print(f"Velocidad promedio total:        {v_promedio_total:.2f} m/s ({v_promedio_total * 3.6:.2f} km/h)")
    
    print("\n" + "="*70)


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
    
    # Menú principal
    while True:
        opcion = menu_principal()
        
        if opcion == '1':
            # ============================================================
            # FILTRADO PASO BANDA - AUTOMÁTICO
            # ============================================================
            print("CONFIGURACION DEL FILTRO PASO BANDA")
            print("="*70)
            
            # Filtros predeterminados
            freq_min1 = 940.0
            freq_max1 = 1050.0
            freq_min2 = 1200.0
            freq_max2 = 1500.0
            
            print(f"\n[OK] Filtro Sirena 1: {freq_min1:.1f} Hz - {freq_max1:.1f} Hz (automatico)")
            print(f"[OK] Filtro Sirena 2: {freq_min2:.1f} Hz - {freq_max2:.1f} Hz (automatico)")
            
            # Aplicar filtros independientes a cada sirena
            print(f"\nAplicando filtros...")
            data1_filtrada = aplicar_filtro_paso_banda(data1, fs1, freq_min1, freq_max1)
            data2_filtrada = aplicar_filtro_paso_banda(data2, fs2, freq_min2, freq_max2)
            print(f"[OK] Filtros aplicados")
            
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
        
        elif opcion == '2':
            analizar_fft_ventanas_menu(sirenas)
        
        elif opcion == '3':
            analizar_doppler_menu(sirenas)
        
        elif opcion == '4':
            print("\n[OK] Programa finalizado.")
            break


if __name__ == "__main__":
    main()