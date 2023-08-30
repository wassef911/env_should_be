from __future__ import annotations

import setuptools

with open('README.md', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='env_should_be',
    author='Wassef911',
    author_email='wassef911.org@gmail.com',
    description='Example PyPI (Python Package Index) Package',
    keywords='example, pypi, package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/wassef911/env_should_be',
    project_urls={
        'Documentation': 'https://github.com/wassef911/env_should_be/blob/master/README.md',
        'Bug Reports': 'https://github.com/wassef911/env_should_be/issues',
        'Source Code': 'https://github.com/wassef911/env_should_be',
        'Funding': 'Tounes Lina, honorable mention since they inspired the idea.',
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.10 :: Only',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11.4',
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    entry_points={
        'console_scripts': [
            'run=env_should_be:main',
        ],
    },
)
