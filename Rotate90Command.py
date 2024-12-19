from commands2 import Command
from wpimath.geometry import Rotation2d


class Rotate90Command(Command):
    def __init__(self, drive_request, max_angular_rate):
        super().__init__()
        self.drive_request = drive_request
        self.max_angular_rate = max_angular_rate
        self.target_angle = None
        self.tolerance = Rotation2d.fromDegrees(2)  # 2 degree tolerance

    def initialize(self):
        # Get current rotation and add 90 degrees
        current_rotation = self.drive_request.get_drivetrain().get_state().pose.rotation()
        self.target_angle = current_rotation + Rotation2d.fromDegrees(90)

    def execute(self):
        current_rotation = self.drive_request.get_drivetrain().get_state().pose.rotation()
        angle_error = self.target_angle - current_rotation

        # Apply rotation based on error
        self.drive_request \
            .with_velocity_x(0) \
            .with_velocity_y(0) \
            .with_rotational_rate(
            min(self.max_angular_rate, abs(angle_error.radians())) *
            (-1 if angle_error.radians() < 0 else 1)
            )

        self.drive_request.get_drivetrain().apply_request(self.drive_request)

    def isFinished(self):
        current_rotation = self.drive_request.get_drivetrain().get_state().pose.rotation()
        return abs((self.target_angle - current_rotation).radians()) < self.tolerance.radians()

    def end(self, interrupted):
        # Stop rotation
        self.drive_request \
            .with_velocity_x(0) \
            .with_velocity_y(0) \
            .with_rotational_rate(0)
        self.drive_request.get_drivetrain().apply_request(self.drive_request)