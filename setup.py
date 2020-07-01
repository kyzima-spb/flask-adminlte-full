import os

from setuptools import setup, find_packages


def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()


readme = read_file('README.rst')


setup(
    name='flask-adminlte-full',
    use_scm_version={
        'relative_to': __file__,
        'local_scheme': lambda version: '',
    },
    description='An extension for Flask that integrates the AdminLTE template with most of the features.',
    long_description=readme,
    keywords='adminlte adminlte3 flask templating html',
    url='https://github.com/kyzima-spb/flask-adminlte-full',
    license='MIT',
    author='Kirill Vercetti',
    author_email='office@kyzima-spb.com',
    packages=find_packages(),
    include_package_data=True,
    setup_requires=['setuptools_scm'],
    install_requires=[
        'adminlte-base',
        'Flask>=1.0',
        'Flask-Gravatar>=0.5',
    ],
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Development Status :: 3 - Alpha',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
