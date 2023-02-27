#include <stdlib.h>
#include <string.h>
#include <stdio.h>

// char serial;
// //#define RELAY1  7                       
// void setup()
// {    
//   Serial.begin(9600);
//   //pinMode(RELAY1, OUTPUT);   
//   pinMode(LED_BUILTIN, OUTPUT);
//   digitalWrite(LED_BUILTIN, LOW);    
// }

// void loop()
// {
//   if(Serial.available() > 0)
//   {
//       serial = Serial.read();
//       Serial.println( serial, HEX);
//       if (serial=='s')
//       {
//         // digitalWrite(RELAY1,0);           
//         Serial.println("Light ON");
//         delay(10000);                                      
//         // digitalWrite(RELAY1,1);
//         // Serial.println("Test from Mayank");
//         // digitalWrite(LED_BUILTIN, HIGH);
//         Serial.println("Light OFF");
//         delay(10000);
//         // digitalWrite(LED_BUILTIN, LOW);
//       }
//    } 
// }

#include <FastLED.h>

#define LED_PIN     7
#define NUM_LEDS    48

CRGB leds[NUM_LEDS];

// struct Pair{
//   int num1;
//   int num2;
// };

int x;
// struct Pair y;
String  tp;

int grids(int m, int n){
  if(m == 4 && n == 3){
    return 6;
  }
  else if(m == 4 && n == 2){
    return 6;
  }
  else if(m == 4 && n == 1){
    return 7;
  }
  if(m == 3 && n == 1){
    return 4;
  }
  if(m == 2 && n == 1){
    return 4;
  }
  if(m == 1 && n == 1){
    return 3;
  }
  if(m == 0 && n == 1){
    return 3;
  }
}

// void temp(){
//   y.num1 = 4;
//   y.num2 = 4;
//   // Serial.print(x);
//   // printf("Hi: %d", &x);
//   FastLED.clear();
//   FastLED.show();
//   // while(!(y.num1 == x.num1 && y.num2 == x.num2)){
//   while(y.num1 == x.num1 && y.num2 == x.num2){
//     for(int i = 0 ; i<grids(y.num1,y.num2); i++){
//       leds[led_load + i] = CRGB(255, 0, 0);
//     }
//     led_load += grids(y.num1,y.num2);
//     FastLED.show();
//     FastLED.clear();
//     FastLED.show();
//     if(!(y.num2 == 0)){
//       y.num1 = 4;
//       y.num2 -= 1;
//     }
//     else{
//       y.num1 -= 1;
//       y.num2 = 4;
//     }
//   }
//   // for(int i = grids(y.num1, y.num2); i>0; i--){
//   //   leds[led_load] = CRGB(255, 0, 0);
//   //   leds[led_load+1] = CRGB(255, 0, 0);
//   //   leds[led_load+2] = CRGB(255, 0, 0);
//   //   leds[led_load+3] = CRGB(255, 0, 0);
//   //   FastLED.show();
//   //   delay(500);
//   //   FastLED.clear();
//   //   FastLED.show();
//   //   led_load += 4;
//   // }
//   // }
//   // if(x.num1 == ){
    
//   // }
//   // if(x.num1 == 0 && x.num2 == 0){
//   // leds[1] = CRGB(0, 255, 0);
//   // FastLED.show();
//   // delay(500);
//   // }
// }


int ledCount(int n){
  if(n == 1){
    return 34;
  }
  else if(n == 2){
    return 30;
  }
  else if(n == 3){
    return 27;
  }
  else if(n == 4){
    return 23;
  }
  else{
    if(n == 5){
      return 14;
    }
    else if(n == 6){
    return 10;
    }
    else if(n == 7){
      return 7;
    }
    else if(n == 8){
      return 3;
    }
    else if(n == 9){
      return 14;
    }
    else if(n == 10){
    return 11;
    }
    else if(n == 11){
      return 8;
    }
    else if(n == 12){
      return 4;
    }
  }
}

void temp(int n){
  FastLED.clear();
  FastLED.show();
  int idk = ledCount(n);
  if( n == -1){
    FastLED.clear();
  }
  // int led_load = 0;
  else{
    if(idk<15 && idk>2){
      // for(int i=0; i<4; i++)
      for(int i = 0; i<4; i++){
        leds[i] = CRGB(255,0,0);
      }
      for(int i = idk; i>-1; i--){
        leds[48-i] = CRGB(255,0,0);
      }
    }
    else{
      for(int i = 0; i<idk; i++){
        leds[i] = CRGB(255,0,0);
      }
    }
  }
  FastLED.show();
}


void setup() {
  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setBrightness(50);
  FastLED.clear();
  FastLED.show();
  Serial.begin(115200);
  Serial.setTimeout(1);
}

void loop() {
  while (!Serial.available());
  x = Serial.readString().toInt();
  temp(x);
}