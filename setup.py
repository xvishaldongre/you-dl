from iy.version import __version__
try:
    from setuptools import setup, find_namespace_packages
except ModuleNotFoundError as err:
    print(err.msg)
    exit(1)


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="you-dl",
    version=__version__,
    author="vishal dongre",
    author_email="xvishaldongre@gmail.com",
    description="A simple interactive youtube downloader written in python. Interactively select the quality and format for youtube-dl",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xvishaldongre/iydl",
    packages=find_namespace_packages(),
    install_requires=['youtube-dl', 'prompt_toolkit==1.0.14','PyInquirer',
                      'regex', 'youtube-search-python', 'pyperclip'],
    include_package_data=True,
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Multimedia ",
    ],
    license='GPLv3',
    python_requires='>=3.5',
    entry_points={
        'console_scripts': [
            'you-dl = iy.yt:main'
        ]}
)
