import os
import numpy as np
from scipy.io import wavfile

def cargar_audio(ruta_archivo):
    """
    Carga un archivo WAV y devuelve la frecuencia de muestreo y los datos.
    Si el archivo tiene múltiples canales, devuelve el primer canal (mono).
    """
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo {ruta_archivo} no existe.")
    fs, data = wavfile.read(ruta_archivo)
    # Si es estéreo, tomar solo un canal
    if data.ndim > 1:
        data = data[:, 0]
    return fs, data

def cargar_sirenas(carpeta='data'):
    """
    Carga los archivos sirena_1.wav y sirena_2.wav desde la carpeta especificada.
    Devuelve un diccionario con la información.
    """
    rutas = {
        'sirena1': os.path.join(carpeta, 'sirena_1.wav'),
        'sirena2': os.path.join(carpeta, 'sirena_2.wav')
    }
    resultados = {}
    for nombre, ruta in rutas.items():
        try:
            fs, data = cargar_audio(ruta)
            resultados[nombre] = {'fs': fs, 'data': data, 'ruta': ruta}
            print(f"Archivo {nombre} cargado: fs={fs} Hz, duración={len(data)/fs:.2f} s, muestras={len(data)}")
        except Exception as e:
            print(f"Error al cargar {nombre}: {e}")
            resultados[nombre] = None
    return resultados

if __name__ == "__main__":
    # Prueba rápida
    sirenas = cargar_sirenas()
    # Mostrar información
    for nombre, info in sirenas.items():
        if info:
            print(f"{nombre}: {info['fs']} Hz, {len(info['data'])} muestras")