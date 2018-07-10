from setuptools import (
    setup, find_packages
)


with open('requirements.txt') as fh:
    requirements = fh.read() \
            .split()

setup(
    name='adoc',
    version='0.1.0',
    license='BSD',
    author='Benoit Myard',
    author_email='benoit@myard.xyz',
    url='https://github.com/saalaa/adoc',
    project_urls={
        'Issues': 'https://github.com/saalaa/adoc/issues'
    },
    description='Python code documentation generator',
    long_description='See https://github.com/saalaa/adoc',
    include_package_data=True,
    install_requires=requirements,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: OS Independent',
        'Operating System :: POSIX :: BSD',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    entry_points={
        'console_scripts': [
            'adoc = adoc.cli:main'
        ]
    }
)
