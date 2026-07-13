import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    # ######################################################################
    # BASIC DESCRIPTION
    # ######################################################################
    name='photoring',
    author="Jorge I. Zuluaga",
    author_email="jorge.zuluaga@udea.edu.co",
    description="PhotoRing Utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://seap-udea.org",
    keywords='planets ring photometry',
    license='MIT',

    # ######################################################################
    # CLASSIFIER
    # ######################################################################
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    version='0.1.0',

    # ######################################################################
    # FILES
    # ######################################################################
    package_dir={"": "package"},
    packages=setuptools.find_packages(where="package"),
    
    # ######################################################################
    # ENTRY POINTS
    # ######################################################################
    entry_points={
        'console_scripts': ['install=pympact.install:main'],
    },

    # ######################################################################
    # TESTS
    # ######################################################################
    test_suite='nose.collector',
    tests_require=['nose'],

    # ######################################################################
    # DEPENDENCIES
    # ######################################################################
    install_requires=['scipy','matplotlib','pandas',
                      'jupyter','nbconvert','multiprocess'],

    # ######################################################################
    # OPTIONS
    # ######################################################################
    include_package_data=True,
    package_data={"": ["data/*"]},
)
