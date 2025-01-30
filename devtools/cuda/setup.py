from setuptools import setup
import os

OPENMM_TORCH_VERSION=os.getenv('OPENMM_TORCH_VERSION')
CUDA_VERSION=os.getenv('CUDA_VERSION')

setup(
    name=f'OpenMM-Torch-CUDA-{CUDA_VERSION}',
    version=OPENMM_TORCH_VERSION,
    description='CUDA platform for OpenMM-Torch',
    author='Peter Eastman',
    url='https://openmm.org',
    packages=[],
    install_requires=[f'OpenMM-CUDA-{CUDA_VERSION}']
)
