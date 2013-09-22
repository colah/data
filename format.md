A Simple Data Format
--------------------

Every dataset is just a tarball with numpy files and a json manifest. For example, MNIST is stored as `mnist.tgz`, a tarball containing:

```
manifest.json
test_xs.npy
test_ys.npy
train_xs.npy
train_ys.npy
```

The `*.npy` files are of the form `set_data.npy`. `set` is train (training set), valid (validation set), test (test set), etc. `data` is the different data types, typically xs and ys, but others for multi-input and multi-task datasets -- for example CIFAR-100 (`cifar100`), which has coarse and fine labels has data `xs`, `ys1`, `ys2`.

(Numpy files are a very convenient binary format to use in python, efficient and fast to load. It is a simple file format, and has importers for languages other than Python. But you don't have to worry about that! `data` will provide the desired dataset in a large variety of language independent formats.)

The manifest includes a lot of useful meta data. For example, the MNIST manifest:

```json
{
    "info": "The MNIST database of handwritten digits has a training set of 60,000 examples, and a test set of 10,000 e
xamples. It is a subset of a larger set available from NIST. The digits have been size-normalized and centered in a fix
ed-size 28x28 image. (Learn more: http://yann.lecun.com/exdb/mnist/)", 
    "credit": "Yann LeCun, Corinna Cortes, & Christopher J.C. Burges"
    "data": {
        "xs": {
            "human_name": "images", 
            "type": "image", 
            "format": "XY"
        }, 
        "ys": {
            "human_name": "labels", 
            "human_labels": [
                "0", 
                "1", 
                "2", 
                "3", 
                "4", 
                "5", 
                "6", 
                "7", 
                "8", 
                "9"
            ], 
            "type": "label", 
            "format": "index"
        }
    }, 
    "sets": [
        "train", 
        "test", 
        "valid"
    ]
}
```


