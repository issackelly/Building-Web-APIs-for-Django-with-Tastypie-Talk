from setuptools import setup, find_packages
 
setup(
    name='django-loupe',
    version='0.1.0',
    description='A simple collaborative image/screenshot review app for Django applications',
    long_description=open('README.rst').read(),
    author='Greg Newman',
    author_email='greg@20seven.org',
    url='http://bitbucket.org/gregnewman/django-loupe/',
    install_requires=(
        'django-imagekit>=0.3.1',
        'django-extensions>=0.4.1',
    ),
    packages=find_packages(exclude=['example']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    zip_safe=False,
)
