import numpy as np
from numpy.polynomial import legendre
import argparse
from math import *
import matplotlib.pyplot as plt

def create_parser():
    '''Creating a parser for command line options for this solver'''
    parser = argparse.ArgumentParser(description = "Inputs to the Schrodinger Equation solver")
    parser.add_argument('-V0', '--potential', nargs = '?', type = float, default = 2, help = 'Constant potential energy, default = 0.1')
    parser.add_argument('-c', '--constant', nargs = '?', type = float, default = 1, help = 'Constant multiplier for the laplacian term of the hamiltonian, default = 1')
    parser.add_argument('-s', '--basis_size', nargs = '?', type = int, default = 10, help = 'Size of the basis set, default = 3')
    parser.add_argument('-ch', '--basis_choice', nargs = '?', type = str, default = 'Legendre', choices = ['Legendre', 'legendre', 'Fourier', 'fourier'], help = 'Choice of basis set - Fourier or Legendre, default = Legendre')
    parser.add_argument('-d', '--domain', nargs = '?', type = tuple, default = (-1, 1), help = 'Domain for the basis set, default = [-1, 1]. Please input a tuple.')
    parser.add_argument('-y', '--wave_function', nargs = '?', type = str, default = 'cos(x)', help = 'Specify a guess for the wave function, default = cos(x). Expression for wave function must be written as a python-formatted mathematical string.')
    parser.add_argument('--output_file', nargs = '?', type = str, default = './SEq/output.txt', help = 'Specify file path where you want output, default = \'./SEq/output.txt\' ')
    return parser

def wave_function(wave_function, x):
    '''This function evaluates the string-formatted function for given x.

    Parameters
    -----
    wave_function: string
        A python string-formatted function, y(x)
    x: array
        The points in domain at which wave_function is evaluated

    Returns
    -----
    array
        An array of function values at given x's. It has the same length as x.
    ''' 
    y = eval(wave_function)
    return y

def basis_set(ch, x, y, basis_size):
    '''Depending on the user choice, basis set elements are returned.
    
    Parameters
    -----
    ch: string
        Selection of type of basis set - Legendre or Fourier
    x: array
        Array of points in domain
    y: array
        Wave function evaluated at x
    basis_size: int
        No of elements in the basis set
    
    Returns
    -----
    array
        Array of basis set elements
    '''
    if(ch == 'Legendre' or ch == 'legendre'):
        basis_set = np.polynomial.legendre.legfit(x, y, basis_size - 1)
    elif(ch == 'Fourier' or ch == 'fourier'):
        basis_set = [fourier_coeff(i, x, y) for i in range(basis_size)]
    return basis_set

def fourier_coeff(n, x, y):  #Source: https://stackoverflow.com/questions/4258106/how-to-calculate-a-fourier-series-in-numpy
    '''Fourier coefficient calculation of the nth term.

    Parameters
    -----
    n: int
    x: array
        Array of points in domain
    y: array
        Wave function evaluated at x

    Return
    -----
    float
        The nth coefficient of the fourier series
    '''
    period = np.amax(x) - np.amin(x)
    c = y*np.exp(-1j*2*n*np.pi*x/period)
    return np.sum(c)/float(len(c))

def hamiltonian(ch, x, y, c, V0, basis_set):
    '''Returns the hamiltonian of the given basis set.
    
    Parameters
    -----
    ch: string
        Selection of type of basis set - Legendre or Fourier
    x: array
        Array of points in domain
    y: array
        Wave function evaluated at x
    c: float
        constant in the hamiltonian expression
    V0: float
        constant potential in the hamiltonian
    basis_set: array
        Array of the basis set elements
    
    Returns
    -----
    array
        The set of hamiltonian coefficients of the given basis set
    '''
    basis_size = len(basis_set)
    if(ch == 'Legendre' or ch == 'legendre'):
        del2_basis = np.polynomial.legendre.legder(basis_set, m = 2)
        del2_basis = np.append(del2_basis, [0,0])
    elif(ch == 'Fourier' or ch == 'fourier'):
        del2_basis = np.gradient(np.gradient(basis_set)) #np.gradient uses central difference method to give the derivative.
    h = [-c * del2_basis + V0 * np.array(basis_set)]
    H = np.matmul(np.transpose([basis_set]), h) # (nx1)x(1xn) = (nxn) matrix multiplication
    return H

def eigen(matrix):
    '''Calculates and returns the eigenvalues and eigenvectors of the matrix. The eigenvalues correspond to the lowest energy and eigenvectors correspond to the lowest energy state basis set coefficients.
    
    Parameters
    -----
    matrix: (.., N, N) array
            A matrix for which eigenvalues and eigenvectors are to be found
    
    Returns
    -----
    (.., N) array
        Eigenvalues of the given matrix
        
    (.., N, N) array
        Eigenvectors of the given matrix
    '''
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    return eigenvalues, eigenvectors

def write_output(out_file, output):
    '''Writes to the output file.
    
    Parameters
    ----
    out_file: string
        The path of the file where output needs to be written
    output: array like
        The output to be written in the file
    '''
    f = open(out_file, 'w')
    f.write('basis set coefficients are:\n')
    for i, n in enumerate(output):
        f.write('a{} = {:.4f}\n'.format(i+1, n))
    f.close()

def main(): #pragma: no cover
    parser = create_parser()
    args = parser.parse_args()
    
    print('Started!')
    V0 = args.potential
    c = args.constant
    basis_size = args.basis_size
    choice = args.basis_choice
    (lower_lim, upper_lim) = args.domain
    output_file = args.output_file
    
    x = np.linspace(lower_lim, upper_lim, 100) 
    wave_func = wave_function(args.wave_function, x)
    
    basis = basis_set(ch = choice, x = x, y = wave_func, basis_size = basis_size)
    H = hamiltonian(ch = choice, x = x, y = wave_func, c = c, V0 = V0, basis_set = basis)
    coefficients, Energy = eigen(H)

    write_output(output_file, coefficients)
    print('\nDone! Please see the output file for results.')