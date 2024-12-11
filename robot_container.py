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
        wpilib.SmartDashboard.putString("Status", "RobotContainer Init")

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
            self.drivetrain.apply_request(
                lambda: self.drive
                .with_velocity_x(-self.joystick.getLeftY() * self.max_speed)
                .with_velocity_y(-self.joystick.getLeftX() * self.max_speed)
                .with_rotational_rate(-self.joystick.getRightX() * self.max_angular_rate)
                )
        )

        # A Button - Brake
        def a_button_pressed():
            wpilib.SmartDashboard.putString("Button", "A Button Pressed")
            self.drivetrain.apply_request(lambda: self.brake)

        self.joystick.A(self.event_loop).ifHigh(
            lambda: CommandScheduler.getInstance().schedule(
                InstantCommand(a_button_pressed)
            )
        )

        # B Button - Point Wheels
        def b_button_pressed():
            wpilib.SmartDashboard.putString("Button", "B Button Pressed")
            self.drivetrain.apply_request(
                lambda: self.point.with_module_direction(
                    Rotation2d(-self.joystick.getLeftY(), -self.joystick.getLeftX())
                )
            )

        self.joystick.B(self.event_loop).ifHigh(
            lambda: CommandScheduler.getInstance().schedule(
                InstantCommand(b_button_pressed)
            )
        )

        # X Button - Rotate to AprilTag
        def x_button_pressed():
            wpilib.SmartDashboard.putString("Button", "X Button Pressed")
            CommandScheduler.getInstance().schedule(
                RotateToAprilTag(self.drivetrain, self.limelight_handler)
            )

        self.joystick.X(self.event_loop).ifHigh(x_button_pressed)

        # Y Button
        self.joystick.Y(self.event_loop).ifHigh(
            lambda: wpilib.SmartDashboard.putString("Button", "Y Button Pressed")
        )

        # Bumpers
        def left_bumper_pressed():
            wpilib.SmartDashboard.putString("Button", "Left Bumper Pressed")
            self.drivetrain.seed_field_centric()

        self.joystick.leftBumper(self.event_loop).ifHigh(
            lambda: CommandScheduler.getInstance().schedule(
                InstantCommand(left_bumper_pressed)
            )
        )

        self.joystick.rightBumper(self.event_loop).ifHigh(
            lambda: wpilib.SmartDashboard.putString("Button", "Right Bumper Pressed")
        )

        # Triggers
        self.joystick.leftTrigger(self.event_loop).ifHigh(
            lambda: wpilib.SmartDashboard.putString("Button", "Left Trigger Pressed")
        )

        self.joystick.rightTrigger(self.event_loop).ifHigh(
            lambda: wpilib.SmartDashboard.putString("Button", "Right Trigger Pressed")
        )

        # Start and Back buttons
        self.joystick.start(self.event_loop).ifHigh(
            lambda: wpilib.SmartDashboard.putString("Button", "Start Button Pressed")
        )

        self.joystick.back(self.event_loop).ifHigh(
            lambda: wpilib.SmartDashboard.putString("Button", "Back Button Pressed")
        )

    def get_autonomous_command(self) -> Command:
        """Return the autonomous command."""
        return PrintCommand("No autonomous command configured")