import os
import random
import numpy as np
import pickle
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

class RiskEngine:
    def __init__(self):
        self.model_path = os.path.join(os.path.dirname(__file__), 'model', 'risk_model_trained.h5')
        self.token_path = os.path.join(os.path.dirname(__file__), 'model', 'tokenizer.pickle')
        self.model = None
        self.tokenizer = None
        self._load_brain()

    def _load_brain(self):
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.token_path):
                print("[*] Loading LSTM Model and Tokenizer...")
                self.model = tf.keras.models.load_model(self.model_path)
                with open(self.token_path, 'rb') as handle:
                    self.tokenizer = pickle.load(handle)
                print("[+] AI Engine Online.")
            else:
                print("[!] Model artifacts not found. Running in Heuristic Mode.")
        except Exception as e:
            print(f"[!] AI Load Error: {e}")

    def analyze_pr(self, pr_data):
        score = 0.0
        reasons = []
        user = pr_data.get('user', 'unknown')
        if 'bot' in user.lower():
            score += 0.1
            reasons.append("Automated account")
        
        desc_len = len(pr_data.get('body', '') or '')
        if desc_len < 20:
            score += 0.3
            reasons.append("Short description")

        if self.model and self.tokenizer:
            try:
                text = (pr_data.get('title', '') + " " + (pr_data.get('body', '') or ""))
                seq = self.tokenizer.texts_to_sequences([text])
                padded = pad_sequences(seq, maxlen=100, padding='post', truncating='post')
                
                ai_prob_safe = self.model.predict(padded, verbose=0)[0][0]
                ai_risk = 1.0 - ai_prob_safe
                
                score = (score * 0.3) + (ai_risk * 0.7)
                
                if ai_risk > 0.6:
                    reasons.append(f"AI detected anomalous pattern ({int(ai_risk*100)}%)")
            except Exception as e:
                print(f"[!] Inference Error: {e}")

        final_score = min(score, 1.0)
        
        return {
            "risk_score": round(final_score, 2),
            "risk_level": self._classify_risk(final_score),
            "flags": reasons
        }

    def _classify_risk(self, score):
        if score > 0.7: return "CRITICAL"
        if score > 0.4: return "HIGH"
        if score > 0.2: return "MODERATE"
        return "LOW"