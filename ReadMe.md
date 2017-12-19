![code coverage](img/coverage.svg)

# Schrödinger Equation Solver: The Variation Method


## Overview
---
<img align="right" width="300"  src="./img/cat.jpg">

Quantum mechanics is the study of small particles, of the order of an atom. Schrödinger equation was developed by Erwin Schrodinger to describe the behaviour of quantum mechanical systems. The Schrödinger equation describes how a quantum system changes with time and characterizes the permitted stationary states of a quantum mechanical system.

<br>
The Schrödinger equation is given by:
<br>

![img](http://latex.codecogs.com/svg.latex?%24%24%5Chat%7BH%7D%5Cpsi%28x%29%3DE%5Cpsi%28x%29%24%24)

![img](http://latex.codecogs.com/svg.latex?%24%24%5Chat%7BH%7D%5Cpsi%28x%29%3D-c%5Cnabla%5E2%5Cpsi%28x%29%2BV_0%5Cpsi%28x%29%24%24)

Where ![img](http://latex.codecogs.com/svg.latex?%5Chat%7BH%7D) is a Hamiltonian operator on a given wave function ![img](http://latex.codecogs.com/svg.latex?%5Cpsi%28x%29), *E* is the energy of the state, ![img](http://latex.codecogs.com/svg.latex?%24%24V_0%24%24) is a constant potential energy, *c* is a constant, and ![img](http://latex.codecogs.com/svg.latex?%5Cnabla%5E2) is the Laplacian. The wave function that satisfies this equation is the one that describes the system.

Variation Method can be used to get approximate solutions for this equation.

## Installation

To install the package, follow the following steps:
```
git clone  https://github.com/hgandhi2411/Schrodinger.git

pip install Schrodinger
```
## Features

This solver can solve the Schrödinger equation for basis sets from Legendre polynomials or Fourier series.
## Usage and Examples

After installation, you can use the entry point 'solver' to start the program and get the basis set coefficients.The following flags/keywords can be used to change the parameters through the command line.

* -V0, --potential: Specify the potential Vo, default is 2.

* -c, --constant: The constant multiplied to the laplacian term in the hamiltonian, default is 0.1.

* -ch, --choice: Specify the type of basis set, choose from Legendre or Fourier. Default is legendre.

* -s, --basis_size: Select the number of basis set elements to use, default is 10.

* -d, --domain: Select the domain over which the basis set should be used, default is [-1,1].

* -y, --wave_function: Give the wave function you want to use, default is cos(x). This should be a python-formatted mathematical string.

* --output_file: Specify the file path to write the output. By default, a file named output.txt is created in the SEq directory.


An example of execution is:
```
$ solver -y x**2+2*x+2 -ch fourier -s 5
```
and in the output you will see:
```
Started!

Done! Please see the output file for results.
```
The output file contains the desired basis set coefficients.

## Documentation
This package uses sphinx documentation library. You will need to have sphinx installed to be able to see the documentation by running the following command:
```
$ sphinx-build -b html .\docs\source .\docs\build
```
After doing this, go to ```docs\build``` directory and open the index.html in your browser.

If you don't have sphinx installed, run
```
$ pip install sphinx
```
in the command line to install it. 
## TODO
* Be able to handle other basis sets.
* Documentation with sphinx is a little erroneous. It documents correctly for some functions but not for others. Need to find out why that is and fix that.
