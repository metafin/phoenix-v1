from commands2 import Command
from generated import tuner_constants
from phoenix6.swerve import requests
class RotateToAprilTag(Command):
    def __init__(self, drive, limelight_handler, max_angular_rate):
        print("rotate_to_april_tag init")
        super().__init__()
        self.drive = drive
        self.limelight_handler = limelight_handler
        self.max_angular_rate = max_angular_rate
        self.target_acquired = False

    def initialize(self):
        self.target_acquired = False
        print("rotate_to_april_tag initialized")

    def execute(self):
        print("rotate_to_april_tag execute")
        result = self.limelight_handler.read_results()
        if result and result.validity:
            print("----- Target: Acquired")
            tx = result.fiducialResults[0].target_x_degrees
            print("----- Target: tx:", tx)
            if abs(tx) > 1.0:
                scaled_rotation = tx / 45
                print("----- Scaled Rotation:", scaled_rotation)
                print("----- Rotation:", -scaled_rotation * self.max_angular_rate)
                # Fixed line - call directly on self.drive
                self.drive.with_rotational_rate(-scaled_rotation * self.max_angular_rate)
            else:
                self.target_acquired = True
        else:
            print('----- Target: None Found')

    def isFinished(self):
        return False

    def end(self, interrupted):
        print(f"rotate_to_april_tag ended, interrupted={interrupted}")
        self.drive.with_rotational_rate(0)