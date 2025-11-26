import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding, Dropout
import pickle
import os

# Configuration
VOCAB_SIZE = 5000
MAX_LENGTH = 100
EMBEDDING_DIM = 64

def train_brain():
    """
    Trains the LSTM risk scoring model based on the text content of Pull Requests.
    """
    print("[*] Loading Data...")
    if not os.path.exists('training_data.csv'):
        print("[!] ERROR: 'training_data.csv' not found.")
        return

    df = pd.read_csv('training_data.csv', engine='python')

    print("[*] Tokenizing Text...")
    # Converts text into a sequence of integers.
    tokenizer = Tokenizer(num_words=VOCAB_SIZE, oov_token="<OOV>")
    tokenizer.fit_on_texts(df['full_text'].astype(str))
    
    with open('tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    sequences = tokenizer.texts_to_sequences(df['full_text'].astype(str))
    # Pads sequences to the same length.
    padded = pad_sequences(sequences, maxlen=MAX_LENGTH, padding='post', truncating='post')
    
    labels = np.array(df['is_merged'])
    
    print("[*] Constructing LSTM Architecture...")
    # Defines the LSTM model architecture.
    model = Sequential([
        Embedding(VOCAB_SIZE, EMBEDDING_DIM),
        LSTM(64),
        Dropout(0.5),
        Dense(32, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    print("[*] Starting Training Session...")
    # Trains the model on the preprocessed data.
    model.fit(padded, labels, epochs=5, verbose=1)
    
    # Saves the trained model for future use.
    model.save('risk_model_trained.h5')
    print("[SUCCESS] Model trained and saved to 'risk_model_trained.h5'")

    try:
        from google.colab import files
        print("[*] Detected Colab environment. Downloading artifacts...")
        files.download('tokenizer.pickle')
        files.download('risk_model_trained.h5')
    except ImportError:
        print("[*] Local environment detected. Files saved to disk.")

if __name__ == "__main__":
    train_brain()
