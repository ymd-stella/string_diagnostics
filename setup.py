from setuptools import find_packages, setup

package_name = 'string_diagnostics'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ymd-stella',
    maintainer_email='world.applepie@gmail.com',
    description='string to diagnostic message converter',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'string_diagnostics = string_diagnostics.string_diagnostics:main',
        ],
    },
)
