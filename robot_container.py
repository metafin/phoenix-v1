#!/usr/bin/env python3

import math
from phoenix6 import utils
from phoenix6.mechanisms.swerve import SwerveRequest, DriveRequestType
from wpimath.geometry import Pose2d, Rotation2d, Translation2d
from commands2 import Command, Commands
from wpilib import XboxController
from .generated.tuner_constants import TunerConstants
from .subsystems.command_swerve_drivetrain import CommandSwerveDrivetrain
from .telemetry import Telemetry


class RobotContainer:
    def __init__(self):
        """Initialize the RobotContainer"""
        self.max_speed = TunerConstants.kSpeedAt12VoltsMps  # Desired top speed
        self.max_angular_rate = 1.5 * math.pi  # 3/4 of a rotation per second max angular velocity

        # Setting up bindings for necessary control of the swerve drive platform
        self.joystick = XboxController(0)  # My joystick
        self.drivetrain = TunerConstants.DriveTrain  # My drivetrain

        # Create drive requests
        self.drive = (SwerveRequest.FieldCentric()
                      .withDeadband(self.max_speed * 0.1)
                      .withRotationalDeadband(self.max_angular_rate * 0.1)  # Add a 10% deadband
                      .withDriveRequestType(DriveRequestType.OpenLoopVoltage))  # Field-centric driving in open loop

        self.brake = SwerveRequest.SwerveDriveBrake()
        self.point = SwerveRequest.PointWheelsAt()

        self.logger = Telemetry(self.max_speed)

        self.configure_bindings()

    def configure_bindings(self) -> None:
        """Configure joystick button bindings"""

        # Drivetrain will execute this command periodically
        self.drivetrain.setDefaultCommand(
            self.drivetrain.applyRequest(
                lambda: self.drive
                .withVelocityX(-self.joystick.getLeftY() * self.max_speed)  # Drive forward with negative Y
                .withVelocityY(-self.joystick.getLeftX() * self.max_speed)  # Drive left with negative X
                .withRotationalRate(-self.joystick.getRightX() * self.max_angular_rate)
                # Drive counterclockwise with negative X
            )
        )

        # A button enables brake mode
        Commands.button(lambda: self.joystick.getAButton()).whileTrue(
            self.drivetrain.applyRequest(lambda: self.brake)
        )

        # B button points wheels based on left stick
        Commands.button(lambda: self.joystick.getBButton()).whileTrue(
            self.drivetrain.applyRequest(
                lambda: self.point.withModuleDirection(
                    Rotation2d(-self.joystick.getLeftY(), -self.joystick.getLeftX())
                )
            )
        )

        # Reset field-centric heading on left bumper press
        Commands.button(lambda: self.joystick.getLeftBumper()).onTrue(
            self.drivetrain.runOnce(lambda: self.drivetrain.seedFieldRelative())
        )

        # Initialize field relative position in simulation
        if utils.is_simulation():
            self.drivetrain.seedFieldRelative(
                Pose2d(Translation2d(), Rotation2d.fromDegrees(90))
            )

        # Register telemetry
        self.drivetrain.registerTelemetry(self.logger.telemeterize)

    def get_autonomous_command(self) -> Command:
        """Returns the autonomous command to run. Override this to add autonomous commands."""
        return Commands.print("No autonomous command configured")