#define STEPS_PER_REV 2000.0
#define GEAR_RATIO (50.0 + (4397.0/4913.0))
#define TOTAL_REV_STEPS long(round(STEPS_PER_REV * GEAR_RATIO))

volatile boolean clk = false;
volatile long counter = 0;

void setup() {
  // set pins as outputs
  pinMode(9, OUTPUT);

  // turn off interrupts
  cli();

  // configure timer2

  // clear TCCR2A/B registers and counter
  TCCR2A = 0;
  TCCR2B = 0;
  TCNT2  = 0;
  
  // turn on CTC mode
  TCCR2A |= (1 << WGM21);

  // set pre-scalar
  // Set CS21 bit for 8 prescaler
//  TCCR2B |= (1 << CS22);
  TCCR2B |= (1 << CS21);
//  TCCR2B |= (1 << CS20);

  // set compare match register
  // int(16,000,000 / (desired_freq * prescalar)) - 1
  // value must be <= 255
  OCR2A = 199;

  // enable timer compare interrupt
  TIMSK2 |= (1 << OCIE2A);

  // turn on interrupts
  sei();
}

ISR(TIMER2_COMPA_vect) {
  // toggle clock
  clk = !clk;

  // possibly set pin output
  if (counter < TOTAL_REV_STEPS) {
//    digitalWrite(9, clk ? HIGH : LOW);
    
    if (clk) {
      // set pin 9 high
      PORTB |= B00000010;
    }
    else {
      // set pin 9 low
      PORTB &= B11111101;

      counter += 1;
    }
  }
}

void loop() {
  // do other things here
}

