//dynamic frequency generator
//for timer2

#include <avr/io.h>
#include <avr/interrupt.h>

unsigned long frequency = 1000;
//unsigned int speeds[] = { 1000, 5000, 7500, 10000, 12500, 14000, 16000, 18000 };

void setup() {
    pinMode(9,1);
    pinMode(10,1);
    
    Serial.begin(57600);
}

void loop() {
  unsigned long freq = 100;
  
  while (freq <= 1000000) {
    //Serial.println(freq);
    DFG(freq);
    delay(62.5);
    freq += 25;
  }
}

void DFG(unsigned long tempfreq) {
    // disable interupts
    cli();

    // registers for timer 1
    TCCR1A = 0;
    TCCR1B = 0;
    TCNT1 = 0;
    TCCR1A |= _BV(COM1A0) + _BV(COM1B0);
    TCCR1B |=_BV(WGM12); 
    TCCR1C = _BV(FOC1A);
    
    if (tempfreq > 122 && tempfreq < 1000001){
        OCR1A = (8000000 / tempfreq) - 1;   // #TIMER COUNTS
        TCCR1B |= _BV(CS10);
    }
    else if(tempfreq <= 122 && tempfreq > 15){
        OCR1A = (1000000 / tempfreq) - 1;
        TCCR1B |= _BV(CS11);
    }
    else if(tempfreq <= 15 && tempfreq > 4){
        OCR1A = (125000 / tempfreq) - 1;
        TCCR1B |= _BV(CS10) + _BV(CS11);
    }
  
  //TIMSK1 = _BV(OCIE1A);//TIMER1 COMPARE INTERUPT

  // enable interupts
  sei();
}

