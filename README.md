Quantified Universal Broadband by Country (qubic)
===================================================

**qubic** enables the required investment to be quantified for providing
universal broadband.


Using conda
==========

The recommended installation method is to use conda, which handles packages and virtual
environments, along with the conda-forge channel which has a host of pre-built libraries and
packages.

Create a conda environment called qubic:

    conda create --name qubic python=3.7 gdal

Activate it (run this each time you switch projects):

    conda activate qubic

First, install optional packages:

    conda install geopandas

Then install qubic:

    python setup.py install

Alternatively, for development purposes, clone this repo and run:

    python setup.py develop


Quick start
===========

To prepare the data for running the model, first you need to execute:

    python scripts/pop.py

To install the packages required for data visualization try:

    conda install seaborn, descartes

And:

    pip install contextily
