import os

from setuptools import find_namespace_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="superposer",
    version="0.1",
    description="Example project to demonstrate structure superimposition",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    project_urls={
        "Source code": "https://github.com/lpravda/example.git",
        "Documentation": "https://github.com/lpravda/example.git",
    },
    author="Lukas Pravda",
    author_email="luky.pravda@gmail.com",
    license="Apache License 2.0.",
    keywords="PDB protein structure gemmi superimposition ",
    packages=find_namespace_packages(),
    zip_safe=False,
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "gemmi @ git+https://github.com/project-gemmi/gemmi.git",
        "pandas",
        "requests"
    ],
    entry_points={
        "console_scripts": ["superposer=superposer.scripts.superposer_cli:main"]
    },
    extras_require={
        "docs": [
            "sphinx",
            "sphinxcontrib-napoleon",
            "sphinx-copybutton",
            "sphinx_rtd_theme",
            "recommonmark",
            "sphinx-autodoc-typehints",
            "sphinx-markdown-tables",
        ],
        "tests": ["pytest", "pytest-cov"],
        "views": ["streamlit", "plotly"],
    },
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Development Status :: 5 - Production/Stable",
    ],
)
