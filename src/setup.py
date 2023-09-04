from __future__ import annotations

import setuptools

with open("README.md", encoding="utf-8") as fh:
    README = fh.read()

setuptools.setup(
    name="env_should_be",
    author="Wassef911",
    author_email="wassef911@gmail.com",
    description="a cli to help, build multi env applications.",
    keywords="python3, pypi, package",
    long_description_content_type="text/markdown",
    long_description=README,
    url="https://github.com/wassef911/env_should_be",
    package_dir={"": "src"},
    install_requires=[
        "pyaml",
    ],
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11.4",
    extras_require={
        "dev": ["check-manifest"],
        "test": ["coverage"],
    },
    entry_points={
        "console_scripts": [
            "env_should_be=env_should_be.cli:main",
        ],
    },
)
