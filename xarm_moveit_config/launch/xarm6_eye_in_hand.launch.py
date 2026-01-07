from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Launch arguments
    robot_ip = LaunchConfiguration('robot_ip')
    show_rviz = LaunchConfiguration('show_rviz')
    add_ft_sensor = LaunchConfiguration('add_ft_sensor')
    run_octomap = LaunchConfiguration('run_octomap')
    

    declared_arguments = [
        DeclareLaunchArgument('robot_ip', default_value='192.168.1.201', description='IP address of the robot'),
        DeclareLaunchArgument('show_rviz', default_value='false', description='Show RViz'),
        DeclareLaunchArgument('add_ft_sensor', default_value='true', description='Add FT sensor'),
        DeclareLaunchArgument('run_octomap', default_value='false', description='Run Octomap'),
    ]   

    # Get xarm_moveit_config package share directory
    moveit_config_dir = get_package_share_directory('xarm_moveit_config')

    # Include the real arm launch file from the package
    real_arm_launch_file = PathJoinSubstitution([moveit_config_dir, 'launch', 'xarm6_moveit_realmove.launch.py'])
    real_arm_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(real_arm_launch_file),
        launch_arguments={
            'robot_ip': robot_ip,
            'show_rviz': show_rviz,
            'add_ft_sensor': add_ft_sensor,
            'run_octomap': run_octomap
        }.items()
    )

    # Static transform nodes
    camera_tf_node = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='camera_tf',
        arguments=['0.0', '0.0', '0.0', '0.7071', '0.0', '0.7071', '0.0', 'camera_link_base', 'camera_link']
    )

    gripper_camera_tf_node = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='gripper_camera_tf',
        arguments=['0.07', '-0.02', '0.012', '0.0', '0.0', '0.0', '1.0', 'link_eef', 'camera_link_base']
    )

    return LaunchDescription(declared_arguments + [
        real_arm_launch,
        camera_tf_node,
        gripper_camera_tf_node
    ])
