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
from Rotate90Command import Rotate90Command

class RobotContainer:
    def __init__(self):
        self.max_speed = tuner_constants.k_speed_at_12_volts_mps
        self.max_angular_rate = 1.5 * math.pi

        self.joystick = XboxController(0)
        self.drivetrain = CommandSwerveDrivetrain()  # Initialize drivetrain directly

        self.drive = requests.FieldCentric() \
            .with_deadband(self.max_speed * 0.1) \
            .with_rotational_deadband(self.max_angular_rate * 0.1) \
            .with_drive_request_type(swerve_module.SwerveModule.DriveRequestType.OPEN_LOOP_VOLTAGE)

        self.brake = requests.SwerveDriveBrake()
        self.point = requests.PointWheelsAt()

        self.logger = Telemetry(self.max_speed)

        if utils.is_simulation():
            self.drivetrain.seed_field_centric()

        self.drivetrain.register_telemetry(self.logger.telemeterize)
        self.configure_bindings()

    def configure_bindings(self):
        self.drivetrain.setDefaultCommand(
            Command(lambda: self.drivetrain.apply_request(self.get_drive_request()))
        )

        a_button = JoystickButton(self.joystick, XboxController.Button.kA.value)
        b_button = JoystickButton(self.joystick, XboxController.Button.kB.value)
        x_button = JoystickButton(self.joystick, XboxController.Button.kX.value)
        left_bumper = JoystickButton(self.joystick, XboxController.Button.kLeftBumper.value)

        # Simple commands
        a_button.onTrue(InstantCommand(self.apply_brake))
        b_button.onTrue(InstantCommand(self.point_wheels))
        x_button.onTrue(Rotate90Command(self.drive, self.max_angular_rate))
        left_bumper.onTrue(InstantCommand(self.seed_field_centric_command))

    def get_drive_request(self):
        return self.drive \
            .with_velocity_x(-self.joystick.getLeftY() * self.max_speed) \
            .with_velocity_y(-self.joystick.getLeftX() * self.max_speed) \
            .with_rotational_rate(-self.joystick.getRightX() * self.max_angular_rate)

    def apply_brake(self):
        self.drivetrain.apply_request(self.brake)

    def point_wheels(self):
        rotation = Rotation2d(-self.joystick.getLeftY(), -self.joystick.getLeftX())
        self.drivetrain.apply_request(self.point.with_module_direction(rotation))

    def seed_field_centric_command(self):
        self.drivetrain.seed_field_centric()

    def get_autonomous_command(self) -> Command:
        return PrintCommand("No autonomous command configured")