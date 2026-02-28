from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="neuraedge-ip",
    version="0.1.0",
    author="NeuraEdge Contributors",
    description="Professional neuromorphic computing platform with memristive core",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/neuraedge/ip",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "pyyaml>=5.4.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0",
    ],
    extras_require={
        "ui": ["streamlit>=1.0.0"],
        "dev": ["pytest>=6.2.0", "black>=21.0", "flake8>=3.9.0"],
    },
)
