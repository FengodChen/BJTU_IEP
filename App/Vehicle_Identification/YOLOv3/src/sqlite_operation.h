#ifndef SQLITE_OPERATION_H_
#define SQLITE_OPERATION_H_

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "darknet.h"
#include <sqlite3.h>

#define CLASS_NEEDED_NUM (3)

#ifndef SB
#define SB
typedef struct detection_data{
    char label[4096];
    double left_normalize;
    double right_normalize;
    double top_normalize;
    double bot_normalize;
} detection_data;
#endif

int SqlTest(void);
void SaveVehicleData(char* dataPath, detection_data *ddata, int ddataLen);

#endif