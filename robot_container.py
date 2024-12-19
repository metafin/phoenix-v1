import math
from commands2 import InstantCommand, PrintCommand, Command, CommandScheduler, SequentialCommandGroup
from commands2.button import Trigger, JoystickButton
from wpilib import XboxController
from wpilib.event import EventLoop
from wpimath.geometry import Pose2d, Rotation2d, Translation2d
from phoenix6 import utils
from phoenix6.swerve import requests, swerve_module
from subsystems.command_swerve_drivetrain import CommandSwerveDrivetrain
from telemetry import Telemetry
from generated import tuner_constants
from handlers.limelight_handler import LimelightHandler
from Rotate90Command import Rotate90Command

class RobotContainer:
    def __init__(self):
        """Initialize the RobotContainer and configure bindings."""
        self.max_speed = tuner_constants.k_speed_at_12_volts_mps  # Top speed
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

        # Configure button bindings
        self.configure_bindings()

        # If in simulation, seed_field_centric position
        if utils.is_simulation():
            self.drivetrain.seed_field_centric()

        # Register telemetry
        self.drivetrain.register_telemetry(self.logger.telemeterize)

    def get_drive_request(self):
        """Create and return the drive request based on joystick inputs."""
        return self.drive \
            .with_velocity_x(-self.joystick.getLeftY() * self.max_speed) \
            .with_velocity_y(-self.joystick.getLeftX() * self.max_speed) \
            .with_rotational_rate(-self.joystick.getRightX() * self.max_angular_rate)

    def apply_brake(self):
        """Apply the brake request."""
        self.drivetrain.apply_request(self.brake)

    def point_wheels(self):
        """Point wheels based on joystick input."""
        rotation = Rotation2d(-self.joystick.getLeftY(), -self.joystick.getLeftX())
        self.drivetrain.apply_request(self.point.with_module_direction(rotation))

    def seed_field_centric_command(self):
        """Seed the field-centric position."""
        self.drivetrain.seed_field_centric()

    def configure_bindings(self):
        """Configure button-to-command mappings."""
        # Default drivetrain command
        self.drivetrain.setDefaultCommand(
            Command(lambda: self.drivetrain.apply_request(self.get_drive_request()))
        )

        a_button = JoystickButton(self.joystick, XboxController.Button.kA.value)
        b_button = JoystickButton(self.joystick, XboxController.Button.kB.value)
        x_button = JoystickButton(self.joystick, XboxController.Button.kX.value)
        left_bumper = JoystickButton(self.joystick, XboxController.Button.kLeftBumper.value)

        # Create command sequences
        a_command = SequentialCommandGroup(
            InstantCommand(lambda: print("Button: A")),
            InstantCommand(self.apply_brake)
        )

        b_command = SequentialCommandGroup(
            InstantCommand(lambda: print("Button: B")),
            InstantCommand(self.point_wheels)
        )

        lb_command = SequentialCommandGroup(
            InstantCommand(lambda: print("Button: LB")),
            InstantCommand(self.seed_field_centric_command)
        )

        # Bind commands to buttons
        a_button.onTrue(a_command)
        b_button.onTrue(b_command)
        left_bumper.onTrue(lb_command)
        x_button.onTrue(Rotate90Command(self.drive, self.max_angular_rate))

    def get_autonomous_command(self) -> Command:
        """Return the autonomous command."""
        return PrintCommand("No autonomous command configured")