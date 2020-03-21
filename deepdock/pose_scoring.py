"""
Scores protein-ligand poses using DeepChem.
"""
import numpy as np
import os
import tempfile
from subprocess import call
from moleculenet.data import NumpyDataset
from moleculenet.featurizers import RdkitGridFeaturizer


class PoseScorer(object):
  """Abstract superclass for all scoring methods."""

  def score(self, protein_file, ligand_file):
    """Returns a score for a protein/ligand pair."""
    raise NotImplementedError


class GridPoseScorer(object):

  def __init__(self, model, feat="grid"):
    """Initializes a pose-scorer."""
    self.model = model
    if feat == "grid":
      self.featurizer = RdkitGridFeaturizer(
          voxel_width=16.0,
          # TODO: add pi_stack and cation_pi to feature_types (it's not trivial
          # because they require sanitized molecules)
          # feature_types=["ecfp", "splif", "hbond", "pi_stack", "cation_pi",
          # "salt_bridge"],
          feature_types=["ecfp", "splif", "hbond", "salt_bridge"],
          ecfp_power=9,
          splif_power=9,
          flatten=True)
    else:
      raise ValueError("feat not defined.")

  def score(self, protein_file, ligand_file):
    """Returns a score for a protein/ligand pair."""
    features, _ = self.featurizer.featurize_complexes([ligand_file],
                                                      [protein_file])
    dataset = NumpyDataset(X=features, y=None, w=None, ids=None)
    score = self.model.predict(dataset)
    return score
