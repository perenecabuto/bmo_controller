#include <RCSwitch.h>

#define RF315 1
#define RF433 2
#define IR1 3
#define IR2 4

# define RF315_TX_DPORT 10
# define RF315_RX_IRQ 0 // Dport 4
# define RF315_PULSE_LEN 297

struct bmo_message {
    int code;
    int type;
} typedef bmo_message;

String getBMOJson();
String getScanJSON(const char * type, long code, int bitLength, int protocol);
void sendCode(bmo_message message);
bmo_message parseBMOMessage(String msg);
int parseBMOType(char * bmoType);


RCSwitch rf315 = RCSwitch();

String msg = "";
String json = "";


void setup() {
    Serial.begin(9600);

    rf315.enableTransmit(RF315_TX_DPORT);
    rf315.enableReceive(RF315_RX_IRQ);
    rf315.setPulseLength(RF315_PULSE_LEN);
}

void loop() {
    msg = "";

    while (Serial.available()) {
        msg += (char) Serial.read();
    }

    bmo_message parsedMessage = parseBMOMessage(msg);

    if (parsedMessage.code) {
        sendCode(parsedMessage);
    }

    json = getBMOJson();

    if (json != "") {
        Serial.println(json);
    }

    delay(30);
}


bmo_message parseBMOMessage(String msg) {
    char * bmoMessage;
    char * bmoType;
    bmo_message message;

    msg.toCharArray(bmoMessage, 128);
    sscanf(bmoMessage, "%s %d", bmoType, &message.code);
    free(bmoMessage);

    message.type = parseBMOType(bmoType);

    return message;
}

int parseBMOType(char * bmoType) {
    if (strncmp("RF315", bmoType,  sizeof(bmoType))) {
        return RF315;
    }
    else if (strncmp("RF433", bmoType,  sizeof(bmoType))) {
        return RF433;
    }
    else if (strncmp("IR1", bmoType,  sizeof(bmoType))) {
        return IR1;
    }
}

void sendCode(bmo_message message) {
    switch (message.type) {
        case RF315:
            // TODO: pegar codigo e protocolo
            rf315.send(message.code, 24);
            break;
    }
}

String getBMOJson() {
    String bmoJson = "";

    Serial.println("json - 1");
    if (rf315.available()) {
        long value = rf315.getReceivedValue();

        if (value != 0) {
            bmoJson += getScanJSON("rf315", value,
                rf315.getReceivedBitlength(),
                rf315.getReceivedProtocol()
            );
        }

        rf315.resetAvailable();
    }
    Serial.println(bmoJson);
    Serial.println("json - 2");

    return bmoJson;
}

String getScanJSON(const char * type, long code, int bitLength, int protocol) {
    char format[] = "{ \"type\": \"%s\", \"code\": %s, \"bits\": %d, \"protocol\": \"%d\" }",
        buffer[200],
        cCode[20];

    String(code).toCharArray(cCode, 20);
    sprintf(buffer, format, type, cCode, bitLength, protocol);

    return String(buffer);
}
