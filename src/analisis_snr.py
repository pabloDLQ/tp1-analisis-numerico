import numpy as np
from scipy import signal

def calcular_snr_simple(data):
    """
    Calcula SNR de forma simple y robusta.
    Asume que los segmentos mas silenciosos contienen principalmente ruido.
    SNR = 10*log10(P_signal / P_noise)
    """
    # Asegurar que data es float
    data = np.array(data, dtype=np.float64)
    
    # Dividir en frames de 1024 muestras
    frame_size = 1024
    frames = []
    
    for i in range(0, len(data) - frame_size, frame_size):
        frame = data[i:i+frame_size]
        potencia = np.mean(frame ** 2)
        frames.append(max(potencia, 1e-15))
    
    frames = np.array(frames)
    
    # El 10% de frames más débiles = ruido
    threshold = np.percentile(frames, 10)
    noise_power = max(threshold, 1e-15)
    
    # Potencia total
    total_power = np.mean(data ** 2)
    total_power = max(total_power, 1e-15)
    
    # Potencia de signal (total - ruido)
    signal_power = total_power - noise_power
    if signal_power <= noise_power:  # Si es menor, reestimar
        signal_power = total_power - (noise_power * 0.5)
    
    # SNR en dB
    snr_db = 10 * np.log10(signal_power / noise_power) if noise_power > 0 else 0
    
    return snr_db, signal_power, noise_power


def metricas_basicas(data, fs):
    """Calcula metricas basicas de la senal"""
    # Evitar valores negativos
    valor_cuadrado_medio = np.mean(data ** 2)
    valor_cuadrado_medio = max(valor_cuadrado_medio, 1e-10)
    
    rms = np.sqrt(valor_cuadrado_medio)
    pico = np.max(np.abs(data))
    minimo = np.min(data)
    maximo = np.max(data)
    
    # Rango dinamico
    if rms > 1e-10:
        rango_dinamico_db = 20 * np.log10(pico / rms)
    else:
        rango_dinamico_db = 0
    
    duracion_s = len(data) / fs
    factor_cresta = pico / rms if rms > 1e-10 else 0
    
    return {
        'rms': rms,
        'pico': pico,
        'minimo': minimo,
        'maximo': maximo,
        'rango_dinamico_db': rango_dinamico_db,
        'duracion_s': duracion_s,
        'factor_cresta': factor_cresta,
        'num_muestras': len(data),
        'fs': fs
    }


def analizar_espectro(data, fs):
    """Analiza FFT y encuentra pico principal (excluyendo DC)"""
    # Ventana Hann
    ventana = signal.windows.hann(len(data))
    datos_ventaneados = data * ventana
    
    # FFT
    fft = np.fft.fft(datos_ventaneados)
    freqs = np.fft.fftfreq(len(data), 1/fs)
    magnitud = np.abs(fft)
    
    # Solo frecuencias positivas
    idx_pos = freqs >= 0
    freqs_pos = freqs[idx_pos]
    mag_pos = magnitud[idx_pos]
    
    # A dB
    mag_db = 20 * np.log10(mag_pos + 1e-10)
    
    # Pico: excluir 0 Hz (DC) y rango muy bajo (<20 Hz)
    min_freq = 20  # Hz
    idx_min_freq = np.argmax(freqs_pos >= min_freq)
    
    # Si no hay freqs >= 20 Hz, usar desde idx=1 (excluir DC)
    if idx_min_freq == 0:
        idx_min_freq = 1
    
    # Encontrar pico en el rango de interés
    mag_pos_filtrado = mag_pos[idx_min_freq:]
    
    idx_pico_local = np.argmax(mag_pos_filtrado)
    idx_pico = idx_min_freq + idx_pico_local
    freq_pico = freqs_pos[idx_pico]
    pot_pico = mag_db[idx_pico]
    
    return freqs_pos, mag_db, freq_pico, pot_pico


def imprimir_analisis_completo(nombre, data, fs):
    """Imprime analisis completo de una senal"""
    print(f"\n{'='*60}")
    print(f"Analisis SNR: {nombre}")
    print(f"{'='*60}")
    
    # SNR
    try:
        snr_db, p_signal, p_noise = calcular_snr_simple(data)
    except:
        snr_db = 0
        p_signal = np.mean(data ** 2)
        p_noise = p_signal * 0.01
    
    print(f"SNR: {snr_db:.2f} dB")
    print(f"  Potencia de senal: {p_signal:.2e}")
    print(f"  Potencia de ruido: {p_noise:.2e}")
    
    # Metricas basicas
    metricas = metricas_basicas(data, fs)
    print(f"\nMetricas de Calidad:")
    print(f"  RMS: {metricas['rms']:.2e}")
    print(f"  Pico: {metricas['pico']:.2e}")
    print(f"  Factor de cresta: {metricas['factor_cresta']:.2f}")
    print(f"  Rango dinamico: {metricas['rango_dinamico_db']:.2f} dB")
    print(f"  Duracion: {metricas['duracion_s']:.2f} s")
    
    # Espectro
    try:
        freqs, mag_db, freq_pico, pot_pico = analizar_espectro(data, fs)
        print(f"\nAnalisis Espectral:")
        print(f"  Frecuencia de pico: {freq_pico:.1f} Hz")
        print(f"  Potencia en pico: {pot_pico:.1f} dB")
    except:
        freq_pico = 0
        pot_pico = 0
        freqs = np.array([])
        mag_db = np.array([])
        print(f"\nAnalisis Espectral: Error en calculo")
    
    print(f"{'='*60}\n")
    
    return {
        'snr_db': snr_db,
        'p_signal': p_signal,
        'p_noise': p_noise,
        'metricas': metricas,
        'freq_pico': freq_pico,
        'pot_pico': pot_pico,
        'freqs': freqs,
        'mag_db': mag_db
    }
