import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="psana_wrapper",
    version="v0.0.0",
    author="Cong Wang",
    author_email="wangimagine@gmail.com",
    description="A psana wrapper.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/carbonscott/psana-wrapper",
    keywords = ['SLAC', 'LCLS', 'PSANA'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
)
