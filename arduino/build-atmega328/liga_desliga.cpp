#include <Arduino.h>
#include <RCSwitch.h>

RCSwitch rf315 = RCSwitch();

String msg = "";
String json = "";
long code = 0;

void setup() {
    Serial.begin(9600);

    rf315.enableTransmit(10);
    rf315.enableReceive(1); // Dport 4
    rf315.setPulseLength(297);
}

String getScanJSON(const char * type, long code, int bitLength, int protocol);

// A - 9221153
void loop() {
    msg = "", json = "", code = 0;

    while (Serial.available()) {
        msg += (char) Serial.read();
    }

    code = msg.toInt();

    if (code > 0) {
        rf315.send(code, 24);
    }

    if (rf315.available()) {
        long value = rf315.getReceivedValue();

        if (value != 0) {
            json = getScanJSON("rf315", value,
                rf315.getReceivedBitlength(),
                rf315.getReceivedProtocol()
            );
        }

        rf315.resetAvailable();
    }

    if (json != "") {
        Serial.println(json);
    }

    delay(30);
}

String getScanJSON(const char * type, long code, int bitLength, int protocol) {
    char format[] = "{ \"type\": \"%s\", \"code\": %s, \"bits\": %d, \"protocol\": \"%d\" }",
        buffer[200],
        cCode[20];

    String(code).toCharArray(cCode, 20);
    sprintf(buffer, format, type, cCode, bitLength, protocol);

    return String(buffer);
}
