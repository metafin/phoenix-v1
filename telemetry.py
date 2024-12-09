from phoenix6 import utils
from phoenix6.swerve import SwerveDrivetrain
from networktables import NetworkTablesInstance
from wpimath.geometry import Pose2d, Translation2d, Rotation2d
from wpilib import SmartDashboard
import time

class Telemetry:
    def __init__(self, max_speed):
        """
        Initialize a telemetry object with the specified max speed of the robot.

        :param max_speed: Maximum speed in meters per second
        """
        self.max_speed = max_speed

        # NetworkTables setup
        self.inst = NetworkTablesInstance.getDefault()

        # Robot pose for field positioning
        self.table = self.inst.getTable("Pose")
        self.field_pub = self.table.getEntry("robotPose")
        self.field_type_pub = self.table.getEntry(".type")

        # Robot speeds for general checking
        self.drive_stats = self.inst.getTable("Drive")
        self.velocity_x = self.drive_stats.getEntry("Velocity X")
        self.velocity_y = self.drive_stats.getEntry("Velocity Y")
        self.speed = self.drive_stats.getEntry("Speed")
        self.odom_period = self.drive_stats.getEntry("Odometry Period")

        # Keep a reference of the last pose to calculate the speeds
        self.last_pose = Pose2d()
        self.last_time = utils.get_system_time_seconds()  # Use Phoenix6 Utils for time

    def telemeterize(self, state: SwerveDrivetrain.SwerveDriveState):
        """
        Accept the swerve drive state and telemeterize it to the dashboard.

        :param state: SwerveDriveState containing pose, module states, and odometry period
        """
        # Telemeterize the pose
        pose = state.pose
        self.field_type_pub.setString("Field2d")
        self.field_pub.setDoubleArray([pose.X(), pose.Y(), pose.rotation().degrees()])

        # Telemeterize the robot's general speeds
        current_time = utils.get_current_time_seconds()
        diff_time = current_time - self.last_time
        self.last_time = current_time

        distance_diff = pose.translation() - self.last_pose.translation()
        velocities = distance_diff / diff_time
        self.last_pose = pose

        self.speed.setDouble(velocities.norm())
        self.velocity_x.setDouble(velocities.X())
        self.velocity_y.setDouble(velocities.Y())
        self.odom_period.setDouble(state.odometry_period)

        # Telemeterize the module's states
        for i, module_state in enumerate(state.module_states):
            angle = module_state.angle.degrees()
            speed_ratio = module_state.speed / (2 * self.max_speed)

            # Simulate visualization using SmartDashboard
            SmartDashboard.putNumber(f"Module {i} Angle", angle)
            SmartDashboard.putNumber(f"Module {i} Speed Ratio", speed_ratio)
