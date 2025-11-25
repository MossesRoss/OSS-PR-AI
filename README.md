# OSS PR AI: Automated Pull Request Risk Assessment

## Overview
OSS PR AI is a machine learning-driven tool designed to quantify the "fraud risk" of open-source contributions. By analyzing commit history, contributor reputation, and code patterns, this system provides a real-time risk score (0.0 - 1.0) for maintainers, mitigating supply chain attacks and low-quality spam.

## Key Features
* **Deep Learning Analysis:** Utilizes TensorFlow to detect anomalous patterns in PR diffs.
* **Risk Scoring Engine:** Heuristic + ML hybrid model to evaluate contributor intent.
* **CI/CD Integration:** Designed to run as a GitHub Action.

## Stack
* Python 3.10+
* TensorFlow / Keras
* PyGithub
* Pandas

## Status
* **Current Version:** v0.1.0-alpha (Prototype)
* **License:** MIT
