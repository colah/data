
"""
`handle.py` is the only mandatory file in a dataset tarball.
The rest of the files are completely up to the packager's
discretion on how to best represent the data. The data may be
stored in any file format you find appropriate.

`handle.py`, then, has an essential role of being a bridge
between the data stored in an unstandardized format and our
package manager. It must describe *how* to use the data.

There are three mandatory values that must be implemented:

* manifest   -- A hash providing meta-data.
* load()     -- A function to actually load the dataset.
* reformat() -- A function to reformat the data into other
                formats you might support

(More details on these are provided below.)

Ideally, you should not need to actually implement `load()`
and `reformat()`. For lots of common scenarios, we provide
dataset helpers, which you can import to handle common 
types of data.

Using a dataset helper is strongly preferable to writing your
own. This is because of the following benefits:

* It makes security reviews of your dataset easier.
* Standardization makes behavior more predictable.
* Less code means less bugs, and that bugs are found faster.
* It is easier to add new load transformations or add support
  for reformatting the data into new formats.

"""

manifest = {
        "info": None, 
        "credit": None
    }

def load(**kwds):
   """ `load(**kwds)` should load the dataset. `**kwds` may 
      describe simple specifications on how the data should
      be formatted or transformations that should be preformed
      such as normalization.

      The object returned should be a natural python object and
      easy to work with and explore. Frequently, it will be a
      hash with entries for different subsets of the dataset,
      such as a training and test set in machine learning.
   """
   pass

def reformat(name, path):
   """ `reformat(name, path)` should install the data in format
      `name` to `path`. If it does not support format `name`, it
      should raise an exception. Always raising an exception is
      a perfectly valid implementation. 
   """
   pass
