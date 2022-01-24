#include <string.h>
#include <stdio.h>
#define MOBO_TEMP_COMMAND "cat //sys//class//thermal//thermal_zone0//temp"
#define CPU_TEMP_COMMAND "cat //sys//class//thermal//thermal_zone1//temp"

int main(int argc, char *argv[]) { 
    system(MOBO_TEMP_COMMAND);
    system(CPU_TEMP_COMMAND);
}
