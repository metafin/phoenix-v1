from commands2 import Command

class RotateToAprilTag(Command):
    def __init__(self, drive, limelight_handler):
        print("rotate_to_april_tag init")
        super().__init__()
        self.drive = drive
        self.limelight_handler = limelight_handler
        self.target_acquired = False

        # Declare subsystem dependencies
        self.addRequirements(self.drive)

    def initialize(self):
        """Called when the command is initially scheduled."""
        self.target_acquired = False
        print("rotate_to_april_tag initialized")

    def execute(self):
        """Called repeatedly when the command is scheduled."""
        print("rotate_to_april_tag execute")
        result = self.limelight_handler.read_results()
        if result and result.validity:
            print("Target: Acquired")
            tx = result.targeting_offset_x  # Replace with your Limelight's offset API
            if abs(tx) > 1.0:  # Adjust the threshold as needed
                self.drive.with_rotational_rate(-0.1 * tx)  # Proportional control
            else:
                self.target_acquired = True
        else:
            print('Target: None Found')

    def isFinished(self):
        """Keep running until interrupted (button release)."""
        return False  # Never finish automatically, only stop on interruption

    def end(self, interrupted):
        """Called once the command ends or is interrupted."""
        print(f"rotate_to_april_tag ended, interrupted={interrupted}")
        self.drive.with_rotational_rate(0)  # Stop the drivetrain
