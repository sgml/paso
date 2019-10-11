# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Bruce_H_Cottman"
__license__ = "MIT License" ""
import warnings

warnings.filterwarnings("ignore")
import pytest
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification

# paso imports
from paso.base import PasoError, Paso, DataFrame_to_Xy
from paso.pre.cleaners import Balancers, Augmenters, Imputers, Cleaners
from paso.pre.inputers import Inputers


def create_dataset(
    n_samples=1000, weights=(0.01, 0.01, 0.98), n_classes=3, class_sep=0.8, n_clusters=1
):
    return make_classification(
        n_samples=n_samples,
        n_features=2,
        n_informative=2,
        n_redundant=0,
        n_repeated=0,
        n_classes=n_classes,
        n_clusters_per_class=n_clusters,
        weights=list(weights),
        class_sep=class_sep,
        random_state=0,
    )


x_pd, y_pg = create_dataset(n_samples=1000, weights=(0.1, 0.2, 0.7))


session = Paso(parameters_filepath="../../parameters/lesson.1.yaml").startup()

# 1
def test_transform_Values_to_nan_no_passed_arg_type_error():
    g = Cleaners()
    with pytest.raises(TypeError):
        g.transform_Values_to_nan()


# 2
def test_transform_Values_to_nan_passed_arg_type_error(City):
    g = Cleaners()
    with pytest.raises(TypeError):
        g.transform_Values_to_nan(City, values=[], unplace=False, verbose=False)


# 3
def test_transform_Values_to_nan_none(City):
    g = Cleaners()
    assert (
        g.transform_Values_to_nan(City, inplace=True, values=[]).isnull().sum().sum()
        == 0
    )


# 4
def test_transform_Values_to_nan_list0_0(City):
    g = Cleaners()
    assert (
        g.transform_Values_to_nan(City, inplace=True, values=[0.0]).isnull().sum().sum()
        == 843
    )


# 5
def test_transform_Values_to_nan_0_0(City):
    g = Cleaners()
    assert (
        g.transform_Values_to_nan(City, inplace=True, values=0.0).isnull().sum().sum()
        == 843
    )


# 6
def test_transform_Values_to_nan_0_0_ne(City):
    g = Cleaners()
    assert (
        (g.transform_Values_to_nan(City, inplace=False, values=0.0) != City).any().any()
    )


# 7
def test_transform_Delete_NA_Features_to_999_2(City):
    g = Cleaners()
    City["bf"] = 999
    City["bf2"] = 2
    g.transform_Values_to_nan(City, inplace=True, values=[2, 999])
    assert (
        g.transform_Delete_NA_Features(City, inplace=True, threshold=0.8).shape[1] == 14
    )


# 8
def test_transform_Delete_NA_Features_to_999(City):
    g = Cleaners()
    City["bf"] = 999
    City["bf2"] = 2
    z = City.shape[1] - 1
    g.transform_Values_to_nan(City, inplace=True, values=[2])
    assert (
        g.transform_Delete_NA_Features(City, inplace=True, threshold=0.8).shape[1] == z
    )


# 10
def test_transform_Delete_NA_Features_to1_threshold(City):
    g = Cleaners()
    City["bf"] = 999
    City["bf2"] = 2
    z = City.shape[1] - 0
    g.transform_Values_to_nan(City, inplace=True, values=[-1])
    assert (
        g.transform_Delete_NA_Features(City, inplace=True, threshold=1.0).shape[1] == z
    )


# 11
def test_transform_Delete_NA_Features_to_big_threshold(City):
    g = Cleaners()
    City["bf"] = 999
    City["bf2"] = 2
    z = City.shape[1] - 0
    g.transform_Values_to_nan(City, inplace=True, values=[2])
    with pytest.raises(PasoError):
        assert (
            g.transform_Delete_NA_Features(City, inplace=True, threshold=1.1).shape[1]
            == z
        )


