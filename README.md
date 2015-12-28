# Aerospace

This is a package of static and dynamic math-models for aerospace computations.
---
Send your feedback to dondmitriys@gmail.com

## Reqiurements

* Python 2.7
* [Odespy](https://github.com/hplgit/odespy)
* NumPy
* Matplotlib

## Installation

The simplest procedure for installing Aerospace is to use pip:


```bash
$ sudo pip install -e git+https://github.com/zokalo/aerospace.git#egg=aerospace
```

Alternatively, you can check out this repo and run setup.py:


```bash
$ git clone git@github.com:zokalo/aerospace.git
$ cd aerospace
$ sudo python setup.py install
```

If you face problems with requirements try to find solution in the next
subsections.

###Odespy

If you obtain an error:


```bash
\error: library _odepack has Fortran sources but no Fortran compiler found
```

install Fortran compiler, i.e.:


```bash
$ apt-get install gfortan
```

or if you do not have a Fortran compiler, you can install without any 
Fortran code (see Odespy [README](https://github.com/hplgit/odespy/blob/master/README.md))


```bash
$ sudo python setup.py install --no-fortran
```

###NumPy

On Unix NumPy reqiures packages to be preinstalled:

* build-essential
* python-dev

Good solution for Windows the NumPy installer for your Python version from the
[Sourceforge](http://sourceforge.net/projects/numpy/files/NumPy/). The NumPy 
installer includes binaries for different CPU’s (without SSE instructions, 
with SSE2 or with SSE3) and installs the correct one automatically.

###Matplotlib

If you have obtained MemoryError:


```bash
$ pip install --no-cache-dir matplotlib
```

If you have error:


```bash
The following required packages can not be built:
                            * freetype, png
```

on unix install packages:


```bash
$ sudo apt-get install libfreetype6-dev libpng12-dev
$ sudo apt-get install pkg-config
```

## Usage

Use interface functions from app_aerospace.py.
See docstrings for more information about functions and classes.

## History

* **v0.1 (2015-12-26)**
    * Added first model:
        - balloon free lift process.
       
## License

GPL v3.0 License. See the LICENSE file.