#include <Servo.h>
#include <Arduino_FreeRTOS.h>

#define pinServoPulseRate 5
#define pinServoRespirationRate 6


/* Global variables */

Servo servoPulseRate;
Servo servoRespirationRate;

int servoReferencePulseRate = 105 ; // Grades
int servoAnglePulseRate = 3 ;    // Delta/2 grades

int servoReferenceRespirationRate = 83 ; // Grades
int servoAngleRespirationRate = 63 ;    // Delta/2 grades

// Pulse rate 60 to 100 beats per minute
int pulseRate = 80; // beats per minute
// 12 to 16 breaths per minute
int respirationRate = 14; // breaths per minute


/*  Define tasks */
void TaskPulseRate( void *pvParameters );
void TaskRespirationRate( void *pvParameters );

// the setup function runs once when you press reset or power the board
void setup() {
  

  // Now set up two tasks to run independently.
  xTaskCreate(
    TaskRespirationRate
    ,  "RespirationRate"   // A name just for humans
    ,  128  // This stack size can be checked & adjusted by reading the Stack Highwater
    ,  NULL
    ,  1  // Priority, with 3 (configMAX_PRIORITIES - 1) being the highest, and 0 being the lowest.
    ,  NULL );

  xTaskCreate(
    TaskPulseRate
    ,  "PulseRate"
    ,  128  // Stack size
    ,  NULL
    ,  1  // Priority
    ,  NULL );

  // Now the task scheduler, which takes over control of scheduling individual tasks, is automatically started.
}

void loop()
{
  // Empty. Things are done in Tasks.
}

/*--------------------------------------------------*/
/*---------------------- Tasks ---------------------*/
/*--------------------------------------------------*/

void TaskRespirationRate(void *pvParameters)  // This is a task.
{
  (void) pvParameters;
  // Configure servo parameters.
  servoRespirationRate.attach(pinServoRespirationRate, 500, 2500);
  
  int respirationRatePeriod = 60000/respirationRate; // milliseconds
  
  // obtenemos la primer referencia temporal
  TickType_t lastWakeupRespirationRate = xTaskGetTickCount();
  

  for (;;) // A Task shall never return or exit.
  {
    // pdMS_TO_TICKS: Milliseconds to ticks
    vTaskDelayUntil( &lastWakeupRespirationRate, pdMS_TO_TICKS( respirationRatePeriod ) );
    
    servoRespirationRate.write(servoReferenceRespirationRate + servoAngleRespirationRate);
    servoAngleRespirationRate = -servoAngleRespirationRate;
    
    
  }
}

void TaskPulseRate(void *pvParameters)  // This is a task.
{
  (void) pvParameters;
  // Configure servo parameters.
  servoPulseRate.attach(pinServoPulseRate, 500, 2500);

  int pulseRatePeriod = 60000/pulseRate; // milliseconds
   
  // obtenemos la primer referencia temporal
  TickType_t lastWakeupPulseRate = xTaskGetTickCount();
  

  for (;;) // A Task shall never return or exit.
  {
    vTaskDelayUntil( &lastWakeupPulseRate, pdMS_TO_TICKS( pulseRatePeriod ) );
    
    servoPulseRate.write(servoReferencePulseRate + servoAnglePulseRate);
    servoAnglePulseRate = -servoAnglePulseRate;
    
  }
}

// References
/*
Theory:
- https://www.luisllamas.es/como-usar-freertos-en-arduino/
https://www.hopkinsmedicine.org/health/conditions-and-diseases/vital-signs-body-temperature-pulse-rate-respiration-rate-blood-pressure
https://www.youtube.com/watch?v=U5Vep8vjcEQ
https://circuitdigest.com/microcontroller-projects/arduino-freertos-tutorial-using-semaphore-and-mutex-in-freertos-with-arduino
vTaskDelayUntil: 
- http://fjrg76.com/2021/09/30/funciones-de-retardo-en-freertos/
- https://www.freertos.org/vtaskdelayuntil.html

*/
