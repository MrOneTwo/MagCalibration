#include <TimerOne.h>

#define PREAMBLE       0xAA
#define MSG_SIZE       4

uint8_t dataBuffer[MSG_SIZE];
char inbuff;

void setup(void)
{
  // it takes micro seconds as argument (1 is the lowest)
  Timer1.initialize(100000);
  Timer1.stop();
  Timer1.attachInterrupt(sendData);
  Serial.begin(115200);
  Serial.println("ARD - OK\n");
  delay(2000);
  Serial.flush();

  inbuff = 'g';

}

void loop(void)
{
  if (Serial.available() > 0) {
    inbuff = Serial.read();
  }

  if (inbuff == 'g'){
    Timer1.start();
    //interrupts();
  }

  if (inbuff == 's'){
    Timer1.stop();
    //noInterrupts();
  }

}

void sendData(void)
{
  dataBuffer[0] = PREAMBLE;
  dataBuffer[1] = random(0, 100);
  dataBuffer[2] = random(0, 100);
  dataBuffer[3] = random(0, 100);
  
  //for(int i = 0; i < MSG_SIZE; i++){
      Serial.write(dataBuffer, 4);
  //}
  
}
