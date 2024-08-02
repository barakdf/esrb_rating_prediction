# ESRB Rating Prediction

## Project Overview
This project aims to predict ESRB ratings of video games using two different data sources: the Steam Web API and the "Video Games Rating By 'ESRB'" dataset. The goal is to determine which dataset provides better predictive power and gain insights into the factors influencing ESRB ratings.

## Project Structure
- `data/`: Directory to store raw data files.
- `notebooks/`: Jupyter notebooks for exploratory analysis.
- `src/`: Source code directory.
  - `data_collection.py`: Script for data collection.
  - `data_preprocessing.py`: Script for data preprocessing.
  - `feature_selection.py`: Script for feature selection.
  - `model_training.py`: Script for model training.
  - `evaluation.py`: Script for model evaluation.
- `requirements.txt`: List of dependencies.
- `README.md`: Project description and instructions.

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/esrb_rating_prediction.git
   cd esrb_rating_prediction
