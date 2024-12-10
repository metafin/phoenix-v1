from commands2 import Command

class RotateToAprilTag(Command):
    def __init__(self, drivetrain, limelight_handler):
        print("rotate_to_april_tag init")
        super().__init__()
        self.drivetrain = drivetrain
        self.limelight_handler = limelight_handler
        self.target_acquired = False

        # Declare subsystem dependencies
        self.addRequirements(self.drivetrain)

    def initialize(self):
        """Called when the command is initially scheduled."""
        self.target_acquired = False

    def execute(self):
        """Called repeatedly when the command is scheduled."""
        print("rotate_to_april_tag executing")
        result = self.limelight_handler.read_results()
        if result and result.validity:
            # Assume `tx` is the horizontal offset (to be adjusted based on your library)
            tx = result.targeting_offset_x  # Update this field based on your Limelight API
            if abs(tx) > 1.0:  # Adjust the threshold as needed
                # Rotate proportionally to the offset
                self.drivetrain.with_rotational_rate(-0.1 * tx)  # Proportional control
            else:
                # If tx is small enough, consider it centered
                self.target_acquired = True

    def isFinished(self):
        """Returns True to indicate the command is finished."""
        return self.target_acquired

    def end(self, interrupted):
        """Called once the command ends or is interrupted."""
        # Stop the robot's rotation
        self.drivetrain.with_rotational_rate(0)
