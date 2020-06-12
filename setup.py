from setuptools import setup, find_packages


setup(
    name='flask-adminlte-full',
    use_scm_version={
        'relative_to': __file__,
    },
    url='https://github.com/kyzima-spb/flask-adminlte-full',
    description='This Flask extension is port the AdminLTE Template for easy integration into Flask Framework.',
    author='Kirill Vercetti',
    author_email='office@kyzima-spb.com',
    packages=find_packages(),
    include_package_data=True,
    setup_requires=['setuptools_scm'],
    install_requires=[
        'Flask>=1.0',
        'Flask-Gravatar>=0.5',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
