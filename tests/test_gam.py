"""
Integration test taking in csv of local attributions 
and producing csv of global attributions
"""

import glob
import os

import numpy as np
import pytest

from gam import gam


def test_read_csv():
    g = gam.GAM(attributions_path="tests/test_attributes.csv")
    g._read_local()

    assert hasattr(g, "attributions")
    assert g.attributions.shape == (4, 3)

    assert hasattr(g, "feature_labels")
    assert g.feature_labels == ["a1", "a2", "a3"]


def test_normalize():
    """Tests normalization of attributions from csv"""
    g = gam.GAM(attributions_path="tests/test_attributes.csv")
    g._read_local()

    normalized_attributions = gam.GAM.normalize(g.attributions)

    assert normalized_attributions.shape == g.attributions.shape
    assert not np.any(np.where(normalized_attributions < 0))
    assert normalized_attributions.sum(axis=1)[0] == pytest.approx(1.0)


def test_get_subpopulation_sizes():
    """Tests transformation of membership array into subpopulation sizes"""
    subpopulations = [0, 1, 0, 0, 1, 2, 0]
    subpopulation_sizes = gam.GAM.get_subpopulation_sizes(subpopulations)
    assert subpopulation_sizes == [4, 2, 1]


def test_cluster():
    """Tests subpopulations generated by clustering attributions"""
    g = gam.GAM(attributions_path="tests/test_attributes.csv", init_medoids=None)
    g._read_local()
    # g.normalized_attributions = gam.GAM.normalize(g.attributions)
    g.clustering_attributions = gam.GAM.normalize(g.attributions)
    g._cluster()

    assert len(g.explanations) == 2
    assert g.subpopulation_sizes[0] > 0
    assert g.subpopulation_sizes[1] > 0
    assert len(g.explanations) == 2
    assert g.explanations[0][0][0] == g.feature_labels[0]

    first_explanation_sum = sum([weight for label, weight in g.explanations[0]])
    assert first_explanation_sum == pytest.approx(1)

    second_explanation_sum = sum([weight for label, weight in g.explanations[1]])
    assert second_explanation_sum == pytest.approx(1)


def test_plotting_top2():

    explanations = [
        [("height", 0.3), ("weight", 0.6), ("hair color", 0.1)],
        [("height", 0.05), ("weight", 0.05), ("hair color", 0.9)],
        [("height", 0.9), ("weight", 0.05), ("hair color", 0.05)],
        [("height", 0.3), ("weight", 0.6), ("hair color", 0.1)],
        [("height", 0.05), ("weight", 0.05), ("hair color", 0.9)],
        [("height", 0.9), ("weight", 0.05), ("hair color", 0.05)],
    ]

    g = gam.GAM(attributions_path="tests/test_attributes.csv", k=len(explanations))

    g.explanations = explanations
    fname = "tests/image1"
    g.plot(num_features=2, output_path_base=fname, display=False)

    output = glob.glob(fname + "*")
    assert len(output) > 0
    for ofile in output:
        os.remove(ofile)


def test_plotting_top3():

    explanations = [
        [("height", 0.3), ("weight", 0.6), ("hair color", 0.1)],
        [("height", 0.05), ("weight", 0.05), ("hair color", 0.9)],
        [("height", 0.9), ("weight", 0.05), ("hair color", 0.05)],
        [("height", 0.3), ("weight", 0.6), ("hair color", 0.1)],
        [("height", 0.05), ("weight", 0.05), ("hair color", 0.9)],
        [("height", 0.9), ("weight", 0.05), ("hair color", 0.05)],
    ]

    g = gam.GAM(attributions_path="tests/test_attributes.csv", k=len(explanations))

    g.explanations = explanations
    fname = "tests/image2"
    g.plot(num_features=3, output_path_base=fname, display=False)

    output = glob.glob(fname + "*")
    assert len(output) > 0
    for ofile in output:
        os.remove(ofile)


def test_plotting_2attributes():

    explanations = [
        [("height", 0.05), ("weight", 0.05), ("hair color", 0.9)],
        [("height", 0.9), ("weight", 0.05), ("hair color", 0.05)],
    ]

    g = gam.GAM(attributions_path="tests/test_attributes.csv", k=len(explanations))

    g.explanations = explanations

    fname = "tests/image3"
    g.plot(num_features=2, output_path_base=fname, display=False)

    output = glob.glob(fname + "*")
    assert len(output) > 0
    for ofile in output:
        os.remove(ofile)
