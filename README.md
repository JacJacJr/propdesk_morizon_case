# Analysis and Prediction of Real Estate Prices in Warsaw

## Project Structure
propdesk/  
├── morizon/  
│   ├── morizon_crawler_html.py  
│   ├── morizon_scrapper_html.py  
│   ├── regex_list.py  
│   ├── find_elem_version_previous *(first approach)*  
│   │   ├── README.md *(morizon)*  
│   │   └── requirements.txt  
├── base_merge/  
│   └── data/  
│   │   └── ....  
│   ├── all_platforms_data.csv  
│   ├── base_merge.ipynb  
│   ├── analyze_housing_data.ipynb  
│   ├── machine_learning.ipynb  
│   ├── district_subdistrict_dict.py  
│   ├── README.md *(base_merge)*  
├── functional_approach *(alpha stage, not ready :)*  
└── README.md *(whole repo)*  

## How It Works

The application is divided into two main parts:

1. **Crawler/Scraping (`morizon`):** Responsible for crawling and scraping real estate listings from the Morizon portal using Python scripts (`morizon_crawler_html.py` and `morizon_scrapper_html.py`). The crawler collects links to individual real estate listings, and the scraper extracts detailed information from each listing.

2. **Merging, analysis, and model implementation (`base_merge`):** Focuses on merging and cleaning data from multiple real estate platforms (Morizon, Otodom, and Nieruchomości Online). Uses Jupyter Notebooks (`base_merge.ipynb` and `machine_learning.ipynb`) to prepare data for analysis, conduct exploratory data analysis, and implement machine learning models to predict real estate prices.

### Workflow

1. **Crawler/Scraping:**
   - Run `morizon_crawler_html.py` to collect URLs of real estate listings.
   - Run `morizon_scrapper_html.py` to extract detailed information from each listing.

2. **Merging and Data Preparation:**
   - Use `base_merge.ipynb` to merge and clean data from Morizon, Otodom, and Nieruchomości Online platforms.
   - Data is deduplicated, cleaned, and prepared for analysis and modeling.

3. **Data Analysis:**
   - Execute `analyze_housing_data.ipynb` to understand data distribution, identify outliers, and perform statistical data analysis.

4. **Machine Learning:**
   - Run `machine_learning.ipynb` to analyze data and train machine learning models to predict real estate prices.
   - Models are compared based on R² metrics, and the best model is saved as `best_model.pkl`.

## File Descriptions

### `README.md`
The main project documentation file, containing a project description, directory structure, and instructions for running the application.

### `morizon_crawler_html.py`
Python script responsible for crawling, i.e., collecting links to real estate listings from the Morizon portal.

### `morizon_scrapper_html.py`
Python script responsible for scraping, i.e., extracting detailed information from individual real estate listings based on the collected URLs.

### `base_merge.ipynb`
Jupyter Notebook responsible for merging data from three real estate platforms into a unified Data Warehouse. Key steps include:
- **Loading Data:** Reading CSV files from Morizon, Otodom, and Nieruchomości Online.
- **Data Cleaning:** Removing duplicates, handling missing values, and normalizing text data.
- **Feature Engineering:** Creating new features and transforming existing ones to prepare data for analysis.
- **Outlier Removal:** Identifying and removing outliers to improve data quality.
- **Saving Clean Data:** Exporting merged and cleaned data to `all_platforms_data.csv` for further analysis.

### `machine_learning.ipynb`
Jupyter Notebook focusing on analyzing cleaned data and implementing various machine learning models to predict real estate prices. Main processes include:
- **Importing Libraries:** Tools for data analysis, visualization, and machine learning.
- **Data Preparation:** Encoding categorical variables, scaling numerical features, and splitting data into training, validation, and test sets.
- **Creating Datasets:** Generating three different datasets with varying levels of transformation.
- **Training Models:** Defining hyperparameter grids and training models using GridSearchCV.
- **Evaluation:** Assessing model performance based on R² metrics.
- **Model Selection:** Identifying the best model and saving it as `best_model.pkl` for future predictions.

### `districts_subdistricts_dict.py`
Dictionary used to normalize district names in real estate data, facilitating analysis and modeling.

### `all_platforms_data.csv`
Merged and cleaned dataset from three real estate platforms, prepared for analysis and training machine learning models.

### `analyze_housing_data.ipynb`
Jupyter Notebook dedicated to exploratory data analysis, understanding distributions, identifying outliers, and calculating descriptive statistics, which helps in better preparing data for modeling.

### `.gitignore`
Git configuration file specifying which files and directories should be ignored by the version control system. Currently ignores system files, Python builds, and the contents of the `ignore/` folder.

## Environment and Installation

### Required Tools
- **Python Version:** 3.10.13
- **Jupyter Notebook**