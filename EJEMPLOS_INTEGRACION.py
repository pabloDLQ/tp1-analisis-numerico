"""
Ejemplo de cómo integrar el análisis de Item 2 en main.py

Este archivo muestra 3 formas de integrar el análisis Doppler:
1. Forma simple (copiar-pegar)
2. Forma modular (usar funciones)
3. Forma completa (análisis exhaustivo)
"""

# ============================================================================
# OPCIÓN 1: FORMA SIMPLE - Copiar en main.py después del análisis filtros
# ============================================================================

def item2_simple():
    """
    Código simple para agregar al final de main()
    """
    
    codigo = '''
    # ============================================================
    # ITEM 2: ANALISIS DE EFECTO DOPPLER
    # ============================================================
    print("\\n" + "="*70)
    print("ITEM 2: FFT EN VENTANAS TEMPORALES - EFECTO DOPPLER")
    print("="*70)
    
    from src.analisis_doppler import analizar_fft_ventanas_temporales, calcular_velocidad_ambulancia
    import numpy as np
    
    # Generar gráfico FFT en ventanas de 0.5 segundos
    archivo_ventanas = os.path.join(carpeta_graficos, "Sirena1_FFT_Ventanas_0.5s.png")
    info_ventanas = analizar_fft_ventanas_temporales(
        fs1, data1,
        titulo="Sirena 1 - FFT en Ventanas Temporales",
        tamaño_ventana_s=0.5,
        color='blue',
        archivo_salida=archivo_ventanas
    )
    
    # Análisis de frecuencias
    frecuencias = [info['freq_pico'] for info in info_ventanas]
    freq_min = np.min(frecuencias)
    freq_max = np.max(frecuencias)
    freq_promedio = np.mean(frecuencias)
    
    print(f"\\nFrequencia mínima: {freq_min:.2f} Hz")
    print(f"Frequencia máxima: {freq_max:.2f} Hz")
    print(f"Variación: {freq_max - freq_min:.2f} Hz")
    
    # Calcular velocidad
    velocidades = calcular_velocidad_ambulancia(freq_min, freq_max, freq_promedio)
    print(f"\\nVelocidad promedio: {velocidades['v_promedio_kmh']:.2f} km/h")
    print(f"Gráfico guardado: {archivo_ventanas}")
    '''
    
    return codigo


# ============================================================================
# OPCIÓN 2: FUNCIÓN MODULAR - Copiar en main.py
# ============================================================================

def realizar_item2(fs, data, carpeta_graficos):
    """
    Función para realizar análisis Item 2.
    
    Uso en main():
        resultado = realizar_item2(fs1, data1, carpeta_graficos)
        print(resultado['velocidad_kmh'])
    """
    from src.analisis_doppler import analizar_fft_ventanas_temporales, calcular_velocidad_ambulancia
    import numpy as np
    import os
    
    # Generar análisis
    archivo_ventanas = os.path.join(carpeta_graficos, "Sirena1_FFT_Ventanas_0.5s.png")
    info_ventanas = analizar_fft_ventanas_temporales(
        fs, data,
        titulo="Sirena 1 - FFT en Ventanas Temporales",
        tamaño_ventana_s=0.5,
        color='blue',
        archivo_salida=archivo_ventanas
    )
    
    # Extraer información
    frecuencias = [info['freq_pico'] for info in info_ventanas]
    freq_min = np.min(frecuencias)
    freq_max = np.max(frecuencias)
    freq_promedio = np.mean(frecuencias)
    
    # Calcular velocidad
    velocidades = calcular_velocidad_ambulancia(freq_min, freq_max, freq_promedio)
    
    return {
        'archivo': archivo_ventanas,
        'info_ventanas': info_ventanas,
        'freq_min': freq_min,
        'freq_max': freq_max,
        'freq_promedio': freq_promedio,
        'variacion': freq_max - freq_min,
        'velocidad_ms': velocidades['v_promedio_ms'],
        'velocidad_kmh': velocidades['v_promedio_kmh'],
    }


# ============================================================================
# OPCIÓN 3: VERSIÓN COMPLETA PARA main.py
# ============================================================================

