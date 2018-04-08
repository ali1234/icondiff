from setuptools import setup

setup(
    name='icondiff',
    keywords='png diff svg icon theme',
    version='0.1',
    author='Alistair Buxton',
    author_email='a.j.buxton@gmail.com',
    url='http://github.com/ali1234/icondiff',
    license='GPLv3+',
    platforms=['linux'],
    packages=['icondiff'],
    entry_points={
        'console_scripts': [
            'icondiff = icondiff.__main__:main',
            #'svgtopng = icondiff.svgtong:main',
        ]
    },
    package_data={'icondiff': ['css/bootstrap.min.css']},
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
    ],
)