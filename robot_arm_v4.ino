#include <Servo.h>
#include <String.h> //split 함수 (string tokenization)
#define numOfAngs 20 //with mcp & cmc joints

int AngsRec[numOfAngs];
String receivedString;

const byte numChars = 200;
char receivedChars[numChars];
char tempChars[numChars];        // temporary array for use when parsing

boolean newData = false;
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
  Serial.begin(9600);
  servo[0].attach(10);
//  servo[19].write(0); //cmc joint angle start from 0
//  servo[0].attach(1);
//  servo[1].attach(2);
//  servo[2].attach(3);
//  servo[3].attach(4);
//  servo[4].attach(5);
//  servo[5].attach(6);
//  servo[6].attach(7);
//  servo[7].attach(8);
//  servo[8].attach(9);
//  servo[9].attach(10);
//  servo[10].attach(11);
//  servo[11].attach(12);
//  servo[12].attach(13);
//  servo[13].attach(14);
//  servo[14].attach(15);
//  servo[15].attach(16);
//  servo[16].attach(17);
//  servo[17].attach(18);
//  servo[18].attach(19);
//  servo[19].attach(20);
  for (int i = 0; i < numOfAngs; i++) {
    if (i < 15) servo[i].write(0);
    else servo[i].write(90);
  }
}

//============

void loop() {
  recvWithStartEndMarkers();
  if (newData == true) {
    strcpy(tempChars, receivedChars);
    // this temporary copy is necessary to protect the original data
    //   because strtok() used in parseData() replaces the commas with \0
    parseData();
    showParsedData();
    servo[0].write(AngsRec[7]);
    newData = false;
  }
}

//============

void recvWithStartEndMarkers() {
  static boolean recvInProgress = false;
  static byte ndx = 0;
  char startMarker = '<';
  char endMarker = '>';
  char rc;

  while (Serial.available() > 0 && newData == false) {
    rc = Serial.read();

    if (recvInProgress == true) {
      if (rc != endMarker) {
        receivedChars[ndx] = rc;
        ndx++;
        if (ndx >= numChars) {
          ndx = numChars - 1;
        }
      }
      else {
        receivedChars[ndx] = '\0'; // terminate the string
        recvInProgress = false;
        ndx = 0;
        newData = true;
      }
    }

    else if (rc == startMarker) {
      recvInProgress = true;
    }
  }
}

//============<1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20>

void parseData() {      // split the data into its parts
  char * strtokIndx; // this is used by strtok() as an index
  Serial.println(tempChars);
  strtokIndx = strtok(tempChars, ",");
  for (int i = 0; i < numOfAngs; ++i) {
    AngsRec[i] = atoi(strtokIndx);
    strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
  }
}

//============

void showParsedData() {
  for (int i = 0; i < numOfAngs; ++i) {
    Serial.println(AngsRec[i]);
  }
}
