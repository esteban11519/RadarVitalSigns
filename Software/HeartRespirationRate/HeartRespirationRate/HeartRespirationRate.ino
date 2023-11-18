// C++ code
//
/*
  Sweep

  by BARRAGAN <http://barraganstudio.com>
  This example code is in the public domain.

  modified 8 Nov 2013  by Scott Fitzgerald
  http://www.arduino.cc/en/Tutorial/Sweep
*/
// Libraries
#include <Servo.h>


#define pinServo 3

int pos = 0;

Servo servo;

void setup()
{
  // https://components101.com/motors/mg995-servo-motor
  servo.attach(pinServo, 500, 2500);
}

void loop()
{  
  servo.write(75);
  delay(100);
  servo.write(105);
  delay(100);
  
}