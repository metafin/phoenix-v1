import math
from commands2 import InstantCommand, PrintCommand, Command, CommandScheduler
from commands2.button import Trigger
from wpilib import XboxController
import wpilib
from wpilib.event import EventLoop
from wpimath.geometry import Pose2d, Rotation2d, Translation2d
from phoenix6 import utils
from phoenix6.swerve import requests, swerve_module
from subsystems.command_swerve_drivetrain import CommandSwerveDrivetrain
from telemetry import Telemetry
from generated import tuner_constants
from commands2 import InstantCommand, CommandScheduler
from subsystems.rotate_to_april_tag import RotateToAprilTag
from handlers.limelight_handler import LimelightHandler

class RobotContainer:
    def __init__(self):
        """Initialize the RobotContainer and configure bindings."""
        self.max_speed = tuner_constants.k_speed_at_12_volts_mps * 0.5  # Top speed
        self.max_angular_rate = 1.5 * math.pi  # Max angular velocity (3/4 rotation per second)

        # Joystick and drivetrain initialization
        self.joystick = XboxController(0)
        self.drivetrain = tuner_constants.DriveTrain

        self.limelight_handler = LimelightHandler(debug=True)

        # Swerve requests
        self.drive = requests.FieldCentric() \
            .with_deadband(self.max_speed * 0.1) \
            .with_rotational_deadband(self.max_angular_rate * 0.1) \
            .with_drive_request_type(swerve_module.SwerveModule.DriveRequestType.OPEN_LOOP_VOLTAGE)

        self.brake = requests.SwerveDriveBrake()
        self.point = requests.PointWheelsAt()

        # Telemetry
        self.logger = Telemetry(self.max_speed)

        self.event_loop = EventLoop()

        # Configure button bindings
        self.configure_bindings()

        # If in simulation, seed_field_centric position
        if utils.is_simulation():
            self.drivetrain.seed_field_centric()

        # Register telemetry
        self.drivetrain.register_telemetry(self.logger.telemeterize)

    def configure_bindings(self):
        """Configure button-to-command mappings."""
        # Default drivetrain command
        self.drivetrain.setDefaultCommand(
            self.drivetrain.apply_request(lambda: self.drive
                                          .with_velocity_x(-self.joystick.getLeftY() * self.max_speed)
                                          .with_velocity_y(-self.joystick.getLeftX() * self.max_speed)
                                          .with_rotational_rate(-self.joystick.getRightX() * self.max_angular_rate)
                                          )
        )

        # A Button - Brake
        self.joystick.A(self.event_loop).ifHigh(
            lambda: CommandScheduler.getInstance().schedule(
                InstantCommand(lambda: [
                    wpilib.DataLogManager.log("A Button Pressed - Activating Brake"),
                    self.drivetrain.apply_request(lambda: self.brake)
                ]())
            )
        )

        # B Button - Point Wheels
        self.joystick.B(self.event_loop).ifHigh(
            lambda: CommandScheduler.getInstance().schedule(
                InstantCommand(
                    lambda: [
                        wpilib.DataLogManager.log("B Button Pressed - Pointing Wheels"),
                        self.drivetrain.apply_request(
                            lambda: self.point.with_module_direction(
                                Rotation2d(-self.joystick.getLeftY(), -self.joystick.getLeftX())
                            )
                        )
                    ]()
                )
            )
        )

        # X Button - Rotate to AprilTag
        self.joystick.X(self.event_loop).ifHigh(
            lambda: [
                wpilib.DataLogManager.log("X Button Pressed - Rotating to AprilTag"),
                CommandScheduler.getInstance().schedule(
                    RotateToAprilTag(self.drivetrain, self.limelight_handler)
                )
            ]()
        )

        # Y Button
        self.joystick.Y(self.event_loop).ifHigh(
            lambda: wpilib.DataLogManager.log("Y Button Pressed")
        )

        # Bumpers
        self.joystick.leftBumper(self.event_loop).ifHigh(
            lambda: [
                wpilib.DataLogManager.log("Left Bumper Pressed - Resetting Field-Centric Heading"),
                CommandScheduler.getInstance().schedule(
                    InstantCommand(lambda: self.drivetrain.seed_field_centric())
                )
            ]()
        )

        self.joystick.rightBumper(self.event_loop).ifHigh(
            lambda: wpilib.DataLogManager.log("Right Bumper Pressed")
        )

        # Triggers
        self.joystick.leftTrigger(self.event_loop).ifHigh(
            lambda: wpilib.DataLogManager.log("Left Trigger Pressed")
        )

        self.joystick.rightTrigger(self.event_loop).ifHigh(
            lambda: wpilib.DataLogManager.log("Right Trigger Pressed")
        )

        # Start and Back buttons
        self.joystick.start(self.event_loop).ifHigh(
            lambda: wpilib.DataLogManager.log("Start Button Pressed")
        )

        self.joystick.back(self.event_loop).ifHigh(
            lambda: wpilib.DataLogManager.log("Back Button Pressed")
        )

    def get_autonomous_command(self) -> Command:
        """Return the autonomous command."""
        return PrintCommand("No autonomous command configured")