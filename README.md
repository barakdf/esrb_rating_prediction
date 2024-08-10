# ESRB Rating Prediction
![img.png](images/esrb_example.png)
## Overview
This project aims to predict the Entertainment Software Rating Board (ESRB) ratings of video games using machine learning models. The project explores two different datasets:

- **ESRB Content-Descriptors Dataset:** A dataset that includes content descriptors like violence, alcohol reference, drug reference, etc., directly related to ESRB ratings.
- **Game Descriptions Dataset:** A dataset derived from the Steam API that includes textual descriptions of games.

The goal is to compare the effectiveness of using content descriptors and game descriptions in predicting ESRB ratings and to evaluate the performance of various machine learning models on these datasets.

Additionally, we hope to achieve high accuracy, particularly in predicting content that falls under the Mature (M) rating. Ensuring that M-rated content is accurately identified is critical, as it helps minimize the risk of exposing children to material that may not be suitable for their age group.

## Datasets

### 1. ESRB Content-Descriptors Dataset
- **Source:** Kaggle Dataset
- **Features:** Binary indicators for various content descriptors (e.g., violence, blood, drug reference).
- **Target:** ESRB rating labels (E, ET, T, M).

### 2. Game Descriptions Dataset
- **Source:** Data collected using the Steam API.
- **Features:** Textual descriptions of the games.
- **Target:** ESRB rating labels (E, ET, T, M).
- **Note:** This dataset is smaller due to the unavailability of some games on the Steam store.

## Usage

### ESRB Rating Classification
- **Notebook:** `data/esrb_rating_classification.ipynb`
- **Description:** This notebook covers the analysis, feature extraction, and model training for both the ESRB Content-Descriptors Dataset and the Game Descriptions Dataset. It includes all steps from data preprocessing to model evaluation, allowing for a direct comparison of the effectiveness of different features and machine learning models in predicting ESRB ratings.

## Models
The following models were trained and evaluated on both datasets:

- Logistic Regression
- Decision Tree
- K-Nearest Neighbors (KNN)
- Support Vector Machine (SVM)

## Performance Summary

### Game Descriptions Dataset

| Model                  | Vectorizer      | Training Accuracy | Test Accuracy |
|------------------------|-----------------|-------------------|---------------|
| Logistic Regression     | TF-IDF          | 99.28%            | 48.56%        |
| Logistic Regression     | CountVectorizer | 100.00%           | 50.96%        |
| Decision Tree           | TF-IDF          | 100.00%           | 46.15%        |
| Decision Tree           | CountVectorizer | 100.00%           | 42.79%        |
| K-Nearest Neighbors     | TF-IDF          | 67.43%            | 49.52%        |
| K-Nearest Neighbors     | CountVectorizer | 28.11%            | 18.75%        |
| Support Vector Machine  | TF-IDF          | 100.00%           | 39.90%        |
| Support Vector Machine  | CountVectorizer | 93.12%            | 41.35%        |

### ESRB Content-Descriptors Dataset

| Model                  | Preprocessing | Training Accuracy | Test Accuracy |
|------------------------|---------------|-------------------|---------------|
| Logistic Regression     | PCA           | 83.98%            | 81.21%        |
| Logistic Regression     | Original      | 85.96%            | 83.72%        |
| Decision Tree           | PCA           | 93.01%            | 83.72%        |
| Decision Tree           | Original      | 93.01%            | 84.97%        |
| K-Nearest Neighbors     | PCA           | 86.85%            | 78.71%        |
| K-Nearest Neighbors     | Original      | 86.33%            | 80.17%        |
| Support Vector Machine  | PCA           | 90.34%            | 83.92%        |
| Support Vector Machine  | Original      | 90.66%            | 85.80%        |

## Insights
- The ESRB Content-Descriptors Dataset yielded better overall predictions due to the direct relevance of the features to ESRB ratings.
- The Game Descriptions Dataset was more challenging due to its indirect relationship with ESRB ratings and the complexity of text data. It also suffered from a smaller dataset size.
- K-Nearest Neighbors using TF-IDF and Logistic Regression with CountVectorizer showed the most balanced performance in the game descriptions dataset, but it still did not match the accuracy achieved with the content-descriptor dataset.
- The application of PCA in the ESRB Content-Descriptors Dataset generally resulted in slightly lower accuracy compared to the original data, suggesting that feature reduction might not always be beneficial for this type of dataset.

## Potential Improvements
- **Data Augmentation:** Expanding the game descriptions dataset by including more games or using synthetic data could provide more training examples.
- **Model Tuning:** Applying cross-validation, regularization, or ensemble methods might help reduce overfitting and improve generalization.
