#include<Servo.h>
#include<Wire.h>
#include <Adafruit_PWMServoDriver.h>
int servoPinX = A4;
int servoPinY = A5;
int laserPin = A7;
Servo serX;
Servo serY;

String serialData;

void setup() {

  // serX.attach(servoPinX);
  // serY.attach(servoPinY);
  // pinMode(laserPin, OUTPUT);
  Wire.begin();
  Serial.begin(9600);
  Serial.setTimeout(10);
  // digitalWrite(laserPin, LOW);
}

void loop() {
}

void serialEvent() {
  serialData = Serial.readString();
  // digitalWrite(laserPin, HIGH);
  // if ( serialData.charAt(2) == 'Y') {
  //   i == 2;
  // } else if (serialData.charAt(3) == 'Y') {
  //   i == 3;
  // } else {
  //   i == 4;
  // }
  
  serX.write(parseDataX(serialData));
  serY.write(parseDataY(serialData));
  // serX.write(serialData.substring(1, i).toInt());
  // serY.write(serialData.substring(i+1).toInt());
}

int parseDataX(String data){
  data.remove(data.indexOf("Y"));
  data.remove(0, 1);
  return data.toInt();
  // return data.substring(1, data.indexOf("Y")).toInt();
}

int parseDataY(String data){
  
  data.remove(0, data.indexOf("Y") + 1);
  return data.toInt();
  // return data.substring(data.indexOf("Y")+1, data.length()).toInt();
}

