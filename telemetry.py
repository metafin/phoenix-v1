#!/usr/bin/env python3

from phoenix6.utils import Utils
from phoenix6.mechanisms.swerve import SwerveDriveState
from wpimath.geometry import Pose2d, Translation2d
from networktables import NetworkTableInstance
from wpilib import SmartDashboard, Mechanism2d, MechanismLigament2d, Color, Color8Bit


class Telemetry:
    def __init__(self, max_speed: float):
        """
        Construct a telemetry object, with the specified max speed of the robot

        Args:
            max_speed: Maximum speed in meters per second
        """
        self.max_speed = max_speed

        # What to publish over networktables for telemetry
        self.inst = NetworkTableInstance.getDefault()

        # Robot pose for field positioning
        self.table = self.inst.getTable("Pose")
        self.field_pub = self.table.getDoubleArrayTopic("robotPose").publish()
        self.field_type_pub = self.table.getStringTopic(".type").publish()

        # Robot speeds for general checking
        self.drive_stats = self.inst.getTable("Drive")
        self.velocity_x = self.drive_stats.getDoubleTopic("Velocity X").publish()
        self.velocity_y = self.drive_stats.getDoubleTopic("Velocity Y").publish()
        self.speed = self.drive_stats.getDoubleTopic("Speed").publish()
        self.odom_period = self.drive_stats.getDoubleTopic("Odometry Period").publish()

        # Keep a reference of the last pose to calculate the speeds
        self.last_pose = Pose2d()
        self.last_time = Utils.getCurrentTimeSeconds()

        # Mechanisms to represent the swerve module states
        self.module_mechanisms = [
            Mechanism2d(1, 1),
            Mechanism2d(1, 1),
            Mechanism2d(1, 1),
            Mechanism2d(1, 1)
        ]

        # A direction and length changing ligament for speed representation
        self.module_speeds = []
        # A direction changing and length constant ligament for module direction
        self.module_directions = []

        # Initialize the mechanism ligaments
        for i, mech in enumerate(self.module_mechanisms):
            root_speed = mech.getRoot(f"RootSpeed", 0.5, 0.5)
            root_direction = mech.getRoot(f"RootDirection", 0.5, 0.5)

            self.module_speeds.append(
                root_speed.append(MechanismLigament2d("Speed", 0.5, 0))
            )

            self.module_directions.append(
                root_direction.append(
                    MechanismLigament2d("Direction", 0.1, 0, 0, Color8Bit(Color.kWhite))
                )
            )

    def telemeterize(self, state: SwerveDriveState) -> None:
        """
        Accept the swerve drive state and telemeterize it to smartdashboard

        Args:
            state: Current state of the swerve drive
        """
        # Telemeterize the pose
        pose = state.Pose
        self.field_type_pub.set("Field2d")
        self.field_pub.set([
            pose.X(),
            pose.Y(),
            pose.rotation().degrees()
        ])

        # Telemeterize the robot's general speeds
        current_time = Utils.getCurrentTimeSeconds()
        diff_time = current_time - self.last_time
        self.last_time = current_time

        distance_diff = pose.minus(self.last_pose).translation()
        self.last_pose = pose

        velocities = distance_diff.div(diff_time)

        self.speed.set(velocities.norm())
        self.velocity_x.set(velocities.X())
        self.velocity_y.set(velocities.Y())
        self.odom_period.set(state.OdometryPeriod)

        # Telemeterize the module's states
        for i in range(4):
            self.module_speeds[i].setAngle(state.ModuleStates[i].angle)
            self.module_directions[i].setAngle(state.ModuleStates[i].angle)
            self.module_speeds[i].setLength(
                state.ModuleStates[i].speedMetersPerSecond / (2 * self.max_speed)
            )

            SmartDashboard.putData(f"Module {i}", self.module_mechanisms[i])