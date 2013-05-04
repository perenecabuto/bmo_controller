#include <RCSwitch.h>
#include <IRremote.h>

#define RF315 1
#define RF433 2
#define IR1 3
#define IR2 4

#define RF315_TX_PIN 10
#define RF315_RX_IRQ 0 // D-PIN 3
#define RF315_PULSE_LEN 297

#define IR1_RX_PIN 12

struct {
    int type;
    long code;
    int bits;
    int protocol;
} typedef bmo_message;

String getBMOJson();
String getScanJSON(const char * type, long code, int bitLength, int protocol);

void sendCode(bmo_message message);
bmo_message parseBMOMessage(String msg);
int parseBMOType(char * bmoType);
char * getBMOTypeName(int type);


RCSwitch rf315 = RCSwitch();
IRrecv ir1RX(IR1_RX_PIN);
IRsend ir1TX;

decode_results results;
String msg = "";
String json = "";
boolean messageCompleted = false;


void setup() {
    Serial.begin(9600);

    rf315.enableTransmit(RF315_TX_PIN);
    rf315.enableReceive(RF315_RX_IRQ);
    rf315.setPulseLength(RF315_PULSE_LEN);

    ir1RX.enableIRIn();
}

void loop() {
    messageCompleted = !Serial.available();

    while (Serial.available()) {
        msg += (char) Serial.read();
    }

    if (msg != "" && messageCompleted) {
        bmo_message message = parseBMOMessage(msg);

        sendCode(message);

        msg = "";
        messageCompleted = false;
    }

    json = getBMOJson();

    if (json != "") {
        Serial.println(json);
    }

    delay(10);
}


// RF315 9221153

bmo_message parseBMOMessage(String msg) {
    char bmoMessage[128];
    char bmoTypeName[8];
    bmo_message message;
    long code;

    msg.toCharArray(bmoMessage, 128);
    sscanf(bmoMessage, "%s %ld %d %d", bmoTypeName, &message.code, &message.bits, &message.protocol);

    message.type = parseBMOType(bmoTypeName);

    return message;
}

void sendCode(bmo_message message) {
    // TODO: retornar json de mensagem recebida
    switch (message.type) {
        case RF315:
            rf315.send(message.code, message.bits);
            break;

        case IR1:
            switch (message.protocol) {
                case NEC:
                    ir1TX.sendNEC(message.code, message.bits);
                    Serial.println("Ovo");
                    break;
                case SONY:
                    ir1TX.sendSony(message.code, message.bits);
                    break;
                case RC5:
                    ir1TX.sendRC5(message.code, message.bits);
                    break;
                case RC6:
                    ir1TX.sendRC6(message.code, message.bits);
                    break;
                case DISH:
                    ir1TX.sendDISH(message.code, message.bits);
                    break;
                case PANASONIC:
                    ir1TX.sendPanasonic(message.code, message.bits);
                    break;
                case JVC:
                    ir1TX.sendJVC(message.code, message.bits, 5);
                    break;
            }

        ir1RX.enableIRIn();
        ir1RX.resume();
    }
}


String getBMOJson() {
    String bmoJson = "";

    if (rf315.available()) {
        long value = rf315.getReceivedValue();

        if (value != 0) {
            bmoJson += getScanJSON(getBMOTypeName(RF315), value,
                rf315.getReceivedBitlength(),
                rf315.getReceivedProtocol()
            );
        }

        rf315.resetAvailable();
        delay(30);
    }

    if (ir1RX.decode(&results)) {
        long value = results.value;
        bmoJson += getScanJSON(getBMOTypeName(IR1), value, results.bits, results.decode_type);
        ir1RX.resume();
    }


    return bmoJson;
}

String getScanJSON(const char * type, long code, int bitLength, int protocol) {
    char format[] = "{\"type\": \"%s\", \"code\": %ld, \"bits\": %d, \"protocol\": %d}",
         buffer[200];

    sprintf(buffer, format, type, code, bitLength, protocol);

    return String(buffer);
}


int parseBMOType(char * bmoType) {
    if (strncmp("RF315", bmoType, 8) == 0) {
        return RF315;
    }
    else if (strncmp("RF433", bmoType, 8) == 0) {
        return RF433;
    }
    else if (strncmp("IR1", bmoType,  8) == 0) {
        return IR1;
    }
    else if (strncmp("IR2", bmoType,  8) == 0) {
        return IR2;
    }
}

char * getBMOTypeName(int type) {
    switch (type) {
        case RF315:
            return "RF315";

        case RF433:
            return "RF433";

        case IR1:
            return "IR1";

        case IR2:
            return "IR2";
    }
}
