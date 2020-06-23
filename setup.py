from setuptools import setup, find_packages


setup(
    name='flask-adminlte-full',
    use_scm_version={
        'relative_to': __file__,
        'local_scheme': lambda version: '',
    },
    description='This Flask extension is port the AdminLTE Template for easy integration into Flask Framework.',
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
