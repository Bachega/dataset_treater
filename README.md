# Dataset Treater

Welcome to the Dataset Treater project! This tool is designed to help pre-process datasets for the Quantifier Recommender project, so it may not be useful to you.

## Features

- **Accepts .CSV and .ARFF datasets**: If the file is .ARFF, it will try to convert it to a .CSV as best as it can.
- **Class Proportion Chart**: It will try to automatically detect the class (binary classes, for now). It will then print the columns of the dataframe that it thinks is the class column, alongside a pie chart of the class proportions.
- **Meta-Features Extraction Test**: Quantifier Recommender is a Meta-learning project, so we need to extract Meta-features. This runs a Meta-feature extraction function on the dataset and warns you if it was successful (or not).
- **Edit and download**: You can edit the dataset freely and download it as a .CSV file.

## Installation

To install Dataset Treater, clone the repository and install the dependencies:

```bash
git clone https://github.com/yourusername/dataset_treater.git
cd dataset_treater
pip install -r requirements.txt
```

Then, you have to run the app:

```bash
streamlit run dataset_treater.py
```

## Usage

This is a web application, so it should be self explanatory.

## Contact

If you have any questions or feedback (or a job opportunity... :D) reach out to me at [guizobachegagomes@gmail.com](mailto:guizobachegagomes@gmail.com).