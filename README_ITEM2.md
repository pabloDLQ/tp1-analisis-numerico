# ITEM 2: Cómo Generar Gráficos FFT en Ventanas Temporales de 0.5 segundos

## Respuesta Rápida

Para generar gráficos FFT en ventanas temporales de 0.5 segundos:

```bash
python analizar_item2.py
```

Este comando:
1. ✓ Divide la Sirena 1 en ventanas de 0.5s
2. ✓ Calcula FFT para cada ventana
3. ✓ Visualiza cómo cambia la frecuencia en el tiempo
4. ✓ Calcula la velocidad de la ambulancia

**Resultado:** Archivo `Sirena1_FFT_Ventanas_0.5s.png` con 16 ventanas FFT

---

## ¿Por Qué Usar Ventanas Temporales?

### FFT Completa (Análisis Global)
```
Señal de 8 segundos
         ↓
    Una sola FFT
         ↓
  Un solo espectro
         ↓
  ❌ No ve cambios en el tiempo
  ❌ Pierde información temporal
```

### FFT en Ventanas (Análisis Temporal)
```
Señal de 8 segundos
         ↓
16 ventanas de 0.5s
         ↓
16 FFTs separadas
         ↓
✓ Ve cambios en el tiempo
✓ Detecta efecto Doppler claramente
```

---

## Archivos Creados

### 1. `src/analisis_doppler.py` - Funciones Principales

#### Función 1: `analizar_fft_ventanas_temporales()`
```python
info = analizar_fft_ventanas_temporales(
    fs=44100,           # Frecuencia muestreo
    data=data1,         # Datos señal
    tamaño_ventana_s=0.5,  # Ventanas de 0.5s
    titulo="Sirena 1",
    color='blue',
    archivo_salida="grafico.png"
)
```

Retorna: Lista de diccionarios con:
- `ventana`: número de ventana
- `tiempo_inicio`, `tiempo_fin`: marcos temporales
- `freq_pico`: frecuencia pico detectada
- `magnitud_pico`: amplitud del pico

#### Función 2: `calcular_velocidad_ambulancia()`
```python
velocidades = calcular_velocidad_ambulancia(
    freq_min=946,           # Hz
    freq_max=1062,          # Hz
    freq_promedio=1003.38   # Hz
)

print(f"Velocidad: {velocidades['v_promedio_kmh']:.1f} km/h")
```

Retorna: Diccionario con velocidades en m/s y km/h

---

## Scripts Disponibles

### Script 1: `analizar_item2.py` (RECOMENDADO)
**Uso:** Análisis completo con detalles

```bash
python analizar_item2.py
```

**Genera:**
- Gráfico `Sirena1_FFT_Ventanas_0.5s.png`
- Tabla de frecuencias por ventana
- Cálculo de velocidad
- Explicación del efecto Doppler

**Output de consola:**
```
======================================================================
ITEM 2: ANÁLISIS DE FFT EN VENTANAS TEMPORALES (EFECTO DOPPLER)
======================================================================

Ventana    Tiempo (s)           Frecuencia Pico (Hz)
-------------------------------------------------------
1          0.00-0.50s         1062.00
2          0.50-1.00s         1062.00
...

Frecuencia mínima: 946.00 Hz
Frecuencia máxima: 1062.00 Hz
Frecuencia promedio: 1003.38 Hz
Variación total: 116.00 Hz (11.6%)

RESULTADOS:
Velocidad acercándose: 18.93 m/s (68.16 km/h)
Velocidad alejándose:  20.80 m/s (74.89 km/h)
Velocidad promedio:    19.87 m/s (71.53 km/h)
```

### Script 2: `comparar_metodos_fft.py` (ILUSTRATIVO)
**Uso:** Ver diferencia entre FFT completa vs ventanas

```bash
python comparar_metodos_fft.py
```

**Genera:** Gráfico comparativo con 6 subplots mostrando:
- Señal completa en tiempo
- FFT global (no ve variación)
- FFT en ventanas (ve Doppler)
- Evolución temporal de frecuencias

