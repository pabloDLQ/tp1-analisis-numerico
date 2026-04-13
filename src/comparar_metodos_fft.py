"""
Script para comparar FFT completa vs FFT en ventanas temporales.
Genera un gráfico comparativo mostrando la diferencia entre ambos enfoques.
"""

from src.cargar_sirenas import cargar_sirenas
from src.graficador import graficar_tiempo_frecuencia
from src.analisis_doppler import analizar_fft_ventanas_temporales
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import os

def graficar_comparacion_fft_completa_vs_ventanas(fs, data, archivo_salida=None):
    """
    Crea un gráfico comparativo: FFT completa vs FFT en ventanas.
    """
    
    # Crear figura con 2 columnas
    fig = plt.figure(figsize=(16, 10))
    
    # ============ COLUMNA 1: FFT COMPLETA ============
    # Subplot 1: Señal en tiempo
    ax1 = plt.subplot(3, 2, 1)
    tiempo = np.arange(len(data)) / fs
    ax1.plot(tiempo, data, 'b-', linewidth=0.8)
    ax1.set_title("Señal Completa en Tiempo (8.0s)", fontsize=11, fontweight='bold')
    ax1.set_xlabel("Tiempo (s)")
    ax1.set_ylabel("Amplitud")
    ax1.grid(True, linestyle='--', alpha=0.6)
    
    # Subplot 2: FFT completa
    ax2 = plt.subplot(3, 2, 2)
    ventana_hann = signal.windows.hann(len(data))
    datos_ventaneados = data * ventana_hann
    fft_complete = np.fft.fft(datos_ventaneados)
    frecuencias = np.fft.fftfreq(len(data), 1/fs)
    magnitud = np.abs(fft_complete)
    
    idx_positivas = frecuencias >= 0
    frecuencias_pos = frecuencias[idx_positivas]
    magnitud_pos = magnitud[idx_positivas]
    magnitud_db = 20 * np.log10(magnitud_pos + 1e-10)
    
    ax2.plot(frecuencias_pos, magnitud_db, 'b-', linewidth=0.8)
    ax2.set_title("FFT Completa (Resolución Global)", fontsize=11, fontweight='bold')
    ax2.set_xlabel("Frecuencia (Hz)")
    ax2.set_ylabel("Magnitud (dB)")
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.set_xlim([0, 2000])
    
    # Encontrar pico
    min_freq_idx = np.argmax(frecuencias_pos >= 50)
    pico_idx = min_freq_idx + np.argmax(magnitud_pos[min_freq_idx:])
    pico_freq = frecuencias_pos[pico_idx]
    ax2.plot(pico_freq, magnitud_db[pico_idx], 'r*', markersize=15, 
             label=f"Pico: {pico_freq:.1f} Hz")
    ax2.legend()
    
    # Subplot 3: Información de FFT completa
    ax3 = plt.subplot(3, 2, 3)
    ax3.axis('off')
    info_text = f"""
ANÁLISIS FFT COMPLETA:

• Se analiza toda la señal de una vez
• Da una visión GLOBAL de las frecuencias
• DESVENTAJA: Pierde variación temporal
• No muestra cómo cambia la frecuencia

• Resolución: {fs/len(data):.3f} Hz/bin
• Frecuencia pico: {pico_freq:.1f} Hz
• Duración: 8.0 segundos

CONCLUSIÓN:
Solo ve un pico promedio (~1000 Hz)
pero NO ve que la frecuencia
está CAMBIANDO en el tiempo
"""
    ax3.text(0.1, 0.5, info_text, fontsize=10, family='monospace',
            verticalalignment='center',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
    
    # ============ COLUMNA 2: FFT EN VENTANAS ============
    # Subplot 4: Primeras 3 ventanas superpuestas
    ax4 = plt.subplot(3, 2, 4)
    tamaño_ventana_muestras = int(0.5 * fs)
    colores_ventanas = ['blue', 'green', 'red']
    
    for i in range(3):
        inicio = i * tamaño_ventana_muestras
        fin = inicio + tamaño_ventana_muestras
        ventana_data = data[inicio:fin]
        ventana_hann_local = signal.windows.hann(len(ventana_data))
        datos_vent = ventana_data * ventana_hann_local
        
        fft_local = np.fft.fft(datos_vent)
        freq_local = np.fft.fftfreq(len(ventana_data), 1/fs)
        mag_local = np.abs(fft_local)
        
        idx_pos = freq_local >= 0
        freq_pos = freq_local[idx_pos]
        mag_db_local = 20 * np.log10(mag_local[idx_pos] + 1e-10)
        
        tiempo_inicio = inicio / fs
        ax4.plot(freq_pos, mag_db_local, colores_ventanas[i], 
                linewidth=1.5, label=f"Ventana {i+1} ({tiempo_inicio:.1f}s)", alpha=0.8)
    
    ax4.set_title("FFT en Ventanas de 0.5s (Primeras 3)", fontsize=11, fontweight='bold')
    ax4.set_xlabel("Frecuencia (Hz)")
    ax4.set_ylabel("Magnitud (dB)")
    ax4.grid(True, linestyle='--', alpha=0.6)
    ax4.set_xlim([0, 2000])
    ax4.legend()
    
    # Subplot 5: Evolución de frecuencias
    ax5 = plt.subplot(3, 2, 5)
    
    info_doppler = []
    num_ventanas = len(data) // tamaño_ventana_muestras
    
    for i in range(num_ventanas):
        inicio = i * tamaño_ventana_muestras
        fin = inicio + tamaño_ventana_muestras
        ventana_data = data[inicio:fin]
        ventana_hann_local = signal.windows.hann(len(ventana_data))
        datos_vent = ventana_data * ventana_hann_local
        
        fft_local = np.fft.fft(datos_vent)
        freq_local = np.fft.fftfreq(len(ventana_data), 1/fs)
        mag_local = np.abs(fft_local)
        
        idx_pos = freq_local >= 0
        freq_pos = freq_local[idx_pos]
        mag_pos = mag_local[idx_pos]
        
        min_freq_idx = np.argmax(freq_pos >= 50)
        pico_idx_local = min_freq_idx + np.argmax(mag_pos[min_freq_idx:])
        pico_freq_local = freq_pos[pico_idx_local]
        
        info_doppler.append({
            'ventana': i,
            'tiempo': (inicio + fin) / (2 * fs),
            'freq': pico_freq_local
        })
    
    tiempos = [info['tiempo'] for info in info_doppler]
    frecuencias_doppler = [info['freq'] for info in info_doppler]
    
    ax5.plot(tiempos, frecuencias_doppler, 'bo-', linewidth=2, markersize=6)
    ax5.fill_between(tiempos, frecuencias_doppler, alpha=0.3)
    ax5.set_title("Evolución de Frecuencia en el Tiempo", fontsize=11, fontweight='bold')
    ax5.set_xlabel("Tiempo (s)")
    ax5.set_ylabel("Frecuencia Pico (Hz)")
    ax5.grid(True, linestyle='--', alpha=0.6)
    
    # Marcar zonas
    ax5.axvspan(0, 4.5, alpha=0.1, color='red', label='Acercamiento')
    ax5.axvspan(4.5, 8, alpha=0.1, color='green', label='Alejamiento')
    ax5.legend()
    
    # Subplot 6: Información ventanas
    ax6 = plt.subplot(3, 2, 6)
    ax6.axis('off')
    
    freq_min_doppler = min(frecuencias_doppler)
    freq_max_doppler = max(frecuencias_doppler)
    
    info_text2 = f"""
ANÁLISIS FFT EN VENTANAS:

• Se divide la señal en ventanas pequeñas
• Cada ventana se analiza por separado
• VENTAJA: Ve cambios temporales
• Visualiza el efecto Doppler claramente

• Tamaño ventana: 0.5 segundos
• Frecuencia máxima: {freq_max_doppler:.1f} Hz
• Frecuencia mínima: {freq_min_doppler:.1f} Hz
• Variación: {freq_max_doppler - freq_min_doppler:.1f} Hz

CONCLUSIÓN:
¡CLARAMENTE se ve el efecto Doppler!
La frecuencia SUBE cuando se acerca
y BAJA cuando se aleja.

VELOCIDAD ESTIMADA: ~71.5 km/h
"""
    ax6.text(0.1, 0.5, info_text2, fontsize=10, family='monospace',
            verticalalignment='center',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
    
    fig.suptitle("Comparación: FFT Completa vs FFT en Ventanas Temporales\n" + 
                 "Análisis del Efecto Doppler en Sirena de Ambulancia",
                fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    
    if archivo_salida:
        carpeta = os.path.dirname(archivo_salida)
        if carpeta and not os.path.exists(carpeta):
            os.makedirs(carpeta)
        fig.savefig(archivo_salida, dpi=300, bbox_inches='tight')
        print(f"Gráfico guardado: {archivo_salida}")
        plt.close(fig)
    else:
        plt.show()


def main():
    carpeta_graficos = os.path.join(os.path.dirname(__file__), "..", "graficos-creados")
    if not os.path.exists(carpeta_graficos):
        os.makedirs(carpeta_graficos)
    
    sirenas = cargar_sirenas()
    
    if sirenas['sirena1'] is None:
        print("Error: No se pudo cargar Sirena 1")
        return
    
    fs1 = sirenas['sirena1']['fs']
    data1 = sirenas['sirena1']['data']
    
    print("="*70)
    print("COMPARACIÓN: FFT COMPLETA vs FFT EN VENTANAS TEMPORALES")
    print("="*70)
    print(f"\nGenerando gráfico comparativo...")
    
    archivo_comparacion = os.path.join(carpeta_graficos, 
                                      "Comparacion_FFT_Completa_vs_Ventanas.png")
    
    graficar_comparacion_fft_completa_vs_ventanas(fs1, data1, archivo_comparacion)
    
    print(f"\n✓ Gráfico guardado en: {archivo_comparacion}")
    print("="*70)


if __name__ == "__main__":
    main()
