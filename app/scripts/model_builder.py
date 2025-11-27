import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding, Dropout
import os

def build_dummy_model():
    print("[*] Constructing Neural Network Architecture...")
    # Vocabulary size simulate
    vocab_size = 5000
    embedding_dim = 64
    max_length = 100

    model = Sequential([
        Embedding(vocab_size, embedding_dim, input_length=max_length),
        # enough to run fast
        LSTM(64, return_sequences=False),
        Dropout(0.5),
        Dense(32, activation='relu'),
        Dense(1, activation='sigmoid')
    ])

    print("[*] Compiling Model with Binary Crossentropy Loss...")
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    return model

if __name__ == "__main__":
    model = build_dummy_model()
    model.summary()
    model.save('risk_model.h5')
    print("[+] Model structure serialized to 'risk_model.h5'")

