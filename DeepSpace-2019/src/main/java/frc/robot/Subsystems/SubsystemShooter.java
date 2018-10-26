/*----------------------------------------------------------------------------*/
/* Copyright (c) 2018 FIRST. All Rights Reserved.                             */
/* Open Source Software - may be modified and shared by FRC teams. The code   */
/* must be accompanied by the FIRST BSD license file in the root directory of */
/* the project.                                                               */
/*----------------------------------------------------------------------------*/

package frc.robot.Subsystems;

import edu.wpi.first.wpilibj.command.Subsystem;

/**
 * Add your docs here.
 */
public class SubsystemShooter extends Subsystem {
  // Put methods for controlling this subsystem
  // here. Call these from Commands.

  public SubsystemShooter {
    shooter = new TalonSRX(Constants.Shooter_ID);
  }

  public void shoot(Joystick joy) {
    speed = Util.Joystick.SCALAR(joy);
    shooter.set(ControlMode.PercentOutput, speed);
  }

  public void stopShooting() {
    shooter.set(ControlMode.PercentOutput, 0);
  }

  @Override
  public void initDefaultCommand() {
    // Set the default command for a subsystem here.
    // setDefaultCommand(new MySpecialCommand());
  }
}
