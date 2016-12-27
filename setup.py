from setuptools import setup

setup(
    name='dashtable',
    packages=['dashtable'],
    version='1.2.6',
    description='A library for converting a HTML tables into ASCII tables',
    long_description=open('README.rst').read(),
    author='doakey3',
    author_email='dashtable.dmodo@spamgourmet.com',
    url='https://github.com/doakey3/DashTable',
    download_url='https://github.com/doakey3/DashTable/tarball/1.2.6',
    license='MIT',
    install_requires=['beautifulsoup4'],
    entry_points={'console_scripts': ['dashtable = DashTable.html2rst:cmdline']}
)
