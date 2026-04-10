# PASO A PASO: Generar Gráficos FFT en Ventanas Temporales de 0.5 Segundos

## 🎯 Objetivo del Item 2

```
Realizar una FFT de la sirena 1
        ↓
Compararla con FFT en ventanas pequeñas (0.5 segundos)
        ↓
Identificar el efecto físico (Efecto Doppler)
        ↓
Calcular la velocidad de la ambulancia
```

---

## ✅ Solución Completamente Implementada

Ya creé todo lo necesario. Solo necesitas ejecutar:

```bash
python analizar_item2.py
```

---

## 📊 ¿Qué Hace este Comando?

### Paso 1: Dividir la Señal en Ventanas
```
Sirena 1: 8 segundos de audio
         ↓
Dividir en ventanas de 0.5 segundos
         ↓
Ventana 1: 0.00-0.50s
Ventana 2: 0.50-1.00s
Ventana 3: 1.00-1.50s
...
Ventana 16: 7.50-8.00s
```

### Paso 2: Calcular FFT para cada Ventana
```
Para cada ventana:
  1. Aplicar ventana de Hann (optimización)
  2. Calcular FFT
  3. Encontrar frecuencia pico
  4. Graficar espectro
```

### Paso 3: Analizar Cambios en Frecuencia
```
Ventana 1-4:  Frecuencia = 1062 Hz ← MÁXIMA (acercamiento)
Ventana 5-7:  Frecuencia = 1058-1060 Hz
Ventana 8-9:  Frecuencia = 966-1038 Hz (transición)
Ventana 10-16: Frecuencia = 946 Hz ← MÍNIMA (alejamiento)

¡La frecuencia CAMBIA en el tiempo!
Esto es el EFECTO DOPPLER
```

### Paso 4: Calcular Velocidad de Ambulancia

**Usando la fórmula de Doppler:**

$$v_{ambulancia} = v_{sonido} \times \left(1 - \frac{f_0}{f_{máxima}}\right)$$

Con:
- $v_{sonido}$ = 343 m/s
- $f_0$ = 1003.38 Hz (promedio)
- $f_{máxima}$ = 1062 Hz

**Resultado:**
```
Velocidad ≈ 71.53 km/h
```

---

## 🖼️ Archivos de Salida

### 1. Gráfico Principal: `Sirena1_FFT_Ventanas_0.5s.png`

**Contenido:** 16 subplots (3×6 grid)

```
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Ventana 1   │ │ Ventana 2   │ │ Ventana 3   │
│ 0.0-0.5s    │ │ 0.5-1.0s    │ │ 1.0-1.5s    │
│ 1062 Hz     │ │ 1062 Hz     │ │ 1062 Hz     │
└─────────────┘ └─────────────┘ └─────────────┘

┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Ventana 4   │ │ Ventana 5   │ │ Ventana 6   │
│ 1.5-2.0s    │ │ 2.0-2.5s    │ │ 2.5-3.0s    │
│ 1062 Hz     │ │ 1060 Hz     │ │ 1060 Hz     │
└─────────────┘ └─────────────┘ └─────────────┘

... (12 ventanas más)

┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Ventana 14  │ │ Ventana 15  │ │ Ventana 16  │
│ 6.5-7.0s    │ │ 7.0-7.5s    │ │ 7.5-8.0s    │
│ 946 Hz      │ │ 946 Hz      │ │ 946 Hz      │
└─────────────┘ └─────────────┘ └─────────────┘
```

Cada subplot muestra:
- **Eje X:** Frecuencia (0-2000 Hz)
- **Eje Y:** Magnitud (dB)
- **Estrella Roja:** Pico detectado
- **Título:** Ventana, tiempo, frecuencia pico

### 2. Gráfico Comparativo: `Comparacion_FFT_Completa_vs_Ventanas.png`

**Muestra la diferencia entre:**

| FFT Completa | FFT en Ventanas |
|---|---|
| Una sola FFT | 16 FFTs separadas |
| No ve cambios | ✓ Ve Doppler claramente |
| Pico único (~1000 Hz) | Picos variables (946-1062 Hz) |

---

## 📋 Tabla de Frecuencias (Salida Consola)

Cuando ejecutes `python analizar_item2.py`, verás:

```
ANÁLISIS DE CAMBIO DE FRECUENCIA EN EL TIEMPO
----------------------------------------------
Ventana    Tiempo (s)           Frecuencia Pico (Hz)
-------------------------------------------------------
1          0.00-0.50s         1062.00
2          0.50-1.00s         1062.00
3          1.00-1.50s         1062.00
4          1.50-2.00s         1062.00
5          2.00-2.50s         1060.00
6          2.50-3.00s         1060.00
7          3.00-3.50s         1058.00
8          3.50-4.00s         1038.00
9          4.00-4.50s         966.00
10         4.50-5.00s         948.00
11         5.00-5.50s         946.00
12         5.50-6.00s         946.00
13         6.00-6.50s         946.00
14         6.50-7.00s         946.00
15         7.00-7.50s         946.00
16         7.50-8.00s         946.00

----------------------------------------------
Frecuencia mínima: 946.00 Hz
Frecuencia máxima: 1062.00 Hz
Frecuencia promedio: 1003.38 Hz
Variación total: 116.00 Hz (11.6%)

======================================================================
EFECTO FÍSICO OBSERVADO: EFECTO DOPPLER
======================================================================

La variación de frecuencia de 116.00 Hz indica el efecto Doppler.

¿Qué está ocurriendo?
- Cuando la ambulancia SE ACERCA: la frecuencia AUMENTA a 1062.00 Hz
- Cuando la ambulancia SE ALEJA: la frecuencia DISMINUYE a 946.00 Hz

CÁLCULO DE VELOCIDAD DE LA AMBULANCIA
======================================================================

RESULTADOS:

Velocidad acercándose: 18.93 m/s (68.16 km/h)
Velocidad alejándose:  20.80 m/s (74.89 km/h)
Velocidad promedio:    19.87 m/s (71.53 km/h)
```

