# Guía: Generando Gráficos FFT en Ventanas Temporales (Item 2)

## Descripción del Problema

El item 2 te pide:
1. Realizar una FFT de la sirena 1
2. Compararla con una FFT en **ventanas temporales de 0.5 segundos**
3. Identificar el **efecto físico** que está ocurriendo
4. **Calcular la velocidad de la ambulancia**

## Solución Implementada

### 1. Crear archivo de análisis Doppler (`src/analisis_doppler.py`)

Este archivo contiene dos funciones principales:

```python
def analizar_fft_ventanas_temporales(fs, data, tamaño_ventana_s=0.5, ...)
```
- Divide la señal en ventanas de 0.5 segundos
- Calcula FFT para cada ventana
- Identifica la frecuencia pico en cada ventana
- Grafica todos los espectros para visualizar cambios

```python
def calcular_velocidad_ambulancia(freq_min, freq_max, freq_promedio=None)
```
- Aplica la fórmula de efecto Doppler
- Calcula velocidad en acercamiento y alejamiento
- Retorna velocidad en m/s y km/h

### 2. Ejecutar el análisis

```bash
python analizar_item2.py
```

Esto genera:
- `Sirena1_FFT_Ventanas_0.5s.png`: Gráfico con 16 ventanas FFT
- Tabla de frecuencias por ventana
- Velocidad calculada de la ambulancia

## Resultados del Análisis

### FFT por Ventanas (0.5 segundos cada una)

| Ventana | Tiempo (s) | Frecuencia Pico (Hz) |
|---------|------------|-------------------|
| 1-4 | 0.00-2.00 | 1062 |
| 5-6 | 2.00-3.00 | 1060 |
| 7 | 3.00-3.50 | 1058 |
| 8 | 3.50-4.00 | 1038 |
| 9 | 4.00-4.50 | 966 |
| 10-16 | 4.50-8.00 | 946 |

### Efecto Físico: EFECTO DOPPLER

**¿Qué está ocurriendo?**

La variación de frecuencia de **116 Hz (11.6%)** indica:

- **Fase 1 (0-4.5s)**: La ambulancia SE ACERCA → Frecuencia SUBE de 1062 Hz
- **Fase 2 (4.5-8.0s)**: La ambulancia SE ALEJA → Frecuencia BAJA a 946 Hz

**¿Por qué ocurre?**

1. **Acercamiento**: Las ondas sonoras se comprimen (longitud de onda disminuye)
2. **Alejamiento**: Las ondas sonoras se expanden (longitud de onda aumenta)
3. El observador percibe diferentes frecuencias según el movimiento relativo

### Velocidad de la Ambulancia

Usando la fórmula de Doppler:

$$f_{observado} = f_0 \times \frac{v_{sonido}}{v_{sonido} \mp v_{ambulancia}}$$

**Con los valores detectados:**
- $f_{máxima} = 1062$ Hz (acercamiento)
- $f_{mínima} = 946$ Hz (alejamiento)  
- $f_0 \approx 1003.38$ Hz (frecuencia de reposo)
- $v_{sonido} = 343$ m/s (a 20°C)

**Velocidades calculadas:**
- **Acercándose**: 18.93 m/s (**68.16 km/h**)
- **Alejándose**: 20.80 m/s (**74.89 km/h**)
- **Promedio**: 19.87 m/s (**71.53 km/h**)

## Uso en tu Código

Si quieres integrar esto en `main.py`:

```python
from src.analisis_doppler import analizar_fft_ventanas_temporales, calcular_velocidad_ambulancia
import numpy as np

# Después de cargar las sirenas
fs1, data1 = sirenas['sirena1']['fs'], sirenas['sirena1']['data']

# Analizar ventanas de 0.5 segundos
info_ventanas = analizar_fft_ventanas_temporales(
    fs1, data1,
    titulo="Sirena 1 - Análisis Doppler",
    tamaño_ventana_s=0.5,
    archivo_salida="graficos-creados/Sirena1_Ventanas_0.5s.png"
)

# Extraer información
frecuencias = [info['freq_pico'] for info in info_ventanas]
freq_min = np.min(frecuencias)
freq_max = np.max(frecuencias)
freq_promedio = np.mean(frecuencias)

# Calcular velocidad
velocidades = calcular_velocidad_ambulancia(freq_min, freq_max, freq_promedio)
print(f"Velocidad promedio: {velocidades['v_promedio_kmh']:.2f} km/h")
```

## Personalización

### Cambiar tamaño de ventana

```python
# Para ventanas de 1 segundo
info = analizar_fft_ventanas_temporales(fs1, data1, tamaño_ventana_s=1.0)

# Para ventanas de 0.25 segundos
info = analizar_fft_ventanas_temporales(fs1, data1, tamaño_ventana_s=0.25)
```

### Cambiar rango de visualización FFT

En `src/analisis_doppler.py`, línea ~107:
```python
ax.set_xlim([0, 2000])  # Cambiar 2000 por el rango deseado
```

## Archivos Generados

- `analizar_item2.py`: Script principal
- `src/analisis_doppler.py`: Funciones de análisis
- `graficos-creados/Sirena1_FFT_Ventanas_0.5s.png`: Gráfico con todas las ventanas

## Referencias

- **Efecto Doppler**: https://es.wikipedia.org/wiki/Efecto_Doppler
- **FFT (Fast Fourier Transform)**: Transformada rápida de Fourier
- **Ventanas temporales**: Técnica para analizar señales no-estacionarias
