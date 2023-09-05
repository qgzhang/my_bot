import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node



def generate_launch_description():


    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name='my_bot' #<--- CHANGE ME

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
             )

    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'my_bot'],
                        output='screen')


    # Run the joystick node to publish topic /joy
    # joy = Node(package='joy',
    #            executable='joy_node',
    #            name='joy_node',
    #            output='screen')


    # Run the teleop_node node to convert topic /joy to topic /cmd_vel

    teleop = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('teleop_twist_joy'),'launch','teleop-launch.py'
                )]), launch_arguments={'joy_config': 'xbox'}.items()
    )
    
    # teleop = Node(package='teleop_twist_joy',
    #            executable='teleop_node',
    #            name='teleop_node',
    #            output='screen')
    

    # Launch them all!
    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
        # joy,
        teleop,
    ])
