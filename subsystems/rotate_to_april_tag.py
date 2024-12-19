from commands2 import Command
from phoenix6.swerve import requests


class RotateToAprilTag(Command):
    def __init__(self, drivetrain, limelight_handler):
        print("[RotateToAprilTag] Initializing command")
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
        print("[RotateToAprilTag] Initialization complete")

    def execute(self):
        """Called repeatedly when the command is scheduled."""
        print("[RotateToAprilTag] Execute called")
        result = self.limelight_handler.read_results()
        print(f"[RotateToAprilTag] Limelight result: {result}")

        if result and result.validity:
            tx = result.targeting_offset_x
            print(f"[RotateToAprilTag] Target offset X: {tx}")

            if abs(tx) > 1.0:
                rotation_rate = -0.1 * tx
                print(f"[RotateToAprilTag] Rotating with rate: {rotation_rate}")
                # Apply the rotation request properly
                self.drivetrain.apply_request(
                    lambda: self.drive
                    .with_velocity_x(0)
                    .with_velocity_y(0)
                    .with_rotational_rate(rotation_rate)
                )
            else:
                print("[RotateToAprilTag] Target acquired - within threshold")
                self.target_acquired = True
        else:
            print("[RotateToAprilTag] No valid target found")

    def isFinished(self):
        """Returns True when the command should end."""
        finished = self.target_acquired
        print(f"[RotateToAprilTag] isFinished called, returning: {finished}")
        return finished

    def end(self, interrupted):
        """Called once the command ends or is interrupted."""
        print(f"[RotateToAprilTag] Ending command. Interrupted: {interrupted}")
        # Stop rotation by applying zero request
        self.drivetrain.apply_request(
            lambda: self.drive
            .with_velocity_x(0)
            .with_velocity_y(0)
            .with_rotational_rate(0)
        )
        print("[RotateToAprilTag] Zero rotation request applied")