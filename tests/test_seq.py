import io
import os
import SEq
import numpy as np
import argparse
import unittest

class Test_Schrodinger(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
        
    def test_inputs(self):
        # Tests if the parser reads correctly and if no inputs are given, uses default values
        self.parser = SEq.create_parser()
        parsed = self.parser.parse_args(['-V0', '2', '-c', '1.1', '-s', '5', '-ch', 'Fourier', '-y', 'x**2 + 2'])
        self.assertEqual([parsed.potential, parsed.constant, parsed.basis_size, parsed.basis_choice, parsed.domain, parsed.wave_function], [2, 1.1, 5, 'Fourier', (-1, 1), 'x**2 + 2'])
        permitted_basis_types = ['legendre', 'Legendre', 'Fourier', 'fourier']
        self.assertIn(parsed.basis_choice, permitted_basis_types, 'Please select Legendre or Fourier for basis type')

    def test_wave_function(self):
        y = SEq.wave_function('x**2 + x + 1', np.linspace(-1,1,100))
        a = y[0]
        b = y[-1]
        self.assertEqual([a, b], [1, 3])
    
    def test_basis_set_legendre(self):
        x = np.linspace(1,5,5)
        y = eval('x')   #only the coefficient of x should be 1 for this wave function
        basis = SEq.basis_set(ch = 'legendre', x = x, y = y, basis_size = 5)
        assert(len(basis) == 5)
        assert(np.isclose(basis, [ 0, 1, 0, 0, 0])).all()
    
    def test_basis_set_fourier(self):
        x = np.linspace(1,5,5)
        y = eval('x')   #only the coefficient of x should be 1 for this wave function
        basis = SEq.basis_set(ch = 'fourier', x = x, y = y, basis_size = 5)
        assert(len(basis) == 5)
        self.assertEqual(basis[0].real, y.sum()/len(y)) # The first basis element must be mean of all y's

    def test_hamiltonian_legendre(self):
        basis_size = 5
        ch = 'legendre'
        x = np.linspace(0,5,basis_size)
        y = eval('x')
        basis = SEq.basis_set(ch, x = x, y = y, basis_size = basis_size)
        H = SEq.hamiltonian(ch, x, y, 0.1, 2, basis)
        assert(H.shape == (basis_size, basis_size))

    def test_hamiltonian_fourier(self):
        basis_size = 5
        x = np.linspace(0, 5, basis_size)
        y = eval('x')
        basis = SEq.basis_set(ch = 'fourier', x = x, y = y, basis_size = basis_size)
        print(basis)
        h = np.gradient(np.gradient(basis))
        print(h)
        H = SEq.hamiltonian('Fourier', x, y, 0.1, 2, basis)
        assert(H.shape == (basis_size,basis_size))
        # TODO: check correctness of the Hamiltonian

    def test_eigen(self):
        matrix = [[1,0,0], [0,1,0], [0,0,1]]
        eigenvalues, eigenvectors = SEq.eigen(matrix)
        print(eigenvalues, eigenvectors)
        self.assertEqual(eigenvalues.all(), np.array([1,1,1]).all())
        self.assertEqual(eigenvectors.all(), np.array([[1,0,0], [0,1,0], [0,0,1]]).all())


    def test_write_output(self):
        '''Tests if the output file is written correctly'''
        test_string = [1, 2, 3, 4]
        test_string2 = '''basis set coefficients are:\na1 = 1.0000\na2 = 2.0000\na3 = 3.0000\na4 = 4.0000\n'''
        test_file = io.StringIO(test_string2)
        test_data = list(test_file.readlines())

        out_file = './test_output.txt'
        SEq.write_output(out_file, test_string)
        f1 = open(out_file, 'r')
        test_data1 = list(f1.readlines())
        f1.close()

        self.assertEqual(test_data, test_data1)