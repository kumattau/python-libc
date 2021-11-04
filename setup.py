from setuptools import setup


def get_metadata(file, key):
    with open(file, "r") as fp:
        for line in fp:
            if line.startswith(key):
                return eval(line.split("=")[-1])
    raise ValueError("can not find {} in {}".format(key, file))


metadata_file = "libc/libc.py"

setup(
    version=get_metadata(metadata_file, "__version__"),
)