# 12
def test_transform_Calculate_NA_ratio(City):
    g = Cleaners()
    City["bf"] = 999
    City["bf2"] = 2
    z = City.columns
    g.transform_Values_to_nan(City, inplace=True, values=[2, 999])
    c = g.transform_Calculate_NA_ratio(City, inplace=True).columns
    assert len(c) == 17


# 13
def test_transform_Calculate_NA_has_NA_ratio(City):
    g = Cleaners()
    City["bf"] = 999
    City["bf2"] = 2
    z = City.columns
    g.transform_Values_to_nan(City, inplace=True, values=[2, 999])
    c = g.transform_Calculate_NA_ratio(City, inplace=True).columns
    assert "NA_ratio" in c


# 14
def test_transform_Calculate_NA_has_NA_ratio(City):
    g = Cleaners()
    City["bf"] = 999
    City["bf2"] = 2
    z = City.columns
    g.transform_Values_to_nan(City, inplace=True, values=[2, 999])
    c = g.transform_Calculate_NA_ratio(City, inplace=True)["NA_ratio"].sum()
    assert c == 2.047430830039525


# 15
def test_transform_delete_Duplicate_Featuress(City):
    g = Cleaners()
    City["bf"] = 999
    City["bf2"] = City["bf"]
    assert g.transform_delete_Duplicate_Features(City, inplace=True).shape[1] == 15


# 15b
def test_transform_delete_Duplicate_Featuress4(City):
    g = Cleaners()
    City["bf"] = 999
    City["bf4"] = City["bf3"] = City["bf2"] = City["bf"]
    assert g.transform_delete_Duplicate_Features(City, inplace=True).shape[1] == 15


# 16
def test_cleaner_statistics(City):
    g = Cleaners()
    assert g.statistics() == [
        "kurt",
        "mad",
        "max",
        "mean",
        "median",
        "min",
        "sem",
        "skew",
        "sum",
        "std",
        "var",
        "nunique",
        "all",
    ]


# 17
def test_transform_Features_Statistics_bad_arg(City):
    g = Cleaners()
    with pytest.raises(PasoError):
        g.transform_Features_Statistics(
            City, concat=False, statistics=[" sum"], inplace=True, verbose=True
        )


# 18
def test_transform_Features_Statistics_3_stats(City):
    g = Cleaners()
    c = g.transform_Features_Statistics(
        City,
        concat=False,
        statistics=["sum", "mean", "kurt"],
        inplace=True,
        verbose=True,
    )
    assert c.shape == (3, 14)


# 19
def test_transform_Features_Statistics_mean(City):
    g = Cleaners()
    c = g.transform_Features_Statistics(
        City, concat=False, statistics=["mean"], inplace=True, verbose=True
    )
    assert c.shape == (1, 14)


# 20
def test_transform_Features_Statistics_all(City):
    g = Cleaners()
    c = g.transform_Features_Statistics(
        City, concat=False, statistics=["all"], inplace=True, verbose=True
    )
    assert c.shape == (12, 14)


# 21
def test_transform_Features_Statistics_3_stats_concat(City):
    g = Cleaners()
    c = g.transform_Features_Statistics(
        City,
        concat=True,
        statistics=["sum", "mean", "kurt"],
        inplace=True,
        verbose=True,
    )
    assert c.shape == (509, 14)


# 22
def test_transform_Features_with_Single_Unique_Value3(City):
    g = Cleaners()
    City["bf"] = 999
    City["bf2"] = 2
    City["bf3"] = 1
    assert (
        g.transform_Features_with_Single_Unique_Value(City, inplace=True).shape[1] == 14
    )


# 23
def test_transform_Features_with_Single_Unique_Value_ignore(City):
    g = Cleaners()
    City["bf"] = 999
    City["bf2"] = 2
    City["bf3"] = 1
    assert (
        g.transform_Features_with_Single_Unique_Value(
            City, ignore=["bf3"], inplace=True
        ).shape[1]
        == 15
    )