---

## 🔧 Archivos del Proyecto

```
tp1-analisis-numerico/
│
├── src/
│   └── analisis_doppler.py (NUEVO) ✨
│       ├── analizar_fft_ventanas_temporales()
│       └── calcular_velocidad_ambulancia()
│
├── analizar_item2.py (NUEVO) ✨ ← EJECUTAR ESTO
│
├── comparar_metodos_fft.py (NUEVO) ✨
│
├── README_ITEM2.md (NUEVO) ✨
│   └── Documentación completa
│
├── GUIA_ITEM2_DOPPLER.md (NUEVO) ✨
│   └── Guía paso a paso
│
├── EJEMPLOS_INTEGRACION.py (NUEVO) ✨
│   └── Ejemplos de integración
│
├── graficos-creados/
│   ├── Sirena1_FFT_Ventanas_0.5s.png ← GENERADO
│   └── Comparacion_FFT_Completa_vs_Ventanas.png ← GENERADO
│
└── main.py (archivo original)
```

---

## 🚀 Instrucciones de Ejecución

### Opción 1: Análisis Básico (RECOMENDADO)

```bash
python analizar_item2.py
```

**Genera:**
- Gráfico FFT en 16 ventanas
- Tabla de frecuencias
- Velocidad calculada

### Opción 2: Ver Comparativa

```bash
python comparar_metodos_fft.py
```

**Genera:**
- Gráfico comparativo: FFT completa vs ventanas
- Visualización del efecto Doppler

### Opción 3: Integración en main.py

Ver archivo: `EJEMPLOS_INTEGRACION.py`

---

## 📚 Conceptos Clave

### ¿Por qué FFT en Ventanas?

**FFT Completa (Análisis Global):**
```
Entrada:  8 segundos de audio
Proceso:  Una sola transformada
Salida:   Un espectro promediado
Problema: ❌ Pierde información temporal
         ❌ No ve el efecto Doppler
```

**FFT en Ventanas (Análisis Temporal):**
```
Entrada:  8 segundos de audio
Proceso:  16 FFTs de 0.5s cada una
Salida:   16 espectros diferentes
Ventaja:  ✓ Ve cambios en el tiempo
         ✓ Detecta Doppler claramente
```

### Efecto Doppler

**Definición:** Cambio de frecuencia percibida cuando hay movimiento relativo

**En una ambulancia:**
- **Se acerca:** Ondas comprimidas → Frecuencia aumenta ↑
- **Se aleja:** Ondas expandidas → Frecuencia disminuye ↓

**Medido en este análisis:**
- Acercamiento: 1062 Hz
- Alejamiento: 946 Hz
- Diferencia: 116 Hz (11.6%)

---

## ✨ Características Implementadas

✅ División automática en ventanas  
✅ Cálculo de FFT por ventana  
✅ Detección automática de picos  
✅ Gráficos multiples generados  
✅ Fórmula de Doppler aplicada  
✅ Velocidad calculada en m/s y km/h  
✅ Documentación completa  
✅ Ejemplos de uso incluidos  

---

## 💾 Para tu Informe

**Tabla a copiar:**

| Ventana | Tiempo (s) | Frecuencia (Hz) | Fase |
|---------|--|--|--|
| 1-4 | 0.0-2.0 | 1062 | Acercamiento |
| 5-7 | 2.0-3.5 | 1060-1058 | Transición |
| 8-9 | 3.5-4.5 | 1038-966 | Transición |
| 10-16 | 4.5-8.0 | 946 | Alejamiento |

**Resultado Principal:**

```
Velocidad de la ambulancia (Sirena 1): 71.53 km/h

Método: Análisis de efecto Doppler usando FFT en ventanas
Verificación: 68.16 km/h (acercándose) y 74.89 km/h (alejándose)
```

---

## ❓ Preguntas Frecuentes

**P: ¿Puedo cambiar el tamaño de ventana?**  
R: Sí, edita `analizar_item2.py` línea ~29: `tamaño_ventana=0.5`

**P: ¿Cómo integro esto en main.py?**  
R: Ver `EJEMPLOS_INTEGRACION.py` para 3 opciones diferentes

**P: ¿Qué significa la estrella roja?**  
R: Indica la frecuencia pico detectada en cada ventana

**P: ¿Son exactos los valores de velocidad?**  
R: Son una aproximación. La velocidad real puede variar según las condiciones.

---

¡Listo! Solo ejecuta `python analizar_item2.py` y tendrás todo lo necesario para tu informe. 🎉
