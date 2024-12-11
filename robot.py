import wpilib
from commands2 import CommandScheduler
from robot_container import RobotContainer


class Robot(wpilib.TimedRobot):
    def robotInit(self):
        """Initialize the robot."""
        # Start data logging
        wpilib.DataLogManager.start()

        # Record both DS control and joystick data
        wpilib.DriverStation.startDataLog(wpilib.DataLogManager.getLog())

        print("Robot Initialized!")
        wpilib.DataLogManager.log("Robot Initialized!")
        self.m_robotContainer = RobotContainer()
        self.m_autonomousCommand = None

    def robotPeriodic(self):
        """Run code that should execute regardless of the robot's mode."""
        CommandScheduler.getInstance().run()

    # Rest of the Robot class remains the same...
    def disabledInit(self):
        pass

    def disabledPeriodic(self):
        pass

    def disabledExit(self):
        pass

    def autonomousInit(self):
        self.m_autonomousCommand = self.m_robotContainer.get_autonomous_command()

        if self.m_autonomousCommand is not None:
            self.m_autonomousCommand.schedule()

    def autonomousPeriodic(self):
        pass

    def autonomousExit(self):
        pass

    def teleopInit(self):
        if self.m_autonomousCommand is not None:
            self.m_autonomousCommand.cancel()

    def teleopPeriodic(self):
        pass

    def teleopExit(self):
        pass

    def testInit(self):
        CommandScheduler.getInstance().cancelAll()

    def testPeriodic(self):
        pass

    def testExit(self):
        pass

    def simulationPeriodic(self):
        pass


if __name__ == "__main__":
    wpilib.run(Robot)