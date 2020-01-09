#ifndef SQLITE_OPERATION_H_
#define SQLITE_OPERATION_H_

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "darknet.h"
#include <sqlite3.h>

#define CLASS_NEEDED_NUM (3)

#ifndef DETECTION_DATA_FLAG
#define DETECTION_DATA_FLAG
typedef struct detection_data{
    char label[4096];
    double left_normalize;
    double right_normalize;
    double top_normalize;
    double bot_normalize;
} detection_data;
#endif

int SqlTest(void);
void saveVehicleData(const char* dataPath, detection_data *ddata, int ddataLen);
int getVehicleFlag(const char* dataPath, const char* flagName);
void setVehicleFlag(const char* dataPath, const char* flagName, int flag);

#endif