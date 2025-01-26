# Analiza i Predykcja Cen Nieruchomości w Warszawie

## Opis Projektu
Projekt został stworzony w celu analizy i przewidywania cen nieruchomości w Warszawie na podstawie danych z trzech głównych portali nieruchomości: Morizon, Otodom i Nieruchomości Online. Wykorzystuje zaawansowane techniki uczenia maszynowego do tworzenia dokładnych prognoz cenowych.

## Struktura Projektu

## Dataset
Data webscrapped from above portals gave around 22k records that had to be deduplicated, cleaned and prepared for Machine Learning which predicts Price attribute. <br />

## Steps

#### 1. Get data from all 3 websites [example in dictionary: morizon]
#### 2. Merge data into a single Data Warehouse by performing minimal transformations and standarization [base_merge.ipynb]
#### 3. Analyze data to understand distribution, outliers and statistics [analyze_housing_data.ipynb]
#### 4. Run machine learning algorithms on cleaned and analyzed data [machine_learning.ipynb]

## File Descriptions

### `README.md`
This file provides an overview of the `base_merge` folder, including the project description, folder structure, and instructions on how to set up and run the application.

### `base_merge.ipynb`
This Jupyter Notebook is responsible for merging data from the three real-estate portals into a unified Data Warehouse. The key steps include:
- **Loading Data:** Reading CSV files from Morizon, Otodom, and Nieruchomości Online.
- **Data Cleaning:** Removing duplicates, handling missing values, and normalizing text data.
- **Feature Engineering:** Creating new features and transforming existing ones to prepare the data for analysis.
- **Outlier Removal:** Identifying and removing outliers to enhance data quality.
- **Saving Cleaned Data:** Exporting the cleaned and merged dataset to `all_platforms_data.csv` for further analysis.

### `machine_learning.ipynb`
This Jupyter Notebook focuses on analyzing the cleaned data and implementing various machine learning models to predict real-estate prices. The main processes include:
- **Importing Libraries:** Tools for data analysis, visualization, and machine learning.
- **Data Preparation:** Encoding categorical variables, scaling numerical features, and splitting the data into training, validation, and testing sets.
- **Dataset Creation:** Generating three different datasets with varying levels of transformation:
  - **Dummies Only:** Utilizing dummy variables without scaling.
  - **Dummies and Scaling:** Applying dummy variables and scaling numerical features.
  - **Dummies, Scaling, and Filtering:** Including dummy variables, scaling, and removing low-correlation features.
- **Model Training:** Defining hyperparameter grids and training models using GridSearchCV for:
  - Random Forest Regressor
  - Gradient Boosting Regressor
  - XGBoost Regressor
  - Linear Regression (as baseline)
- **Evaluation:** Assessing model performance using R² scores on validation and test datasets.
- **Model Selection:** Identifying the best-performing model and saving it as `best_model.pkl` for future predictions.

## Environment Setup

### Required Tools
- **Python Version:** 3.11.4

### Required Libraries
- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `scikit-learn`
- `xgboost`
- `pickle`
- `re`
- `unidecode`
- `unicodedata`

### Installation
Install the required libraries using `pip`. Run the following command in your terminal:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn xgboost unidecode
```

## How to Run the Application

### 1. Data Preparation
Ensure that the CSV files from Morizon, Otodom, and Nieruchomości Online are placed in their respective directories within the `data/` folder:
- `data/morizon/morizon.csv`
- `data/otodom/otodom.csv`
- `data/no/no.csv`

### 2. Merging Data
Open and run the `base_merge.ipynb` notebook using Jupyter Notebook. This will merge the data from the three portals, clean it, and save the unified dataset as `all_platforms_data.csv`.

### 3. Machine Learning
After successfully merging and cleaning the data, open and run the `machine_learning.ipynb` notebook. This will perform the following:
- Analyze the cleaned data.
- Prepare multiple datasets with different transformations.
- Train and evaluate various machine learning models.
- Select and save the best-performing model as `best_model.pkl`.

### 4. Using the Best Model
The saved `best_model.pkl` can be used to make price predictions on new real-estate data. Load the model using `pickle` and apply it to your dataset as needed.

## Additional Information

- **Data Analysis:** The project includes thorough data analysis to understand distributions, identify outliers, and compute descriptive statistics, enabling informed feature engineering and model selection.
- **Data Processing:** The notebooks cover text cleaning, type conversions, creation of binary variables, and scaling of numerical features to prepare the data for effective machine learning.
- **Machine Learning Models:** Various regression algorithms are implemented and compared to determine the most accurate model for predicting real-estate prices in Warsaw.

## Encouragement to Learn
This project was developed as part of a master's thesis in data science, serving as a comprehensive example of applying ETL (Extract, Transform, Load) processes and machine learning techniques to real estate market analysis. The research and implementation demonstrate practical applications of data science methodologies in business contexts. I encourage you to explore the code, experiment with different models and hyperparameters, and deepen your understanding of data processing and modeling techniques used in this academic work.
