from setuptools import setup

setup(
    name='dashtable',
    packages=[
        'dashtable',
            'dashtable.dashutils',
            'dashtable.data2md',
            'dashtable.data2rst',
            'dashtable.data2simplerst',
            'dashtable.grid2data',
            'dashtable.html2data',
            'dashtable.simple2data'],
    version='1.4.1',
    description='A library for converting a HTML tables into ASCII tables, rowspan and colspan allowed!',
    long_description=open('README.rst').read(),
    author='doakey3 & gustavklopp',
    author_email='dashtable.dmodo@spamgourmet.com',
    url='https://github.com/doakey3/DashTable',
    download_url='https://github.com/doakey3/DashTable/tarball/1.4.0',
    license='MIT',
)
