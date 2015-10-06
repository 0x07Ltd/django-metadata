from setuptools import setup, find_packages

setup(
    name='django-metadata',
    version='2.0.1',
    url='https://github.com/rafaelsdm/django-metadata',
    author='Rafael Sierra',
    author_email='eu@rafaelsdm.com',
    license='Free Use',
    packages=find_packages(),
    include_package_data=True,
    description=('This is a simple addon to your models, with this package you can add metadata to '
                 'any of your models'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Environment :: Plugins",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: Freeware",
        "Programming Language :: Python :: 2.7",
    ],
)
