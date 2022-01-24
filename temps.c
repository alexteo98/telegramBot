#include <string.h>
#include <stdio.h>

#define String HDD_TEMPS_COMMAND "hddtemp /dev/sdc /dev/sdb"

int main(int argc, char *argv[]){
//  getreuid(geteuid(), geteuid());
  setuid(0);
  seteuid(0);
  system("hddtemp /dev/sd?");
}
