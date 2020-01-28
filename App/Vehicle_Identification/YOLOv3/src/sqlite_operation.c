#include "sqlite_operation.h"

char buf[1000];
char* class_needed_list[CLASS_NEEDED_NUM] = {"car", "truck", "bus"};
const char createVehicleTable[] = "CREATE TABLE %s\
                            (left FLOAT NOT NULL,\
                             right FLOAT NOT NULL,\
                             top FLOAT NOT NULL,\
                             bot FLOAT NOT NULL\
                             );";
const char insertVehicleData[] = "INSERT INTO %s VALUES(%f, %f, %f, %f);";
const char cleanData[] = "DELETE FROM %s;";
const char createFlagTable[] = "CREATE TABLE flag\
                            (name TEXT NOT NULL,\
                             flag BOOLEAN NOT NULL\
                             );";
const char insertFlagData[] = "INSERT INTO flag SELECT \"%s\", %d \
                               WHERE NOT EXISTS (SELECT * FROM flag WHERE name is \"%s\");";
const char updateFlagData[] = "UPDATE flag SET flag = %d WHERE name = \"%s\";";
const char getFlagData[] = "SELECT flag from flag WHERE name is \"%s\";";

static int uselessCallback(void *NotUsed, int argc, char **argv, char **azColName) {
    return 0;
}

static int getFlagCallback(void *flag, int argc, char **argv, char **azColName) {
    if (argc >= 1) {
        if (strcmp(argv[0], "1") == 0)
            *((int*)flag) = 1;
        else
            *((int*)flag) = 0;
    } else {
        *((int*)flag) = 0;
    }
    return 0;
}

int SqlTest() {
    sqlite3 *db;
    char* zErrMsg = 0;
    sqlite3_open("/Lab/test.db", &db);
    char sql[] = "CREATE TABLE student(ID INT NOT NULL, NAME TEXT NOT NULL);";
    char sql_i[] = "INSERT INTO student VALUES(17211401, \"Liao Chen\");";
    sqlite3_exec(db, sql, uselessCallback, 0, &zErrMsg);
    sqlite3_exec(db, sql_i, uselessCallback, 0, &zErrMsg);
    sqlite3_close(db);

    return 0;
}

void saveVehicleData(const char* dataPath, detection_data *ddata, int ddataLen) {
    sqlite3 *db;
    char* zErrMsg = 0;

    sqlite3_open(dataPath, &db);
    for (int i = 0; i < CLASS_NEEDED_NUM; ++i) {
        // Create
        sprintf(buf, createVehicleTable, class_needed_list[i]);
        sqlite3_exec(db, buf, uselessCallback, 0, &zErrMsg);
        // Clean
        sprintf(buf, cleanData, class_needed_list[i]);
        sqlite3_exec(db, buf, uselessCallback, 0, &zErrMsg);
    }
    for (int dptr = 0; dptr < ddataLen; ++dptr) {
        for (int cn = 0; cn < CLASS_NEEDED_NUM; ++cn) {
            if (strcmp(ddata[dptr].label, class_needed_list[cn]) == 0) {
                sprintf(buf, insertVehicleData, 
                        class_needed_list[cn],
                        ddata[dptr].left_normalize,
                        ddata[dptr].right_normalize,
                        ddata[dptr].top_normalize,
                        ddata[dptr].bot_normalize
                        );
                sqlite3_exec(db, buf, uselessCallback, 0, &zErrMsg);
                break;
            }
        }
    }
    sqlite3_close(db);
    return;
}

int getVehicleFlag(const char* dataPath, const char* flagName) {
    int flag;
    sqlite3 *db;
    char* zErrMsg = 0;

    sqlite3_open(dataPath, &db);

    sprintf(buf, getFlagData, flagName);
    sqlite3_exec(db, buf, getFlagCallback, (void*)(&flag), &zErrMsg);

    sqlite3_close(db);
    return flag;
}

void setVehicleFlag(const char* dataPath, const char* flagName, int flag) {
    sqlite3 *db;
    char* zErrMsg = 0;

    sqlite3_open(dataPath, &db);

    sprintf(buf, createFlagTable);
    sqlite3_exec(db, buf, uselessCallback, 0, &zErrMsg);

    sprintf(buf, insertFlagData, flagName, flag, flagName);
    sqlite3_exec(db, buf, uselessCallback, 0, &zErrMsg);

    sprintf(buf, updateFlagData, flag, flagName);
    sqlite3_exec(db, buf, uselessCallback, 0, &zErrMsg);

    sqlite3_close(db);
    return;
}