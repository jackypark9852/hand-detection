#include <Servo.h>
#include <String.h> //split 함수 (string tokenization)
#define numOfAngs 20 //with mcp & cmc joints
#define digitsPerAng 2 //cmc joint has 3 digits

int AngsRec[numOfAngs];
int stringLength = numOfAngs * digitsPerAng + 2; //$ sign + cmc joint
int count = 0;
bool startCount = false;
String receivedString;

Servo servo[numOfAngs];

enum {
  servoThumb_cmc = 0,
  servoThumb_mcp_y,
  servoThumb_dip,
  servoIndex_mcp_y,
  servoIndex_pip,
  servoIndex_dip,
  servoMiddle_mcp_y,
  servoMiddle_pip,
  servoMiddle_dip,
  servoRing_mcp_y,
  servoRing_pip,
  servoRing_dip,
  servoPinky_mcp_y,
  servoPinky_pip,
  servoPinky_dip,
  servoThumb_mcp_x,
  servoIndex_mcp_x,
  servoMiddle_mcp_x,
  servoRing_mcp_x,
  servoPinky_mcp_x
};


void setup() {
  Serial.begin(115200);
  servo[19].write(0); //cmc joint angle start from 0
  servo[0].attach(1);
  servo[1].attach(2);
  servo[2].attach(3);
  servo[3].attach(4);
  servo[4].attach(5);
  servo[5].attach(6);
  servo[6].attach(7);
  servo[7].attach(8);
  servo[8].attach(9);
  servo[9].attach(10);
  servo[10].attach(11);
  servo[11].attach(12);
  servo[12].attach(13);
  servo[13].attach(14);
  servo[14].attach(15);
  servo[15].attach(16);
  servo[16].attach(17);
  servo[17].attach(18);
  servo[18].attach(19);
  servo[19].attach(20);
}

void receiveData() {
  while (Serial.available()) {
    receivedString = Serial.readString();
    if (c == '$') {
      startCount = true;
    }
    if (startCount == true) {
      if (count < stringLength) {
        receivedString = String(receivedString + c);
        count++;
      }
      if (count >= stringLength) {
        for (int i = 0; i < numOfAngs - 1; i++) {
          int num = (i * digitsPerAng) + 1;
          AngsRec[i] = receivedString.substring(num, num + digitsPerAng).toInt();
        }
        AngsRec[numOfAngs - 1] = receivedString.substring(39, 42).toInt(); //3 digit cmc joint angle
        receivedString = "";
        count = 0;
        startCount = false;
      }
    }
  }
}

void loop() {
    receiveData();
    for (int j = 0; j < 19; j++) {
      servo[j].write(90 + AngsRec[j]);
    }
    servo[19].write(AngsRec[19]); //cmc joint
}
