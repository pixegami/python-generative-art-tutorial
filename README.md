# Python Generative Art Tutorial

![preview](images/pygenarttut.png)

This is a tutorial for creating generative abstract art-work using Python. It is based on a generative art NFT collection I created earlier, called [Machine Psychology](https://www.mach-psy.com/) ([source](https://github.com/pixegami-team/machine-psychology-python-art)). But this tutorial project is simplified and only focuses on using Python to create the image.

## Usage

First make sure you have PIL installed.

```bash
pip install pillow
```

You can run it like this.

```bash
# Generates a collection called 'foo' with 32 pieces into ./output/foo/
python src/generate_art.py -n 32 --collection "foo"
```

It should generate an image like this:

![example_image](images/gamma_image_5.png)
