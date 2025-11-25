import random

class RiskEngine:
    def __init__(self):
        self.model = None

    def analyze_pr(self, pr_data):
        """
        Analyzes a PR and returns a risk score (0.0 - 1.0).
        Higher score = Higher fraud risk.
        """
        score = 0.0
        reasons = []
        user = pr_data.get('user', 'unknown')
        if 'bot' in user.lower():
            score += 0.1
            reasons.append("Automated account detected")
        desc_len = len(pr_data.get('body', '') or '')
        if desc_len < 20:
            score += 0.4
            reasons.append("Suspiciously short description")
        elif desc_len < 100:
            score += 0.2
            reasons.append("Low detail in description")
        title = pr_data.get('title', '').lower()
        suspicious_keywords = ['update', 'fix', 'typo', 'patch']
        if any(word == title for word in suspicious_keywords):
            score += 0.3
            reasons.append("Generic title patterns")
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
