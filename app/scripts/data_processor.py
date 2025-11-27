import pandas as pd
import numpy as np
import os
import json

VOCAB_SIZE = 5000
MAX_LENGTH = 100

def process_data():
    input_file = 'dataset.csv'
    
    if not os.path.exists(input_file):
        print("[!] Run data_collector.py first!")
        return

    print(f"[*] Loading raw text data from {input_file}...")
    df = pd.read_csv(input_file)
    
    df['full_text'] = df['title'].astype(str) + " " + df['body'].astype(str)

    print("[*] Text features extracted. (Tokenization will happen in training)")
    final_df = df[['full_text', 'is_merged', 'files_changed']]
    
    final_df.to_csv('training_data.csv', index=False)
    print(f"[+] processed data saved to 'training_data.csv'. Ready for TensorFlow.")

if __name__ == "__main__":
    process_data()
