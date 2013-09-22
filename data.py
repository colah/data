"""
data
~~~~
A machine learning dataset in python. Functions load a 
variety of datasets.

If the dataset is not installed, we automically install 
it. No more searching for where to download datasets.
"""

# Standard library
import json
from glob import glob
import os
import random
from subprocess import call

# Third-party libraries
import numpy as np


def get_dataset_path():
    """Return the dataset path, making sure the path is created if it
    doesn't exist."""

    def force_slash(path):
        """Return `path`, ensuring it ends with a '/'.
           For example: foo/test -> foo/test/"""
        if path[-1] != "/":
            return path + "/"
        return path

    home = None
    if "HOME" in os.environ:
        home = force_slash(os.environ["HOME"])

    if os.path.exists("data/"):
        return force_slash(os.path.abspath("data/"))
    elif home and os.path.exists(home + ".pydata/"):
        return home + ".pydata/"
    elif "DATASET_PATH" in os.environ.keys():
        return force_slash(os.path.abspath(os.environ["DATASET_PATH"]))
    else:
        print "Can't determine dataset path."
        print "Assuming ./data/"
        wd = os.path.abspath(".")
        path = force_slash(wd) + "data/"
        print "Creating ", path
        os.mkdir(path)
        return path

def unpickle(filename):
    """
    Return the unpickled file ``filename``.
    """ 
    f = open(filename, 'rb')
    data = json.load(f)
    f.close()
    return data

def vector(n,m):
    """
    Return a unit vector of length n, with a 1 in the m'th location.
    """ 
    v = np.zeros(n).astype('float32')
    v[m] = 1
    return v

def setup(name, url, path):
    """ Install dataset `name`, if necessary, from `url` into `path`.
    """
    # If the data set is already installed
    # (we infer this from its path existing)
    # we're done!
    if os.path.exists(path):
        return
    else:
        raise "no setup yet"

def process_image(image, features_last = False, max_intensity = 255, float_type = 'float32', **kwds):
    if len(image.shape) == 3:
        if features_last:
            image = image.swapaxes(0, 2)
    image = image.astype(float_type)
    image = image/float(max_intensity)
    return image

def process_label(label, num_labels, label_format = "vector", **kwds):
    if   label_format == "vector":
        return vector(num_labels, label)
    elif label_format == "index":
        return label

#def process_data(data, type = None,  **kwds):


def load_path(path):
    manifest = unpickle(path + "manifest.pkl")
    data = {"meta" : {}}
    for d in manifest["data"]:
        data["meta"][d] = {"type" : manifest["data"][d]["type"]}
        if "human_labels" in manifest["data"][d]:
            data["meta"][d]["human_labels"] = manifest["data"][d]["human_labels"]
    for s in manifest["sets"]:
        data[s] = {}
        for d in manifest["data"]:
            data[s][d] = np.load(path + s + "_" + d + ".npy")
    return data

a = load_path(get_dataset_path() + "mnist/")
