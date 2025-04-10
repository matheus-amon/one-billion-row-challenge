from csv import reader
from collections import defaultdict
from pathlib import Path
import time

def process_temp(txt_path: Path):
    print("Iniciando o processamento do arquivo...")

    start_time = time.time()
    station_temps = defaultdict(list)

    with open(txt_path, 'r', encoding="utf-8") as file:
        _reader = reader(file, delimiter=';')
        for row in _reader:
            station, temp = str(row[0]), float(row[1])
            station_temps[station].append(temp)

    print("Dados carregados. Calculando estatísticas...")

    results = {}

    for station, temps in station_temps.items():
        min_temp = min(temps)
        mean_temp = sum(temps) / len(temps)
        max_temp = max(temps)
        results[station] = (min_temp, mean_temp, max_temp)

    print("Estatísticas calculadas. Ordenando...")

    sorted_results = dict(sorted(results.items()))
    formatted_results = {
        station: (f"{stats[0]:.1f}", f"{stats[1]:.1f}", f"{stats[2]:.1f}")
        for station, stats in sorted_results.items()
    }

    end_time = time.time()
    print(f"Processamento concluído em {end_time - start_time:.2f} segundos.")

    return formatted_results

if __name__ == "__main__":
    TXT_PATH: Path = "./db/measurements.txt"
    processed_data = process_temp(TXT_PATH)
