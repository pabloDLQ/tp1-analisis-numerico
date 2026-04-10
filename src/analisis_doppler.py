import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import os

def analizar_fft_ventanas_temporales(fs, data, titulo="FFT en Ventanas Temporales", 
                                     tamaño_ventana_s=0.5, color='b', archivo_salida=None):
    """
    Analiza FFT en ventanas temporales pequeñas para observar cambios de frecuencia (efecto Doppler).
    
    Parámetros:
    - fs: frecuencia de muestreo (Hz)
    - data: array con las muestras
    - titulo: título principal
    - tamaño_ventana_s: tamaño de ventana en segundos (default 0.5s)
    - color: color de las líneas
    - archivo_salida: ruta para guardar imagen
    
    Retorna:
    - diccionario con información de frecuencias por ventana
    """
    
    # Calcular tamaño de ventana en muestras
    tamaño_ventana_muestras = int(tamaño_ventana_s * fs)
    num_ventanas = len(data) // tamaño_ventana_muestras
    
    if num_ventanas < 1:
        print(f"Error: Señal muy corta para ventanas de {tamaño_ventana_s}s")
        return None
    
    # Crear figura con subplots
    ventanas_por_fila = 3
    num_filas = (num_ventanas + ventanas_por_fila - 1) // ventanas_por_fila
    
    fig, axes = plt.subplots(num_filas, ventanas_por_fila, figsize=(15, 4*num_filas))
    
    # Asegurar que axes sea un array 2D
    if num_filas == 1 and ventanas_por_fila == 1:
        axes = np.array([[axes]])
    elif num_filas == 1:
        axes = axes.reshape(1, -1)
    elif ventanas_por_fila == 1:
        axes = axes.reshape(-1, 1)
    
    info_ventanas = []
    
    # Procesar cada ventana
    for i in range(num_ventanas):
        inicio = i * tamaño_ventana_muestras
        fin = inicio + tamaño_ventana_muestras
        
        # Extraer ventana
        ventana_data = data[inicio:fin]
        
        # Aplicar ventana de Hann
        ventana_hann = signal.windows.hann(len(ventana_data))
        datos_ventaneados = ventana_data * ventana_hann
        
        # Calcular FFT
        fft = np.fft.fft(datos_ventaneados)
        frecuencias = np.fft.fftfreq(len(ventana_data), 1/fs)
        magnitud = np.abs(fft)
        
        # Solo frecuencias positivas
        idx_positivas = frecuencias >= 0
        frecuencias_pos = frecuencias[idx_positivas]
        magnitud_pos = magnitud[idx_positivas]
        magnitud_db = 20 * np.log10(magnitud_pos + 1e-10)
        
        # Encontrar pico (excluyendo DC y frecuencias bajas)
        min_freq = 50  # Hz
        idx_min_freq = np.argmax(frecuencias_pos >= min_freq)
        
        if idx_min_freq < len(magnitud_pos):
            mag_filtrada = magnitud_pos[idx_min_freq:]
            idx_pico_local = np.argmax(mag_filtrada)
            idx_pico = idx_min_freq + idx_pico_local
        else:
            idx_pico = 1 + np.argmax(magnitud_pos[1:])
        
        freq_pico = frecuencias_pos[idx_pico]
        pot_pico = magnitud_db[idx_pico]
        
        info_ventanas.append({
            'ventana': i,
            'tiempo_inicio': inicio / fs,
            'tiempo_fin': fin / fs,
            'freq_pico': freq_pico,
            'magnitud_pico': pot_pico
        })
        
        # Graficar
        fila = i // ventanas_por_fila
        col = i % ventanas_por_fila
        ax = axes[fila, col]
        
        ax.plot(frecuencias_pos, magnitud_db, color=color, linewidth=0.8)
        ax.plot(freq_pico, pot_pico, 'r*', markersize=12)
        
        tiempo_inicio = inicio / fs
        tiempo_fin = fin / fs
        ax.set_title(f"Ventana {i+1} ({tiempo_inicio:.2f}-{tiempo_fin:.2f}s)\nPico: {freq_pico:.1f} Hz", 
                    fontsize=9)
        ax.set_xlabel("Frecuencia (Hz)", fontsize=8)
        ax.set_ylabel("Magnitud (dB)", fontsize=8)
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.set_xlim([0, 2000])
    
    # Desactivar subplots vacíos
    total_subplots = num_filas * ventanas_por_fila
    for i in range(num_ventanas, total_subplots):
        fila = i // ventanas_por_fila
        col = i % ventanas_por_fila
        axes[fila, col].set_visible(False)
    
    fig.suptitle(f"{titulo} (ventanas de {tamaño_ventana_s}s)", fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    # Guardar si se especifica
    if archivo_salida:
        carpeta = os.path.dirname(archivo_salida)
        if carpeta and not os.path.exists(carpeta):
            os.makedirs(carpeta)
        fig.savefig(archivo_salida, dpi=300, bbox_inches='tight')
        print(f"Gráfico guardado: {archivo_salida}")
        plt.close(fig)
    
    return info_ventanas


def calcular_velocidad_ambulancia(freq_min, freq_max, freq_promedio=None):
    """
    Calcula la velocidad de la ambulancia usando efecto Doppler.
    
    Parámetros:
    - freq_min: frecuencia mínima detectada (Hz)
    - freq_max: frecuencia máxima detectada (Hz)
    - freq_promedio: frecuencia de reposo estimada (si no se proporciona, usa promedio)
    
    Retorna:
    - diccionario con velocidades calculadas
    """
    
    v_sonido = 343  # m/s a 20°C
    
    if freq_promedio is None:
        freq_promedio = (freq_min + freq_max) / 2
    
    # Fórmula Doppler (observador estacionario):
    # f_max = f0 * v_sonido / (v_sonido - v_ambulancia)  [acercamiento]
    # f_min = f0 * v_sonido / (v_sonido + v_ambulancia)  [alejamiento]
    
    # Despejando velocidad:
    v_acerca = v_sonido * (1 - freq_promedio / freq_max)
    v_aleja = v_sonido * (freq_promedio / freq_min - 1)
    v_promedio = (v_acerca + v_aleja) / 2
    
    return {
        'v_acerca_ms': v_acerca,
        'v_acerca_kmh': v_acerca * 3.6,
        'v_aleja_ms': v_aleja,
        'v_aleja_kmh': v_aleja * 3.6,
        'v_promedio_ms': v_promedio,
        'v_promedio_kmh': v_promedio * 3.6,
        'v_sonido': v_sonido
    }
