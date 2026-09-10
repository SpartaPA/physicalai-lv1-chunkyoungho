from setuptools import find_packages, setup

package_name = 'turtle_py'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='pa28',
    maintainer_email='ckhy2k@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            # 문제 3
            'ex03_distance_publisher = turtle_py.ex03_distance_publisher:main',
            'ex03_distance_subscriber = turtle_py.ex03_distance_subscriber:main',
            # 문제 5
            'ex05_builtin_service_client = turtle_py.ex05_builtin_service_client:main',
            'ex05_toggle_servers = turtle_py.ex05_toggle_servers:main',
            'ex05_rotate_absolute_client = turtle_py.ex05_rotate_absolute_client:main',
            # 문제 6
            'ex06_polygon_action_server = turtle_py.ex06_polygon_action_server:main',
            'ex06_waypoint_publisher = turtle_py.ex06_waypoint_publisher:main',
            # 문제 7
            'ex07_qos_sensor_publisher = turtle_py.ex07_qos_sensor_publisher:main',
            'ex07_qos_subscriber = turtle_py.ex07_qos_subscriber:main',
            # 문제 9 launch 학생 모드 규격 이름 (같은 main에 대한 별칭)
            'turtle_distance_publisher = turtle_py.ex03_distance_publisher:main',
            'turtle_distance_subscriber = turtle_py.ex03_distance_subscriber:main',
            'polygon_action_server = turtle_py.ex06_polygon_action_server:main',
        ],
    },
)
