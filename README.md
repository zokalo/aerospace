# Aerospace
Calculator for aerospace static and dynamic math-models.

---
Send your feedback to dondmitriys@gmail.com

## Reqiurements
* Python 2.7
* [Odespy](https://github.com/hplgit/odespy)
* NumPy
* Matplotlib

## Installation
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
On unix it reqiures packages to be preinstalled:

* build-essential
* python-dev

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