from commands2 import Command
from phoenix6.swerve import requests


class RotateToAprilTag(Command):
    def __init__(self, drivetrain, limelight_handler):
        print("rotate_to_april_tag init")
        super().__init__()
        self.drivetrain = drivetrain
        self.limelight_handler = limelight_handler
        self.target_acquired = False

        # Create the field-centric drive request
        self.drive = requests.FieldCentric() \
            .with_deadband(0.1) \
            .with_rotational_deadband(0.1)

        # Declare subsystem dependencies
        self.addRequirements(self.drivetrain)

    def execute(self):
        """Called repeatedly when the command is scheduled."""
        print("rotate_to_april_tag executing")
        result = self.limelight_handler.read_results()
        if result and result.validity:
            tx = result.targeting_offset_x
            if abs(tx) > 1.0:
                # Apply the rotation request properly
                self.drivetrain.apply_request(
                    lambda: self.drive
                    .with_velocity_x(0)
                    .with_velocity_y(0)
                    .with_rotational_rate(-0.1 * tx)
                )
            else:
                self.target_acquired = True

    def isFinished(self):
        """Returns True when the command should end."""
        return self.target_acquired

    def end(self, interrupted):
        """Called once the command ends or is interrupted."""
        # Stop rotation by applying zero request
        self.drivetrain.apply_request(
            lambda: self.drive
            .with_velocity_x(0)
            .with_velocity_y(0)
            .with_rotational_rate(0)
        )