def codigo_completo_para_main_py():
    """
    Código completo y optimizado para agregar a main()
    """
    
    codigo = '''
def main():
    # ... código existente del filtrado ...
    
    print(f"\\n[OK] Los graficos han sido guardados en '{carpeta_graficos}'")
    
    # ============================================================
    # ITEM 2: ANÁLISIS DE FFT EN VENTANAS TEMPORALES (EFECTO DOPPLER)
    # ============================================================
    print("\\n" + "="*70)
    print("ITEM 2: ANÁLISIS DE FFT EN VENTANAS TEMPORALES - EFECTO DOPPLER")
    print("="*70)
    
    from src.analisis_doppler import analizar_fft_ventanas_temporales, calcular_velocidad_ambulancia
    import numpy as np
    
    # Parámetro: tamaño de ventana en segundos
    tamaño_ventana = 0.5
    
    # Generar gráfico FFT en ventanas
    print(f"\\nGenerando gráfico FFT en ventanas de {tamaño_ventana}s...")
    archivo_ventanas = os.path.join(carpeta_graficos, f"Sirena1_FFT_Ventanas_{tamaño_ventana}s.png")
    
    info_ventanas = analizar_fft_ventanas_temporales(
        fs1, data1,
        titulo="Sirena 1 - FFT en Ventanas Temporales",
        tamaño_ventana_s=tamaño_ventana,
        color='blue',
        archivo_salida=archivo_ventanas
    )
    
    # Análisis de cambio de frecuencia
    frecuencias_pico = [info['freq_pico'] for info in info_ventanas]
    freq_min = np.min(frecuencias_pico)
    freq_max = np.max(frecuencias_pico)
    freq_promedio = np.mean(frecuencias_pico)
    variacion = freq_max - freq_min
    
    print(f"\\n--- Análisis de Variación de Frecuencia ---")
    print(f"Número de ventanas: {len(info_ventanas)}")
    print(f"Frecuencia mínima:  {freq_min:.2f} Hz")
    print(f"Frecuencia máxima:  {freq_max:.2f} Hz")
    print(f"Frecuencia promedio: {freq_promedio:.2f} Hz")
    print(f"Variación total: {variacion:.2f} Hz ({(variacion/freq_promedio)*100:.1f}%)")
    
    # Explicar efecto Doppler
    print(f"\\n--- Efecto Físico: EFECTO DOPPLER ---")
    print(f"La variación de {variacion:.2f} Hz indica cambios de frecuencia en el tiempo.")
    print(f"Esto ocurre porque:")
    print(f"  • Acercamiento (0-4.5s): Frecuencia SUBE a {freq_max:.2f} Hz")
    print(f"  • Alejamiento (4.5-8.0s): Frecuencia BAJA a {freq_min:.2f} Hz")
    print(f"\\nEste es el efecto Doppler: cambio de frecuencia por movimiento relativo")
    
    # Calcular velocidad de ambulancia
    print(f"\\n--- Cálculo de Velocidad de la Ambulancia ---")
    
    velocidades = calcular_velocidad_ambulancia(freq_min, freq_max, freq_promedio)
    
    print(f"Usando fórmula de Doppler:")
    print(f"  f = f₀ × v_sonido / (v_sonido ± v_ambulancia)")
    print(f"\\nResultados:")
    print(f"  Acercándose: {velocidades['v_acerca_ms']:.2f} m/s ({velocidades['v_acerca_kmh']:.2f} km/h)")
    print(f"  Alejándose:  {velocidades['v_aleja_ms']:.2f} m/s ({velocidades['v_aleja_kmh']:.2f} km/h)")
    print(f"  Promedio:    {velocidades['v_promedio_ms']:.2f} m/s ({velocidades['v_promedio_kmh']:.2f} km/h)")
    
    print(f"\\n" + "="*70)
    print(f"Gráfico guardado: {archivo_ventanas}")
    print("="*70)


if __name__ == "__main__":
    main()
    '''
    
    return codigo


# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("EJEMPLOS DE INTEGRACIÓN:")
    print("\n1. FORMA SIMPLE:")
    print("-" * 50)
    print(item2_simple())
    
    print("\n2. FORMA MODULAR:")
    print("-" * 50)
    print("from src.analisis_doppler import calcular_velocidad_ambulancia")
    print("resultado = realizar_item2(fs1, data1, carpeta_graficos)")
    print("print(f'Velocidad: {resultado[\"velocidad_kmh\"]:.2f} km/h')")
    
    print("\n3. PARA VER CÓDIGO COMPLETO:")
    print("-" * 50)
    print(codigo_completo_para_main_py())
