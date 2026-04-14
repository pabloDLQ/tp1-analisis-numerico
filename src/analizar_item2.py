"""
Script para generar gráficos FFT en ventanas temporales y analizar efecto Doppler.
Ejecutar: python -m src.analizar_item2
"""

from src.cargar_sirenas import cargar_sirenas
from src.analisis_doppler import analizar_fft_ventanas_temporales, calcular_velocidad_ambulancia
import numpy as np
import os

def main():
    # Crear carpeta de gráficos
    carpeta_graficos = os.path.join(os.path.dirname(__file__), "..", "graficos-creados")
    if not os.path.exists(carpeta_graficos):
        os.makedirs(carpeta_graficos)
    
    # Cargar sirenas
    sirenas = cargar_sirenas()
    
    if sirenas['sirena1'] is None:
        print("Error: No se pudo cargar Sirena 1")
        return
    
    fs1 = sirenas['sirena1']['fs']
    data1 = sirenas['sirena1']['data']
    
    print("="*70)
    print("ITEM 2: ANÁLISIS DE FFT EN VENTANAS TEMPORALES (EFECTO DOPPLER)")
    print("="*70)
    print(f"\nSirena 1: fs = {fs1} Hz, duración = {len(data1)/fs1:.2f} s\n")
    
    # Generar gráfico FFT en ventanas de 0.5 segundos
    tamaño_ventana = 0.5
    archivo_ventanas = os.path.join(carpeta_graficos, "Sirena1_FFT_Ventanas_0.5s.png")
    
    print(f"Generando gráfico FFT en ventanas de {tamaño_ventana} segundos...")
    info_ventanas = analizar_fft_ventanas_temporales(
        fs1, data1,
        titulo="Sirena 1 - FFT en Ventanas Temporales",
        tamaño_ventana_s=tamaño_ventana,
        color='blue',
        archivo_salida=archivo_ventanas
    )
    
    # Análisis de variación de frecuencia
    print("\n" + "-"*70)
    print("ANÁLISIS DE CAMBIO DE FRECUENCIA EN EL TIEMPO")
    print("-"*70)
    print(f"\n{'Ventana':<10} {'Tiempo (s)':<20} {'Frecuencia Pico (Hz)':<25}")
    print("-" * 55)
    
    frecuencias_pico = []
    for info in info_ventanas:
        print(f"{info['ventana']+1:<10} {info['tiempo_inicio']:.2f}-{info['tiempo_fin']:.2f}s{'':<8} {info['freq_pico']:.2f}")
        frecuencias_pico.append(info['freq_pico'])
    
    # Estadísticas
    freq_min = np.min(frecuencias_pico)
    freq_max = np.max(frecuencias_pico)
    freq_promedio = np.mean(frecuencias_pico)
    variacion = freq_max - freq_min
    
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
    
    # Calcular velocidad
    print("="*70)
    print("CÁLCULO DE VELOCIDAD DE LA AMBULANCIA")
    print("="*70)
    
    velocidades = calcular_velocidad_ambulancia(freq_min, freq_max, freq_promedio)
    
    print(f"""
Fórmula de Doppler utilizada:
- Acercamiento: f_max = f₀ × v_sonido / (v_sonido - v_ambulancia)
- Alejamiento: f_min = f₀ × v_sonido / (v_sonido + v_ambulancia)

Parámetros:
- Velocidad del sonido: {velocidades['v_sonido']} m/s (a 20°C)
- Frecuencia de reposo (f₀): {freq_promedio:.2f} Hz
- Frecuencia máxima (acercamiento): {freq_max:.2f} Hz
- Frecuencia mínima (alejamiento): {freq_min:.2f} Hz

RESULTADOS:
""")
    
    print(f"Velocidad acercándose: {velocidades['v_acerca_ms']:.2f} m/s ({velocidades['v_acerca_kmh']:.2f} km/h)")
    print(f"Velocidad alejándose:  {velocidades['v_aleja_ms']:.2f} m/s ({velocidades['v_aleja_kmh']:.2f} km/h)")
    print(f"Velocidad promedio:    {velocidades['v_promedio_ms']:.2f} m/s ({velocidades['v_promedio_kmh']:.2f} km/h)")
    
    print("\n" + "="*70)
    print(f"Gráfico generado: {archivo_ventanas}")
    print("="*70)


if __name__ == "__main__":
    main()
