#ifndef bmo_driver_h
#define bmo_driver_h

typedef struct bmo_message {
    int type;
    long code;
    int bits;
    int protocol;
} bmo_message;

bmo_message parseBMOMessage(String msg);
void sendCode(bmo_message message);
String getBMOJson();
String getScanJSON(const char * type, long code, int bitLength, int protocol);
int parseBMOType(char * bmoType);
char * getBMOTypeName(int type);

#endif
