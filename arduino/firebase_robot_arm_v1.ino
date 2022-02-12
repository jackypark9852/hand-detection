#include <Servo.h>
#include <ESP8266WIFI.h>
#include <FirbaseArduino.h>

#define numOfAngs 20 //with mcp & cmc joints
#define FIRBASE_HOST "robot-hand-153bf-default-rtdb.firebaseio.com"
#define FIRBASE_AUTH "c2EuhkDVzrCMeJZI8FRig8CxLusAuJknCRkoEoAG"
#define WIFI_SSID "iptime"
//#define WIFI_PASSWORD " "

int AngsRec[numOfAngs];

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
  for (int i = 0; i < 20; i++) {
    if (i < 15) servo[i].write(0);
    else servo[i].write(90);
  }
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

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to ");
  Serial.print(WIFI_SSID);
  while (WIFI.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected to ");
  Serial.println(WIFI_SSID);
  Serial.print("IP Address is : ");
  Serial.print(WiFi.localIP());

  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
}

void loop() {
    for (int j = 0; j < numOfAngs; j++) {
      AngsRec[j] = Firebase.getInt("angle %d", j);
      servo[j].write(AngsRec[k]);
    }
}