# 24
def test_transform_Feature_Correlation(City):
    g = Cleaners()
    g.plot_corr(City)
    assert g.transform_Feature_Feature_Correlation(
        City, verbose=True, inplace=True
    ).shape == (14, 14)


# 25
def test_transform_Feature_Correlation_flowers(flower):
    g = Cleaners()
    g.plot_corr(flower, kind="visual")
    assert g.transform_Feature_Feature_Correlation(
        flower, verbose=True, inplace=True
    ).shape == (5, 5)


# 26
def test_transform_delete_Features_null(flower):
    g = Cleaners()
    assert g.transform_delete_Features(flower, verbose=True, inplace=True).shape == (
        150,
        5,
    )


# 27
def test_transform_delete_Features_all(flower):
    g = Cleaners()
    assert g.transform_delete_Features(
        flower, features=flower.columns, verbose=True, inplace=True
    ).shape == (150, 0)


# 28
def test_transform_delete_Features_but12(City):
    g = Cleaners()
    assert g.transform_delete_Features(
        City, features=City.columns[3:5], verbose=True, inplace=True
    ).shape == (506, 12)


# 29
def test_transform_delete_Features_not_in_train_or_test(City):
    g = Cleaners()
    train = City.copy()
    City["bf"] = 999
    City["bf2"] = 2
    City["bf3"] = 1
    test = City.copy()
    g.transform_delete_Features_not_in_train_or_test(
        train, test, ignore=["bf3"], inplace=True
    )
    assert train.shape[1] == (test.shape[1] - 1)


# 29
def test_Balancer_classBalancer():
    assert Balancers().balancers() == [
        "RanOverSample",
        "SMOTE",
        "ADASYN",
        "BorderLineSMOTE",
        "SVMSMOTE",
        "SMOTENC",
        "RandomUnderSample",
        "ClusterCentroids",
        "NearMiss",
        "EditedNearestNeighbour",
        "RepeatedEditedNearestNeighbours",
        "CondensedNearestNeighbour",
        "OneSidedSelection",
    ]


# 30
def test_Balancer_read_parameters_file_not_exists(City):
    o = Balancers()
    with pytest.raises(PasoError):
        o.transform(City[City.columns.difference(["MEDV"])], City["MEDV"]).shape == []


# 31
def test_Balancer_Smote_Flowers(flower):
    o = Balancers(description_filepath="../../descriptions/pre/cleaners/SMOTE.yaml")
    X, y = DataFrame_to_Xy(flower, "TypeOf")
    X, y = o.transform(X, y)
    assert X.shape == (150, 4) and y.shape == (150,)


# 32
def test_Augmenter_no_Ratio(flower):
    o = Augmenters(
        description_filepath="../../descriptions/pre/cleaners/most_frequent_impute.yaml"
    )
    X, y = DataFrame_to_Xy(flower, "TypeOf")
    with pytest.raises(PasoError):
        assert o.transform(X, y) == 0


# 33
def test_Augmenter_Smote_Flower_ratio_0(flower):
    o = Augmenters(description_filepath="../../descriptions/pre/cleaners/SMOTE.yaml")
    X, y = DataFrame_to_Xy(flower, "TypeOf")
    X, y = o.transform(X, y, ratio=0.0)
    assert X.shape == (150, 4) and y.shape == (150,)


# 34
def test_Augmenter_Smote_Flower_ratio_1(flower):
    o = Augmenters(description_filepath="../../descriptions/pre/cleaners/SMOTE.yaml")
    X, y = DataFrame_to_Xy(flower, "TypeOf")
    X, y = o.transform(X, y, ratio=1.0)
    assert X.shape == (300, 4) and y.shape == (300,)


# 34
def test_Augmenter_bad_ratio(flower):
    o = Augmenters(description_filepath="../../descriptions/pre/cleaners/SMOTE.yaml")
    X, y = DataFrame_to_Xy(flower, "TypeOf")
    with pytest.raises(PasoError):
        o.transform(X, y, ratio=2.0)


