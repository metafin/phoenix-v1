import wpilib
from commands2 import CommandScheduler
from robot_container import RobotContainer


class Robot(wpilib.TimedRobot):
    def robotInit(self):
        """Initialize the robot."""
        # Basic print to console
        wpilib.SmartDashboard.putString("Robot Status", "Initializing")

        # Create the robot container
        self.m_robotContainer = RobotContainer()
        self.m_autonomousCommand = None

        # Update status
        wpilib.SmartDashboard.putString("Robot Status", "Initialized")

    def robotPeriodic(self):
        """Run code that should execute regardless of the robot's mode."""
        CommandScheduler.getInstance().run()

    def disabledInit(self):
        """Run once when the robot enters Disabled mode."""
        wpilib.SmartDashboard.putString("Robot Status", "Disabled")

    def autonomousInit(self):
        """Run once when the robot enters Autonomous mode."""
        wpilib.SmartDashboard.putString("Robot Status", "Auto Init")
        self.m_autonomousCommand = self.m_robotContainer.get_autonomous_command()

        if self.m_autonomousCommand is not None:
            self.m_autonomousCommand.schedule()

    def teleopInit(self):
        """Run once when the robot enters Teleoperated mode."""
        wpilib.SmartDashboard.putString("Robot Status", "Teleop Init")
        if self.m_autonomousCommand is not None:
            self.m_autonomousCommand.cancel()

    def teleopPeriodic(self):
        """Run periodically during Teleoperated mode."""
        pass


if __name__ == "__main__":
    wpilib.run(Robot)