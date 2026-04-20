"""
Generador de espectrogramas para análisis de sirenas.

Este módulo genera espectrogramas de tiempo-frecuencia para las sirenas,
mostrando la evolución temporal de las componentes de frecuencia.

Uso desde línea de comandos:
    python -m src.analizar_espectrograma 1 0.5
        Genera espectrograma para Sirena 1 con ventanas de 0.5 segundos
    
    python -m src.analizar_espectrograma 2 0.25
        Genera espectrograma para Sirena 2 con ventanas de 0.25 segundos

Uso como módulo:
    from src.analizar_espectrograma import generar_espectrograma
    generar_espectrograma(fs, data, numero_sirena=1, tamaño_ventana_s=0.5)
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import argparse
import sys
import os

# Importar funciones de cargar_sirenas
from src.cargar_sirenas import cargar_sirenas


def generar_espectrograma(fs, data, numero_sirena=1, tamaño_ventana_s=0.5, 
                          titulo="Espectrograma", archivo_salida=None, 
                          freq_min=0, freq_max=3000):
    """
    Genera un espectrograma de tiempo-frecuencia para una señal de audio.
    
    Parámetros:
    -----------
    fs : float
        Frecuencia de muestreo en Hz
    data : ndarray
        Array con las muestras de audio
    numero_sirena : int, default 1
        Número de sirena (1 o 2) para seleccionar colormapa
    tamaño_ventana_s : float, default 0.5
        Tamaño de la ventana temporal en segundos
    titulo : str, default "Espectrograma"
        Título del gráfico
    archivo_salida : str, optional
        Ruta para guardar la imagen PNG
    freq_min : float, default 0
        Frecuencia mínima a mostrar en Hz
    freq_max : float, default 3000
        Frecuencia máxima a mostrar en Hz
    
    Retorna:
    --------
    dict : Información del espectrograma generado
    """
    
    # Validaciones
    if fs <= 0:
        raise ValueError("Frecuencia de muestreo debe ser positiva")
    if len(data) == 0:
        raise ValueError("Array de datos está vacío")
    if tamaño_ventana_s <= 0:
        raise ValueError("Tamaño de ventana debe ser positivo")
    
    # Calcular parámetros STFT (Short-Time Fourier Transform)
    nperseg = int(tamaño_ventana_s * fs)  # Número de muestras por ventana
    noverlap = int(nperseg * 0.75)  # 75% de solapamiento para suavidad
    
    # Generar STFT
    f, t, Sxx = signal.spectrogram(data, fs=fs, 
                                   window='hann',
                                   nperseg=nperseg,
                                   noverlap=noverlap,
                                   scaling='spectrum')
    
    # Limitar rango de frecuencias
    idx_freq = np.where((f >= freq_min) & (f <= freq_max))[0]
    f_limitado = f[idx_freq]
    Sxx_limitado = Sxx[idx_freq, :]
    
    # Convertir a dB (evitar log(0) añadiendo pequeño offset)
    Sxx_db = 10 * np.log10(Sxx_limitado + 1e-10)
    
    # Crear figura
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Seleccionar colormapa según sirena
    if numero_sirena == 2:
        cmap = 'Reds'
        titulo_completo = f"Espectrograma - {titulo} (Sirena 2)"
    else:
        cmap = 'Blues'
        titulo_completo = f"Espectrograma - {titulo} (Sirena 1)"
    
    # Dibujar espectrograma
    im = ax.pcolormesh(t, f_limitado, Sxx_db, shading='gouraud', cmap=cmap, 
                       rasterized=True)
    
    # Configurar ejes
    ax.set_ylabel('Frecuencia (Hz)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Tiempo (s)', fontsize=12, fontweight='bold')
    ax.set_title(titulo_completo, fontsize=14, fontweight='bold')
    ax.set_ylim([freq_min, freq_max])
    
    # Barra de colores
    cbar = fig.colorbar(im, ax=ax, label='Magnitud (dB)')
    
    # Grid
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Guardar imagen
    if archivo_salida:
        os.makedirs(os.path.dirname(archivo_salida), exist_ok=True)
        plt.savefig(archivo_salida, dpi=150, bbox_inches='tight')
        print(f"[OK] Espectrograma guardado: {archivo_salida}")
    
    plt.close()
    
    # Información del espectrograma
    duracion = len(data) / fs
    num_ventanas = len(t)
    freq_pico = f_limitado[np.argmax(np.mean(Sxx_db, axis=1))]
    
    info_espectrograma = {
        'numero_sirena': numero_sirena,
        'duracion_total_s': float(duracion),
        'frecuencia_muestreo_Hz': float(fs),
        'tamaño_ventana_s': float(tamaño_ventana_s),
        'numero_ventanas': int(num_ventanas),
        'rango_frecuencias_Hz': (float(freq_min), float(freq_max)),
        'frecuencia_dominante_Hz': float(freq_pico),
        'archivo_salida': archivo_salida
    }
    
    return info_espectrograma


def main(numero_sirena=1, tamaño_ventana_s=0.5):
    """
    Función principal para generar espectrogramas.
    
    Parámetros:
    -----------
    numero_sirena : int, default 1
        Número de sirena a analizar (1 o 2)
    tamaño_ventana_s : float, default 0.5
        Tamaño de la ventana temporal en segundos
    """
    
    # Validar entrada
    if numero_sirena not in [1, 2]:
        print("Error: numero_sirena debe ser 1 o 2")
        return
    
    if tamaño_ventana_s <= 0:
        print("Error: tamaño_ventana debe ser positivo")
        return
    
    # Crear carpeta de gráficos
    carpeta_graficos = os.path.join(os.path.dirname(__file__), "..", "graficos-creados")
    if not os.path.exists(carpeta_graficos):
        os.makedirs(carpeta_graficos)
    
    # Cargar sirenas
    print("="*70)
    print("ANÁLISIS DE ESPECTROGRAMA DE SIRENAS")
    print("="*70)
    print(f"\nCargando sirenas...")
    
    sirenas = cargar_sirenas()
    
    # Seleccionar sirena según parámetro
    if numero_sirena == 1:
        if sirenas['sirena1'] is None:
            print("Error: No se pudo cargar Sirena 1")
            return
        fs = sirenas['sirena1']['fs']
        data = sirenas['sirena1']['data']
        nombre_sirena = "Sirena 1"
        rango_freq = (500, 1500)  # Rango para Sirena 1
    else:  # numero_sirena == 2
        if sirenas['sirena2'] is None:
            print("Error: No se pudo cargar Sirena 2")
            return
        fs = sirenas['sirena2']['fs']
        data = sirenas['sirena2']['data']
        nombre_sirena = "Sirena 2"
        rango_freq = (500, 1700)  # Rango para Sirena 2
    
    duracion = len(data) / fs
    print(f"[OK] {nombre_sirena}: fs = {fs} Hz, duración = {duracion:.2f} s")
    print(f"[OK] Tamaño de ventana STFT: {tamaño_ventana_s} s")
    print(f"[OK] Rango de frecuencias a mostrar: {rango_freq[0]}-{rango_freq[1]} Hz")
    
    # Generar espectrograma
    print(f"\nGenerando espectrograma para {nombre_sirena}...")
    
    archivo_salida = os.path.join(carpeta_graficos, 
                                  f"{nombre_sirena.replace(' ', '')}_Espectrograma_{tamaño_ventana_s}s.png")
    
    info = generar_espectrograma(
        fs, data,
        numero_sirena=numero_sirena,
        tamaño_ventana_s=tamaño_ventana_s,
        titulo=nombre_sirena,
        archivo_salida=archivo_salida,
        freq_min=rango_freq[0],
        freq_max=rango_freq[1]
    )
    
    # Mostrar información
    print("\n" + "="*70)
    print("INFORMACIÓN DEL ESPECTROGRAMA")
    print("="*70)
    print(f"Sirena: {nombre_sirena}")
    print(f"Duración total: {info['duracion_total_s']:.2f} s")
    print(f"Frecuencia de muestreo: {info['frecuencia_muestreo_Hz']:.0f} Hz")
    print(f"Tamaño de ventana STFT: {info['tamaño_ventana_s']} s")
    print(f"Número de ventanas: {info['numero_ventanas']}")
    print(f"Rango de frecuencias mostrado: {info['rango_frecuencias_Hz'][0]:.0f} - {info['rango_frecuencias_Hz'][1]:.0f} Hz")
    print(f"Frecuencia dominante: {info['frecuencia_dominante_Hz']:.2f} Hz")
    
    print("\n" + "="*70)
    print(f"Archivo generado: {archivo_salida}")
    print("="*70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generador de espectrogramas para análisis de sirenas"
    )
    parser.add_argument(
        'numero_sirena',
        type=int,
        nargs='?',
        default=1,
        help='Número de sirena a analizar (1 o 2). Default: 1'
    )
    parser.add_argument(
        'tamaño_ventana',
        type=float,
        nargs='?',
        default=0.5,
        help='Tamaño de la ventana STFT en segundos. Default: 0.5'
    )
    
    args = parser.parse_args()
    
    main(numero_sirena=args.numero_sirena, tamaño_ventana_s=args.tamaño_ventana)
