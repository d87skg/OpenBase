from setuptools import setup, find_packages

setup(
    name="openbase-sdk",
    version="0.1.0",
    description="OpenBase SDK - Lightweight client for emitting OpenBase Evidence",
    author="OpenBase",
    packages=find_packages(),
    install_requires=["cryptography>=41.0.0"],
    python_requires=">=3.8",
)