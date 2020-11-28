from setuptools import setup

setup(
    name='RunAnova',
    version="1.0a",
    long_description="Run One Way and Two Anova and few tests",
    package_data={
    },
    packages=
    [
        "RunAnova"
    ],
    include_package_data=True,
    install_requires=[
        "numpy==1.19.1",
        "pandas==1.1.3",
        "scipy==1.5.2",
        "seaborn==0.11.0",
        "matplotlib==3.3.2",
        "statsmodels==0.12.1"
    ],
    url='https://github.com/bledem',
    license='MIT',
    author='Betty LD',
    python_requires='>=3.7',
    author_email='',
    description='Run ANOVA',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
    ]
)

