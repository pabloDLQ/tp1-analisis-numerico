from src.cargar_sirenas import cargar_sirenas
from src.graficador import graficar_comparacion_seniales
from src.analisis_snr_v2 import imprimir_analisis_completo
import os

def main():
    # Crear la carpeta de gráficos si no existe
    carpeta_graficos = os.path.join(os.path.dirname(__file__), "graficos-creados")
    if not os.path.exists(carpeta_graficos):
        os.makedirs(carpeta_graficos)
    
    # Cargar las sirenas
    sirenas = cargar_sirenas()

    # Verificar que ambas se cargaron correctamente
    if sirenas['sirena1'] is None or sirenas['sirena2'] is None:
        print("Error: no se pudieron cargar los archivos.")
        return

    # Extraer datos
    fs1, data1 = sirenas['sirena1']['fs'], sirenas['sirena1']['data']
    fs2, data2 = sirenas['sirena2']['fs'], sirenas['sirena2']['data']

    # Mostrar información básica
    print("\n--- Información de las señales ---")
    print(f"Sirena 1: fs = {fs1} Hz, duración = {len(data1)/fs1:.2f} s")
    print(f"Sirena 2: fs = {fs2} Hz, duración = {len(data2)/fs2:.2f} s")

    # ============================================================
    # ANÁLISIS SNR
    # ============================================================
    print("\n" + "="*70)
    print("ANÁLISIS DE RELACIÓN SEÑAL-RUIDO (SNR)")
    print("="*70)
    
    # Análisis detallado de cada señal
    resultado_1 = imprimir_analisis_completo("Sirena 1", data1, fs1)
    resultado_2 = imprimir_analisis_completo("Sirena 2", data2, fs2)
    
    # Comparación SNR
    print("\n" + "="*70)
    print("COMPARACIÓN Y CONCLUSIONES")
    print("="*70)
    snr1 = resultado_1['snr_db']
    snr2 = resultado_2['snr_db']
    
    print(f"\nComparación SNR:")
    print(f"  Sirena 1: {snr1:.2f} dB")
    print(f"  Sirena 2: {snr2:.2f} dB")
    print(f"  Diferencia: {abs(snr1 - snr2):.2f} dB")
    
    if snr1 > snr2:
        mejor = "Sirena 1"
        valor_mejor = snr1
    else:
        mejor = "Sirena 2"
        valor_mejor = snr2
    
    print(f"\n  --> {mejor} tiene mejor SNR ({valor_mejor:.2f} dB)")
    print(f"      Una mayor SNR significa una señal más clara con menos ruido.")
    
    # Recomendación de filtro
    print(f"\nAnálisis de Frecuencias Dominantes:")
    freq_pico1 = resultado_1['freq_pico']
    freq_pico2 = resultado_2['freq_pico']
    print(f"  Sirena 1: Pico en {freq_pico1:.1f} Hz")
    print(f"  Sirena 2: Pico en {freq_pico2:.1f} Hz")
    
    # Análisis de si se necesita filtro
    snr_threshold = 15  # dB
    print(f"\nRecomendación de Filtrado:")
    if snr1 < snr_threshold or snr2 < snr_threshold:
        print(f"  [!] SNR < {snr_threshold} dB -> FILTRADO RECOMENDADO")
        print(f"      - Tipo sugerido: Filtro paso-banda alrededor de la frecuencia dominante")
        print(f"      - Alternativa: Filtro paso-bajo para eliminar ruido de alta frecuencia")
    else:
        print(f"  [OK] SNR > {snr_threshold} dB -> Señal relativamente limpia")
        print(f"       Filtrado es OPCIONAL; puede proceder directamente a análisis de frecuencia")
    
    print("\n" + "="*70 + "\n")
    
    # ============================================================
    # GRÁFICOS - COMPARACIÓN DE PRUEBAS
    # ============================================================
    
    # Definir ruta de salida para el gráfico de comparación
    archivo_comparacion = os.path.join(carpeta_graficos, "Comparacion_Sirena1_vs_Sirena2.png")
    
    graficar_comparacion_seniales(fs1, data1, fs2, data2,
                                  titulo1="Sirena 1",
                                  titulo2="Sirena 2",
                                  metricas1=resultado_1,
                                  metricas2=resultado_2,
                                  archivo_salida=archivo_comparacion)
    
    print(f"\n✓ Los gráficos han sido guardados en la carpeta '{carpeta_graficos}'")
    print(f"  - {archivo_comparacion}")


if __name__ == "__main__":
    main()