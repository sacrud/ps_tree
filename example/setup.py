from setuptools import setup

version = '1.0'

setup(
    name='ps_tree_example',
    version=version,
    py_modules=['ps_tree_example'],
    entry_points="""
[paste.app_factory]
main = ps_tree_example:main
    """,
)
