
Data: A Package Manager for Datasets
====================================

Tired of searching for datasets? Getting one is as easy as,

```bash
$ data get mnist
```

If you're working in python, you don't even have to do that.

```python
import data
mnist = data.load("mnist")
```

If it isn't already installed, it gets installed on first load.

The data command
-----------------

```
data get [-f format -t target_dir] dataset...
data bibtex dataset...
```

To install MNIST and CIFAR-10 on your computer, run `data get mnist cifar10`.

To install them into a particular directory in the `h5` format, `data get -f h5 -t data/ mnist cifar10`.

To get bibtex entries for MNIST and CIFAR-10, run `data bibtex mnist cifar10`.

To install a dataset we don't support, just give a path or URL. For example, if we didn't support CIFAR-100, you might run: `data get https://s3.amazonaws.com/PyData-colah/cifar100.tgz`

The data library
----------------

The Python data library can be imported as:

```python
import data
```

It provides a load function `data.load` and a list of datasets `data.sets`.

`data.load` takes a dataset name (and optional arguments dependent on the dataset). For example, `data.load("mnist")`. If the dataset isn't supported, you can give a URL instead -- eg. `data.load("https://s3.amazonaws.com/PyData-colah/cifar100.tgz")`.

The result you get is a nested dictionary structure with numpy arrays at the bottom. For example:

```python
>>> D = data.load("mnist")
>>> D.keys()
['test', 'train', 'meta', 'valid']
>>> D["train"].keys()
['xs', 'ys']
>>> D["train"]["xs"].shape
(50000, 28, 28)
```

Adding Datasets Is Simple
-------------------------

Every dataset is just a tarball with numpy files and a json manifest. [Learn More](format.md)

To add a dataset, throw it somewhere fast, reliable and cheap (we use Amazon S3) and submit the URL and a hash to us in a pull request editing `datasets.py`.

