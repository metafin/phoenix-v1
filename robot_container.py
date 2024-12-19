import math
from commands2 import InstantCommand, PrintCommand, Command, CommandScheduler, SequentialCommandGroup
from commands2.button import Trigger
from wpilib import XboxController
from wpilib.event import EventLoop
from wpimath.geometry import Pose2d, Rotation2d, Translation2d
from phoenix6 import utils
from phoenix6.swerve import requests, swerve_module
from subsystems.command_swerve_drivetrain import CommandSwerveDrivetrain
from telemetry import Telemetry
from generated import tuner_constants
from commands2.button import JoystickButton
from subsystems.rotate_to_april_tag import RotateToAprilTag
from handlers.limelight_handler import LimelightHandler
from commands2 import InstantCommand, WaitCommand, SequentialCommandGroup
from wpilib import Timer

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

        # Ensure you have a default EventLoop from the CommandScheduler
        default_loop = CommandScheduler.getInstance().getDefaultButtonLoop()

        a_button = JoystickButton(self.joystick, self.joystick.Button.kA)
        b_button = JoystickButton(self.joystick, self.joystick.Button.kB)
        x_button = JoystickButton(self.joystick, self.joystick.Button.kX)
        x_button.onTrue(self.create_rotate_command(90))
        left_bumper_button = JoystickButton(self.joystick, self.joystick.Button.kLeftBumper)

        def print_action(button_name):
            print(f"Button: {button_name}")

        a_button_command = SequentialCommandGroup(
            InstantCommand(lambda: print_action("A")),  # Print that the A button was pressed
            InstantCommand(lambda: self.drivetrain.apply_request(lambda: self.brake))  # Apply the brake
        )

        b_button_command = SequentialCommandGroup(
            InstantCommand(lambda: print_action("B")),  # Print that the A button was pressed
            InstantCommand(
                lambda: self.drivetrain.apply_request(
                    lambda: self.point.with_module_direction(
                        Rotation2d(-self.joystick.getLeftY(), -self.joystick.getLeftX())
                    )
                )
            )
        )

        lb_button_command = SequentialCommandGroup(
            InstantCommand(lambda: print_action("LB")),  # Print that the A button was pressed
            InstantCommand(lambda: self.drivetrain.seed_field_centric())
        )

        # Bind the command to run continuously
        a_button.onTrue(InstantCommand(lambda: CommandScheduler.getInstance().schedule(a_button_command)))
        b_button.onTrue(InstantCommand(lambda: CommandScheduler.getInstance().schedule(b_button_command)))
        left_bumper_button.onTrue(InstantCommand(lambda: CommandScheduler.getInstance().schedule(lb_button_command)))
        x_button.whileTrue(RotateToAprilTag(self.drive, self.limelight_handler, self.max_angular_rate))

    def create_rotate_command(self, degrees):
        radians = math.radians(degrees)
        duration = abs(radians / self.max_angular_rate)

        return SequentialCommandGroup(
            InstantCommand(
                lambda: self.drivetrain.apply_request(
                    lambda: self.drive.with_velocity_x(0)
                    .with_velocity_y(0)
                    .with_rotational_rate(
                        self.max_angular_rate if degrees > 0 else -self.max_angular_rate
                    )
                )
            ),
            WaitCommand(duration),
            InstantCommand(
                lambda: self.drivetrain.apply_request(
                    lambda: self.drive.with_velocity_x(0)
                    .with_velocity_y(0)
                    .with_rotational_rate(0)
                )
            )
        )
    def get_autonomous_command(self) -> Command:
        """Return the autonomous command."""
        return PrintCommand("No autonomous command configured")