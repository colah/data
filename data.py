
import imp
import os
import tarfile
import shutil
import urllib2

datasets = {
    "mnist"    : "https://s3.amazonaws.com/PyData-colah/mnist.tgz",
    "cifar10"  : "https://s3.amazonaws.com/PyData-colah/cifar10.tgz",
    "cifar100" : "https://s3.amazonaws.com/PyData-colah/cifar100.tgz" }

def download_file(url, file_name):
    """Download a file with a progress bar.
       Based on http://stackoverflow.com/a/22776"""

    u = urllib2.urlopen(url)
    f = open(file_name, 'w')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,

    f.close()

def get_dataset_paths():
    """Return dataset paths, making sure a path is created if
    none exist.

    Example return: ["/home/USER/.pydata/"]

    """

    paths = []

    home = None
    if "HOME" in os.environ:
        home = os.environ["HOME"]

    if os.path.exists("data/"):
        paths.append(os.path.abspath("data/"))
    if "DATASET_PATH" in os.environ.keys():
        pathes.append(os.path.abspath(os.environ["DATASET_PATH"]))
    if home and os.path.exists(os.path.join(home, ".pydata/")):
        paths.append(os.path.join(home, ".pydata/"))
    if not paths:
        print "Can't determine dataset path."
        if home:
            path = os.path.join(home, ".pydata/")
        else:
            path = os.path.join(os.path.abspath("."), "data/")
        print "Assuming ", path
        print "Creating ", path
        os.mkdir(path)
        paths = [path]
    return paths

def get_installed_datasets(paths):
    """Return {dataset: dataset_path} hash from searching `paths`."""

    datasets = {}
    for path in paths:
        for name in os.listdir(path):
            datasets[name] = os.path.join(path, name)
    return datasets

def get_dataset_handle(name, path):
    return imp.load_source(name + ".handle", os.path.join(path, "handle.py") )

def install_dataset(base_path, name, url):
    """ Install dataset from `url` into `base_path/name`. We assume it isn't already installed.
        A few temporary files, `data.tgz` and `work/` are created in base_path during the installation.
    """
    
    install_path  = os.path.join(base_path, name)
    download_path = os.path.join(base_path, "data.tgz")
    work_path     = os.path.join(base_path, "work")
    
    print "Downloading dataset from %s..." % url
    download_file(url, download_path )
    
    print "Extracting dataset..."
    os.mkdir(work_path)
    with tarfile.open(download_path) as tarball:
        tarball.extractall(work_path)
    
    print "Installing dataset..."
    work_contents = os.listdir(work_path)
    if len(work_contents) == 1 and os.path.isdir(os.path.join(work_path, work_contents[0])):
        shutil.move(os.path.join(work_path, work_contents[0]), install_path)
    else:
        shutil.move(work_path, install_path)
    helper_path = os.path.join(os.path.split(__file__)[0], "helpers/")
    os.symlink(helper_path, os.path.join(install_path, "helpers"))

    #Clean up...
    os.remove(download_path)
    shutil.rmtree(work_path)

def load(name):
    """ """

    if name[:4] in ["http", "file"] and "://" in name:
        url  = name
        compname = hex(hash(name))[2:].upper()
    else:
        url = None 
        compname = name
    base_paths = get_dataset_paths()
    installed_datasets = get_installed_datasets(base_paths)
    if not compname in installed_datasets:
        if not url:
            if not name in datasets:
                raise "Can't install unknown dataset: %s" % name
            url = datasets[compname]
        path = os.path.join(base_paths[0], compname)
        install_dataset(base_paths[0], compname, url)
    else:
        path = installed_datasets[compname]
    handle = get_dataset_handle(compname, path)
    data = handle.load()
    return data
        
            