---

## Resultados Obtenidos

### Análisis de Sirena 1 (8 segundos)

| Aspecto | Valor |
|---------|-------|
| Resolución temporal | 16 ventanas × 0.5s |
| Frecuencia máxima | 1062 Hz (0-4.5s) |
| Frecuencia mínima | 946 Hz (4.5-8.0s) |
| Variación total | 116 Hz (11.6%) |
| **Velocidad promedio** | **71.53 km/h** |

### Fases Detectadas

**Fase 1: Acercamiento (0-4.5 segundos)**
- Frecuencia aumenta gradualmente
- 1062 Hz → máxima compresión
- Ambulancia se acerca → velocidad ~68 km/h

**Fase 2: Alejamiento (4.5-8.0 segundos)**
- Frecuencia disminuye 
- 946 Hz → máxima expansión
- Ambulancia se aleja → velocidad ~75 km/h

---

## Cómo Personalizar

### Cambiar tamaño de ventana

```python
# Ventanas de 1 segundo
analizar_fft_ventanas_temporales(fs1, data1, tamaño_ventana_s=1.0)

# Ventanas de 0.25 segundos
analizar_fft_ventanas_temporales(fs1, data1, tamaño_ventana_s=0.25)

# Ventanas de 2 segundos
analizar_fft_ventanas_temporales(fs1, data1, tamaño_ventana_s=2.0)
```

### Cambiar rango de frecuencias en gráfico

En `src/analisis_doppler.py` línea ~107:
```python
ax.set_xlim([0, 2000])  # Cambiar este valor
```

Ejemplos:
```python
ax.set_xlim([0, 5000])  # Ver rango más amplio
ax.set_xlim([500, 1500])  # Zoom en rango de sirena
```

### Aplicar a Sirena 2

```python
from src.cargar_sirenas import cargar_sirenas
from src.analisis_doppler import analizar_fft_ventanas_temporales

sirenas = cargar_sirenas()
fs2 = sirenas['sirena2']['fs']
data2 = sirenas['sirena2']['data']

info = analizar_fft_ventanas_temporales(
    fs2, data2,
    titulo="Sirena 2 - Análisis Doppler",
    tamaño_ventana_s=0.5,
    archivo_salida="graficos-creados/Sirena2_Ventanas.png"
)
```

---

## Fórmula de Doppler Utilizada

$$f_{observado} = f_0 \times \frac{v_{sonido}}{v_{sonido} \mp v_{fuente}}$$

Donde:
- $f_0$: frecuencia de reposo de la sirena
- $v_{sonido}$ = 343 m/s (a 20°C)
- $v_{fuente}$: velocidad de la ambulancia
- Signo negativo: fuente acercándose (+ f)
- Signo positivo: fuente alejándose (- f)

**Despejando velocidad:**

$$v_{ambulancia} = v_{sonido} \times \left(1 - \frac{f_0}{f_{máxima}}\right)$$

---

## Archivos Generados

```
graficos-creados/
├── Sirena1_FFT_Ventanas_0.5s.png
│   └── 16 subplots con FFT de cada ventana
├── Comparacion_FFT_Completa_vs_Ventanas.png
│   └── Comparativa visual del método
└── [otros gráficos existentes]
```

---

## Próximos Pasos

1. **Ejecutar:** `python analizar_item2.py`
2. **Revisar gráfico:** Abrir `Sirena1_FFT_Ventanas_0.5s.png`
3. **Analizar tabla:** Copiar tabla de frecuencias a tu informe
4. **Explicar:** Describir el efecto Doppler observado
5. **Documentar:** Incluir velocidad calculada (71.53 km/h)

---

## Troubleshooting

| Problema | Solución |
|----------|----------|
| "ModuleNotFoundError" | Ejecutar desde directorio raíz |
| Gráfico no se genera | Verificar que `graficos-creados/` existe |
| Valores de velocidad irracionales | Verificar que freq_min < freq_max |
| Ventanas están vacías | Aumentar `tamaño_ventana_s` si señal es corta |

