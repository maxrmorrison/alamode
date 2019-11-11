from setuptools import setup, find_packages

setup(
    name='alamode',
    version='1.0.0',
    url='https://github.com/maxrmorrison/alamode',
    author='Max Morrison',
    author_email='maxrmorrison@gmail.com',
    description='Synthetic multimodal audio database generator',
    packages=find_packages(),    
    install_requires=['librosa', 'matplotlib', 'numpy', 'scipy'],
)