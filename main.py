from src.cargar_sirenas import cargar_sirenas
from src.graficador import graficar_comparacion_seniales
from src.analisis_snr import imprimir_analisis_completo
import os

def main():
    # Crear la carpeta de graficos si no existe
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

    # Mostrar informacion basica
    print("\n--- Informacion de las senales ---")
    print(f"Sirena 1: fs = {fs1} Hz, duracion = {len(data1)/fs1:.2f} s")
    print(f"Sirena 2: fs = {fs2} Hz, duracion = {len(data2)/fs2:.2f} s")

    # ============================================================
    # ANALISIS SNR
    # ============================================================
    print("\n" + "="*70)
    print("ANALISIS DE RELACION SENAL-RUIDO (SNR)")
    print("="*70)
    
    # Analisis detallado de cada senal
    resultado_1 = imprimir_analisis_completo("Sirena 1", data1, fs1)
    resultado_2 = imprimir_analisis_completo("Sirena 2", data2, fs2)
    
    # Comparacion SNR
    print("\n" + "="*70)
    print("COMPARACION Y CONCLUSIONES")
    print("="*70)
    snr1 = resultado_1['snr_db']
    snr2 = resultado_2['snr_db']
    
    print(f"\nComparacion SNR:")
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
    print(f"      Una mayor SNR significa una senal mas clara con menos ruido.")
    
    # Recomendacion de filtro
    print(f"\nAnalisis de Frecuencias Dominantes:")
    freq_pico1 = resultado_1['freq_pico']
    freq_pico2 = resultado_2['freq_pico']
    print(f"  Sirena 1: Pico en {freq_pico1:.1f} Hz")
    print(f"  Sirena 2: Pico en {freq_pico2:.1f} Hz")
    
    # Analisis de si se necesita filtro
    snr_threshold = 15  # dB
    print(f"\nRecomendacion de Filtrado:")
    if snr1 < snr_threshold or snr2 < snr_threshold:
        print(f"  [!] SNR < {snr_threshold} dB -> FILTRADO RECOMENDADO")
        print(f"      - Tipo sugerido: Filtro paso-banda alrededor de la frecuencia dominante")
        print(f"      - Alternativa: Filtro paso-bajo para eliminar ruido de alta frecuencia")
    else:
        print(f"  [OK] SNR > {snr_threshold} dB -> Senal relativamente limpia")
        print(f"       Filtrado es OPCIONAL; puede proceder directamente a analisis de frecuencia")
    
    print("\n" + "="*70 + "\n")
    
    # ============================================================
    # GRAFICOS - COMPARACION DE PRUEBAS
    # ============================================================
    
    # Definir ruta de salida para el grafico de comparacion
    archivo_comparacion = os.path.join(carpeta_graficos, "Comparacion_Sirena1_vs_Sirena2.png")
    
    graficar_comparacion_seniales(fs1, data1, fs2, data2,
                                  titulo1="Sirena 1",
                                  titulo2="Sirena 2",
                                  metricas1=resultado_1,
                                  metricas2=resultado_2,
                                  archivo_salida=archivo_comparacion)
    
    print(f"\n[OK] Los graficos han sido guardados en la carpeta '{carpeta_graficos}'")
    print(f"  - {archivo_comparacion}")


if __name__ == "__main__":
    main()