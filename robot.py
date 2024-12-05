#!/usr/bin/env python3

# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.

import wpilib
import commands2

class Robot(wpilib.TimedRobot):
    def robotInit(self) -> None:
        """
        This function is run when the robot is first started up and should be used for any
        initialization code.
        """
        self.autonomous_command: commands2.Command = None
        self.robot_container = RobotContainer()

    def robotPeriodic(self) -> None:
        """
        This function is called every 20 ms, no matter the mode.
        """
        commands2.CommandScheduler.getInstance().run()

    def disabledInit(self) -> None:
        """Called once when robot is disabled"""
        pass

    def disabledPeriodic(self) -> None:
        """Called periodically while disabled"""
        pass

    def disabledExit(self) -> None:
        """Called when robot leaves disabled mode"""
        pass

    def autonomousInit(self) -> None:
        """Called when autonomous mode starts"""
        self.autonomous_command = self.robot_container.getAutonomousCommand()

        if self.autonomous_command is not None:
            self.autonomous_command.schedule()

    def autonomousPeriodic(self) -> None:
        """Called periodically during autonomous"""
        pass

    def autonomousExit(self) -> None:
        """Called when autonomous mode ends"""
        pass

    def teleopInit(self) -> None:
        """Called when teleop mode starts"""
        if self.autonomous_command is not None:
            self.autonomous_command.cancel()

    def teleopPeriodic(self) -> None:
        """Called periodically during teleop"""
        pass

    def teleopExit(self) -> None:
        """Called when teleop mode ends"""
        pass

    def testInit(self) -> None:
        """Called when test mode starts"""
        commands2.CommandScheduler.getInstance().cancelAll()

    def testPeriodic(self) -> None:
        """Called periodically during test mode"""
        pass

    def testExit(self) -> None:
        """Called when test mode ends"""
        pass

    def simulationPeriodic(self) -> None:
        """Called periodically during simulation"""
        pass