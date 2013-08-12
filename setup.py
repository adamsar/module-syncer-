try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='webdav_syncer',
    version='0.1',
    description='A CLI for synchronizing directories with a webdav server',
    author='Andrew Adams',
    author_email='a_adams@ubicast.com',
    url='http://github.com/ubicast',
    install_requires=[
        "pycli",
        "Python_WebDAV_Library",
        "fabric",
        "clint"
    ],
    setup_requires=[],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    package_data={'syncer': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors={'admin_console': [
    #        ('**.py', 'python', None),
    #        ('public/**', 'ignore', None)]},
    zip_safe=False,
    paster_plugins=['PasteScript', 'Pylons']
)
