# Estructura del Proyecto - Item 2 Reorganizado

## Cambios Realizados

Los cálculos del Item 2 han sido movidos a la carpeta `src/` para mantener el proyecto ordenado:

### Archivos de Código (en `src/`)

```
src/
├── analisis_doppler.py           # Módulo principal con funciones de cálculo
├── analizar_item2.py             # Script de análisis Item 2
├── comparar_metodos_fft.py       # Script comparativo FFT
├── cargar_sirenas.py             # Cargar archivos de audio
├── filtro_paso_banda.py          # Aplicar filtros
└── graficador.py                 # Generar gráficos
```

### Archivos de Documentación (en raíz)

```
├── INICIO_RAPIDO.txt             # Guía rápida
├── README_ITEM2.md               # Manual completo
├── GUIA_ITEM2_DOPPLER.md         # Conceptos teóricos
├── PASO_A_PASO.md                # Tutorial detallado
├── RESUMEN_FINAL.txt             # Resumen ejecutivo
└── src/
    └── ejemplos_integracion.py   # Ejemplos de código
```

## Cómo Ejecutar

### Opción 1: Menú Interactivo

```bash
python run_item2.py
```

Esto abrirá un menú para elegir qué análisis ejecutar.

### Opción 2: Directo desde src

```bash
python -m src.analizar_item2
```

Para análisis del Item 2

```bash
python -m src.comparar_metodos_fft
```

Para comparativa FFT

### Opción 3: Con argumentos

```bash
python run_item2.py 1    # Analizar Item 2
python run_item2.py 2    # Comparar métodos
```

## Archivos Generados

Todos los gráficos se guardan en `graficos-creados/`:

- `Sirena1_FFT_Ventanas_0.5s.png` - 16 ventanas FFT
- `Comparacion_FFT_Completa_vs_Ventanas.png` - Comparativa

## Estructura Completa del Proyecto

```
tp1-analisis-numerico/
│
├── src/                          # Código fuente
│   ├── __init__.py
│   ├── analisis_doppler.py       # ✓ Cálculos Item 2
│   ├── analizar_item2.py         # ✓ Script Item 2
│   ├── cargar_sirenas.py
│   ├── comparar_metodos_fft.py   # ✓ Comparativa
│   ├── ejemplos_integracion.py   # ✓ Ejemplos
│   ├── filtro_paso_banda.py
│   └── graficador.py
│
├── graficos-creados/             # Salida de gráficos
│
├── data/                         # Archivos de audio
│
├── Imagenes/                     # Imágenes de referencia
│
├── run_item2.py                  # ✓ Ejecutor principal
│
├── main.py                       # Script principal del proyecto
│
├── INICIO_RAPIDO.txt             # ✓ Documentación
├── README_ITEM2.md               # ✓ Manual
├── GUIA_ITEM2_DOPPLER.md         # ✓ Guía conceptual
├── PASO_A_PASO.md                # ✓ Tutorial
├── RESUMEN_FINAL.txt             # ✓ Resumen
│
└── requirements.txt              # Dependencias
```

## Beneficios de Esta Estructura

✓ **Código organizado**: Todo en `src/`  
✓ **Fácil acceso**: Script `run_item2.py` en raíz  
✓ **Documentación clara**: Explicaciones en archivos `.md` y `.txt`  
✓ **Modular**: Funciones reutilizables en `analisis_doppler.py`  
✓ **Escalable**: Fácil agregar más análisis  

## Ejecución Recomendada

Para el trabajo completo del Item 2:

```bash
python run_item2.py
```

Luego selecciona:
1. Para generar análisis y velocidad
2. Para ver la comparativa visual

Todos los gráficos se guardan automáticamente.
