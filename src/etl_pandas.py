import pandas as pd
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

CONCURRENCY = cpu_count()

total_rows = 1_000_000_000
chunk_size = 100_000_000
filename = "./db/measurements.txt"

def process_chunk(chunk):
    aggregated = chunk.groupby('station')['measure'].agg(['min', 'max', 'mean']).reset_index()
    return aggregated

def create_df_with_pandas(filename, total_rows, chunk_size=chunk_size):
    total_chunks = total_rows // chunk_size + (1 if total_rows % chunk_size > 0 else 0)
    results = []

    with pd.read_csv(filename, sep=';', header=None, names=['station', 'measure'], chunksize=chunk_size) as reader:
        with Pool(CONCURRENCY) as pool:
            for chunk in tqdm(reader, total=total_chunks, desc="Processing chunks"):
                result = pool.apply_async(process_chunk, (chunk,))
                results.append(result)

            results = [result.get() for result in results]

    final_df = pd.concat(results, ignore_index=True)

    final_aggregated_df = final_df.groupby('station').agg({
        'min': 'min',
        'max': 'max',
        'mean': 'mean'
    }).reset_index().sort_values(by='station')

    return final_aggregated_df

if __name__ == "__main__":
    import time

    print("Iniciando o processamento do arquivo...")
    start_time = time.time()
    df = create_df_with_pandas(filename, total_rows, chunk_size)
    took = time.time() - start_time

    print(df.head())
    print(f"Processamento concluído em {took:.2f} segundos.")
