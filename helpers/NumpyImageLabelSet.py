from os import path
import numpy as np
from glob import glob

class NumpyImageLabelSet(object):
    """NumpyImageLabelSet is a dataset helper class that
       makes it easy to work with (possibly labeled) image 
       data stored in numpy arrays.

       It expects data to be split into a number of sets
       (eg. training, test, validation, unsupervised
       training...) and data types (eg. images, or a
       labeling set).

       All data is stored in numpy array files of the form 
       `set_type.npy` where "set" is the set name and "type"
       is the type name. For example, MNIST has the files:

         test_xs.npy
         test_ys.npy
         train_xs.npy
         train_ys.npy

       `xs` are the images and `ys` are the labels. Typically,
       the goal is to create a prediction function mapping xs[n]
       to its label ys[n].

       If there are two different labelings (eg. CIFAR-100 has
       both "coarse" and "fine" labels), one might have `y1s`
       and `y2s` or `ys` and `zs`.

       Not every set needs to contain all types. For example, you
       might have a set for unsupervised training with only `xs`.
    """

    def __init__(self, handle_file):
        """Create an image classification dataset object for
           the dataset with handle `handle_file`.
           
           Recomended Usage:
           > ImageClassificationDataset(__file__)
        """

        # "foo/blah/handle.py" -> "foo/blah/"
        self.path = path.split(handle_file)[0]
        

    def load(self, label_format = "index", image_interval = None):

        assert label_format in ["index", "vector"]

        #     data[  set  ][type] = load("set_type.npy")
        # eg. data["train"]["xs"] = load("train_xs.npy")
        data = {}
        for array_path in glob(path.join(self.path, "*_*.npy")):
            array_name = path.split(array_path)[1][:-4]
            set_name, type_name = array_name.split("_")
            if set_name not in data:
                data[set_name] = {}
            data[set_name][type_name] = np.load(array_path)
        
        # Verify dtype/shape consistency of data types
        dtypes, shapes = {}, {}
        for set_name in data:
            for type_name in data[set_name]:
                if type_name in dtypes:
                    assert dtypes[type_name] == data[set_name][type_name].dtype
                    assert shapes[type_name] == data[set_name][type_name].shape[1:]
                else:
                    dtypes[type_name] = data[set_name][type_name].dtype
                    shapes[type_name] = data[set_name][type_name].shape[1:]
        
        # Modify data as requested
        for set_name in data:
            for type_name in data[set_name]:
                pres = data[set_name][type_name]
                # It's a label
                if len(pres.shape) == 1 and pres.dtype in ["int", "int32", "int64"]:
                    if label_format == "vector":
                        N = pres.max()
                        new_data = np.zeros((len(pres), N))
                        for n in xrange(len(pres)):
                            new_data[n][pres[n]] = 1
                        pres = new_data
                data[set_name][type_name] = pres

        return data



    def reformat(self, format_name, path):
        raise "Installing formats not supported."

