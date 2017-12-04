"""Setup script."""

from setuptools import setup

setup(
    name="tradingbot",
    version="0.0.0",
    authors="Komarov Nikita, Ivan Shkurak, Alexandra Minochkina",
    author_email="nikita.a.komarov@phystech.edu",
    url="https://github.com/glazastyi/trading",
    license="MIT",
    packages=[
        "trading",
    ],
    install_requires=[
        "sqlite3",
        "json",
        "hashlib",
        "hmac",
        "httplib",
        "urllib"
    ],
    setup_requires=[
        "pytest-runner",
        "pytest-pylint",
        "pytest-pycodestyle",
        "pytest-pep257",
        "pytest-cov",
    ],
    tests_require=[
        "pytest",
        "pylint",
        "pycodestyle",
        "pep257",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ]
)