# 35
# def test_Balancer_nbad_key(flower):
#     o = Balancers(description_filepath="../../descriptions/pre/cleaners/SMOTE.yaml")
#     X,y = DataFrame_to_Xy(flower,"TypeOf")
#     X, y = o.transform(X, y, xratio= 1.0)
#     with pytest.raises(PasoError):
#         assert (X.shape == (300, 4) and y.shape == (300, ))


# 36
def test_imputer_features_no_given():
    o = Inputers(description_filepath="../../descriptions/pre/inputers/yeast3.yaml")
    train = o.transform(dataset="train")
    imp = Imputers(
        description_filepath="../../descriptions/pre/cleaners/most_frequent_impute.yaml"
    )
    with pytest.raises(PasoError):
        train = imp.transform(train, inplace=True, verbose=True)


# 37
def test_imputer_features_not_found():
    o = Inputers(description_filepath="../../descriptions/pre/inputers/yeast3.yaml")
    train = o.transform(dataset="train")
    imp = Imputers(
        description_filepath="../../descriptions/pre/cleaners/most_frequent_impute.yaml"
    )
    with pytest.raises(PasoError):
        train = imp.transform(
            train, features=["bad", "badder", "Alm"], inplace=True, verbose=True
        )


# 38
def test_imputer_features_not_found():
    o = Inputers(description_filepath="../../descriptions/pre/inputers/yeast3.yaml")
    train = o.transform(dataset="train")
    train.loc[0, "Alm"] = np.NaN
    imp = Imputers(
        description_filepath="../../descriptions/pre/cleaners/most_frequent_impute.yaml"
    )
    assert (
        imp.transform(train, features=["Alm"], inplace=True, verbose=True)
        .isnull()
        .all()
        .all()
    ) == False


# 39
def test_imputer_features_allnans():
    o = Inputers(description_filepath="../../descriptions/pre/inputers/yeast3.yaml")
    train = o.transform(dataset="train")
    train["Alm"] = np.NaN
    train.loc[0, "Alm"] = 0
    imp = Imputers(
        description_filepath="../../descriptions/pre/cleaners/most_frequent_impute.yaml"
    )
    assert (
        imp.transform(train, features=["Alm"], inplace=True, verbose=True)
        .isnull()
        .all()
        .all()
    ) == False


# 40
def test_imputer_features_nans_found():
    o = Inputers(description_filepath="../../descriptions/pre/inputers/yeast3.yaml")
    train = o.transform(dataset="train")
    train["bad"] = np.NaN
    imp = Imputers(
        description_filepath="../../descriptions/pre/cleaners/most_frequent_impute.yaml"
    )
    assert (
        imp.transform(train, features=["Alm"], inplace=True, verbose=True)
        .isnull()
        .any()
        .any()
    ) == True


# 41
def test_transform_boo_lnone(City):
    g = Cleaners()
    train = City.copy()
    g.transform_booleans(train, inplace=True)
    assert (train == City).all().all()


# 41
def test_transform_booL_some(City):
    o = Inputers(description_filepath="../../descriptions/pre/inputers/yeast3.yaml")
    train = o.transform(dataset="train")
    g = Cleaners()
    train["Alm"] = False
    train.loc[0, "Alm"] = True
    assert g.transform_booleans(train, inplace=True).loc[0, "Alm"] == 1


# 41
def test_transform_booL_some_not_true(City):
    o = Inputers(description_filepath="../../descriptions/pre/inputers/yeast3.yaml")
    train = o.transform(dataset="train")
    g = Cleaners()
    train["Mcg"] = True
    train.loc[0, "Mcg"] = False
    train["Alm"] = False
    train.loc[0, "Alm"] = True
    assert (
        g.transform_booleans(train, inplace=True).loc[0, "Alm"] == 1
        and train.loc[0, "Mcg"] == 0
    )
