
# Phishing Website Detector

## 1. Project Overview
The Phishing Website Detector is a machine learning project that analyzes URL characteristics to estimate whether a website URL may be associated with phishing.

The application uses Python, Scikit-learn, and Streamlit to provide an interactive web interface.

## 2. Objectives
- Analyze website URLs using machine learning.
- Extract useful characteristics from a URL.
- Classify URLs as potentially phishing or likely legitimate.
- Display prediction scores and URL characteristics.
- Provide a simple cybersecurity demonstration interface.

## 3. Technologies Used
- Python
- Pandas
- NumPy
- Scikit-learn
- Joblib
- Streamlit

## 4. Dataset
Dataset: PhiUSIIL Phishing URL Dataset.

Source:
https://archive.ics.uci.edu/dataset/967/phiusiil%2Bphishing%2Burl%2Bwebsite%2Bdataset

The training script uses the URL column and the label column.
The classifier is trained using features that can be extracted directly from URL text.

## 5. Machine Learning Algorithm
Random Forest Classifier.

The dataset is divided into training and testing sets using an 80:20 split.

The reported test accuracy from the current training run was approximately 99.51%.

This score is a dataset test result and does not guarantee equivalent performance on new, real-world URLs.

## 6. Project Structure

PhishingWebsiteDetector/
├── dataset/
├── models/
├── src/
│   ├── feature_extraction.py
│   └── train_model.py
├── app.py
├── requirements.txt
└── README.md

## 7. Installation

Create and activate a Python virtual environment, then install dependencies:

    python -m pip install -r requirements.txt

If PowerShell activation is blocked, use the virtual environment's Python executable directly.

## 8. Run the Application

From the main project directory, run:

    python -m streamlit run app.py

Open the local URL displayed in the terminal, usually:

    http://localhost:8501

## 9. How It Works
1. The user enters a URL.
2. The application extracts URL-based features.
3. The saved Random Forest model predicts a class.
4. The application displays the prediction and model scores.
5. URL characteristics are shown for inspection.

## 10. Limitations
- The application analyzes URL text only.
- It does not visit the submitted website.
- Predictions may be incorrect.
- A likely legitimate result does not guarantee that a website is safe.
- Model scores are estimates, not verified real-world probabilities.

## 11. Future Improvements
- Evaluate performance on an independent, newer dataset.
- Improve phishing recall and false-positive analysis.
- Add confusion matrix and precision-recall visualizations.
- Improve URL feature engineering.
- Deploy the application to a hosting platform.

## 12. Conclusion
This project demonstrates how machine learning can be used to analyze URL characteristics and build an interactive phishing-risk classification application.
