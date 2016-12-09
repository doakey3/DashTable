from setuptools import setup

setup(name='DashTable',
      version='1.2.0',
      author='Gustav Klopp',
      author_email='gustavk@protonmail.com',
      description='A library for converting a HTML table into an ASCII table',
      url='https://github.com/gustavklopp/DashTable',
      packages=['DashTable'],
      install_requires=['beautifulsoup4'],
      entry_points={'console_scripts': ['dashtable = DashTable.html2rst:cmdline']}
)
