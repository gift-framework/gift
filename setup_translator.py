"""
Setup script for GIFT Translator
"""

from setuptools import setup, find_packages
import os

# Read requirements for translator
def read_requirements():
    requirements = [
        "flask>=2.0.0",
        "numpy>=1.21.0",
    ]
    return requirements

setup(
    name="gift-translator",
    version="1.0.0",
    author="GIFT Research Group",
    author_email="contact@gift-framework.org",
    description="Bidirectional translator between Standard Model and GIFT formalism",
    long_description="GIFT Translator provides bidirectional translation capabilities between Standard Model and Geometric Information Field Theory (GIFT) formalism, including web interface and command-line tools.",
    url="https://github.com/gift-framework/gift",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "web": [
            "flask>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "gift-translate=gift_translator.cli:main",
            "gift-web=gift_translator.web_interface:app",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
