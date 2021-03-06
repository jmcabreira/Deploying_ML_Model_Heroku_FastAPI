import os
import logging
import pytest
from pathlib import Path
import yaml
from box import Box
import pandas as pd
import sys
import pytest

STARTER_OUT_PTH = str(Path(__file__).resolve().parents[1])
ml_path = os.path.join(STARTER_OUT_PTH, "starter", "ml")
sys.path.insert(0, ml_path)

from data import *
from model import *

LOG_FOLDER = os.path.join(STARTER_OUT_PTH, "logs")
CONFIG_FILEPATH = os.path.join(STARTER_OUT_PTH, "config.yaml")
LOG_FILE_PTH = os.path.join(LOG_FOLDER, "unit_test.log")

if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

with open(CONFIG_FILEPATH, "r", encoding="UTF-8") as configfile:
    config = Box(yaml.safe_load(configfile))

CLEANED_DATA_FILEPATH = os.path.join(STARTER_OUT_PTH, config.data.cleaned.filepath)
print("CLEANED_DATA_FILEPATH: ", CLEANED_DATA_FILEPATH)


@pytest.fixture
def data():
    """
    Load the cleaned dataset
    """
    df = pd.read_csv(CLEANED_DATA_FILEPATH).drop(["Unnamed: 0"], axis=1)
    return df


def test_dataframe_shape(data):
    """
    test dataframe shape
    """
    try:
        assert data.shape[0] > 0
        assert data.shape[1] == 15
        logging.info(
            f"Testing the cleaned data: The cleaned dataset has {data.shape[0]} rows and {data.shape[1]} columns as expected."
        )
    except AssertionError as e:
        logging.error(
            f"Testing the cleaned data: The cleaned dataset has {data.shape[0]} rows and {data.shape[1]}."
        )
        raise e


def test_column_names(data):
    """
    test the columns dataset name
    """
    right_columns = [
        "age",
        "workclass",
        "fnlgt",
        "education",
        "education-num",
        "marital-status",
        "occupation",
        "relationship",
        "race",
        "sex",
        "capital-gain",
        "capital-loss",
        "hours-per-week",
        "native-country",
        "salary",
    ]
    data_columns = data.columns.values
    try:
        assert list(right_columns) == list(data_columns)
        logging.info("Testing Cleaned data: Column names are as expected")
    except AssertionError as e:
        logging.error(
            f"Testing cleaned data: Column names are not as expected. Dataset columns: {data_columns}"
        )
        raise e


def test_missing_values(data):
    print(data.isnull().sum())
    try:
        assert data.isnull().sum().sum() == 0
        print(data)
        logging.info("Testing cleaned data: No rows with null values.")
    except AssertionError as e:
        logging.error(
            f"Testing cleaned data: Expected no null values but found {data.isnull().sum()} missing values"
        )
        raise e


def test_question_mark(data):
    """
    Check whether the data has a question mark in it
    """
    try:
        assert "?" not in data.values
        logging.info("Testing the cleaned data: No question mark in cleaned data")
    except AssertionError as e:
        logging.error(f"Testing cleaned data: There is still ? in the clenaed data")
        raise e


# def run_cleaned_tests():
#     df = data()
#     test_dataframe_shape(df)
#     test_column_names(df)
#     test_missing_values(df)
#     test_question_mark(df)


# if __name__ == "__main__":
#     run_cleaned_tests()
