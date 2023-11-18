#include <Arduino_FreeRTOS.h>
// Include mutex support
#include <semphr.h>

/*
   Declaring a global variable of type SemaphoreHandle_t

*/
SemaphoreHandle_t myMutex;


int statusLed = 0;
// Define tasks

// Pulse rate 60 t0 100 beats per minute
void TaskPulseRate( void *pvParameters );
// 12 to 16 breaths per minute
void TaskRespirationRate( void *pvParameters );

// the setup function runs once when you press reset or power the board
void setup() {
  
  Serial.begin(9600);

  /**
       Create a mutex.
       https://www.freertos.org/CreateMutex.html
  */
  myMutex = xSemaphoreCreateMutex();
  if (myMutex != NULL) {
    Serial.println("Mutex created");
  }
  
  // initialize digital LED_BUILTIN on pin 13 as an output.
  

  // Now set up two tasks to run independently.
  xTaskCreate(
    TaskRespirationRate
    ,  "RespirationRate"   // A name just for humans
    ,  128  // This stack size can be checked & adjusted by reading the Stack Highwater
    ,  NULL
    ,  2  // Priority, with 3 (configMAX_PRIORITIES - 1) being the highest, and 0 being the lowest.
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
  // initialize digital LED_BUILTIN on pin 13 as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  
  int respirationRate = 3000; // milliseconds
  
  // obtenemos la primer referencia temporal
  TickType_t lastWakeupRespirationRate = xTaskGetTickCount();
  

  for (;;) // A Task shall never return or exit.
  {
    // pdMS_TO_TICKS: Milliseconds to ticks
    vTaskDelayUntil( &lastWakeupRespirationRate, pdMS_TO_TICKS( respirationRate ) );
    
    // Task in Mutex
    xSemaphoreTake(myMutex,portMAX_DELAY);
    digitalWrite(LED_BUILTIN, statusLed);
    statusLed = !statusLed;
    xSemaphoreGive(myMutex);
    
    
  }
}

void TaskPulseRate(void *pvParameters)  // This is a task.
{
  (void) pvParameters;
  int pulseRate = 600; // milliseconds
   
  // obtenemos la primer referencia temporal
  TickType_t lastWakeupPulseRate = xTaskGetTickCount();
  

  for (;;) // A Task shall never return or exit.
  {
    vTaskDelayUntil( &lastWakeupPulseRate, pdMS_TO_TICKS( pulseRate ) );
    
    // Task in Mutex
    xSemaphoreTake(myMutex,portMAX_DELAY);
    digitalWrite(LED_BUILTIN, statusLed);
    statusLed = !statusLed;
    xSemaphoreGive(myMutex);
    
    
  }
}

// References
/*
https://www.hopkinsmedicine.org/health/conditions-and-diseases/vital-signs-body-temperature-pulse-rate-respiration-rate-blood-pressure
https://www.youtube.com/watch?v=U5Vep8vjcEQ
https://circuitdigest.com/microcontroller-projects/arduino-freertos-tutorial-using-semaphore-and-mutex-in-freertos-with-arduino
vTaskDelayUntil: 
- http://fjrg76.com/2021/09/30/funciones-de-retardo-en-freertos/
- https://www.freertos.org/vtaskdelayuntil.html

*/
