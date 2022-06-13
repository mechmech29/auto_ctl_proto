from setuptools import setup

package_name = 'auto_ctl'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yuhex',
    maintainer_email='yuhex@todo.todo',
    description='TODO: Package description',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'csv_talker = auto_ctl.csv_pub:main',
            'swing_talker = auto_ctl.swing_pub:main',
            'rolling_talker = auto_ctl.const_rolling:main'
        ],
    },
)

