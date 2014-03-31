from setuptools import setup

setup(
    name='half-moon-tagging',
    version='1.0.1',
    url='http://schwa.io',
    license='BSD 2-clause',
    author='Jonathan Wight',
    author_email='jwight@mac.com',
    description='Mavericks command line tool for tagging files',
	install_requires = [
		'docopt',
		],
	py_modules=['tag'],
	scripts=['tag'],
    )
