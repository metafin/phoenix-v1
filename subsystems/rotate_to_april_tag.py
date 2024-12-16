from commands2 import Command
from generated import tuner_constants

class RotateToAprilTag(Command):
    def __init__(self, drive, limelight_handler, max_angular_rate):
        print("rotate_to_april_tag init")
        super().__init__()
        self.drivetrain = tuner_constants.DriveTrain
        self.drive = drive
        self.limelight_handler = limelight_handler
        self.max_angular_rate = max_angular_rate
        self.target_acquired = False

        # Declare subsystem dependencies
        self.addRequirements(self.drive)

    def initialize(self):
        """Called when the command is initially scheduled."""
        self.target_acquired = False
        print("rotate_to_april_tag initialized")

    def execute(self):
        """Called repeatedly when the command is scheduled."""
        print("")
        print("")
        print("rotate_to_april_tag execute")
        result = self.limelight_handler.read_results()
        if result and result.validity:
            print("")
            print("")
            print("----- Target: Acquired")
            tx = result.fiducialResults[0].target_x_degrees  # Replace with your Limelight's offset API
            print("")
            print("")
            print("----- Target: tx:",tx)
            if abs(tx) > 1.0:  # Adjust the threshold as needed
                scaled_rotation = tx / 45
                print("")
                print("")
                print("----- Scaled Rotation:", scaled_rotation)
                print("----- Rotation:", -scaled_rotation * self.max_angular_rate)
                self.drivetrain.apply_request(lambda: self.drive
                                              .with_rotational_rate(-scaled_rotation * self.max_angular_rate)
                                              )
            else:
                self.target_acquired = True
        else:
            print("")
            print("")
            print('----- Target: None Found')

    def isFinished(self):
        """Keep running until interrupted (button release)."""
        return False  # Never finish automatically, only stop on interruption

    def end(self, interrupted):
        """Called once the command ends or is interrupted."""
        print(f"rotate_to_april_tag ended, interrupted={interrupted}")
        self.drive.with_rotational_rate(0)  # Stop the drivetrain
