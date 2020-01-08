#include "sqlite_operation.h"

char* class_needed_list[CLASS_NEEDED_NUM] = {"car", "truck", "bus"};

static int uselessCallback(void *NotUsed, int argc, char **argv, char **azColName) {
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

void SaveVehicleData(char* dataPath, detection_data *ddata, int ddataLen) {
    sqlite3 *db;
    char* zErrMsg = 0;
    char buf[1000];

    const char createTable[] = "CREATE TABLE %s\
                                (left FLOAT NOT NULL,\
                                 right FLOAT NOT NULL,\
                                 top FLOAT NOT NULL,\
                                 bot FLOAT NOT NULL\
                                 );";

    const char cleanData[] = "DELETE FROM %s;";

    const char insertData[] = "INSERT INTO %s VALUES(%f, %f, %f, %f);";

    sqlite3_open(dataPath, &db);
    for (int i = 0; i < CLASS_NEEDED_NUM; ++i) {
        // Create
        sprintf(buf, createTable, class_needed_list[i]);
        sqlite3_exec(db, buf, uselessCallback, 0, &zErrMsg);
        // Clean
        sprintf(buf, cleanData, class_needed_list[i]);
        sqlite3_exec(db, buf, uselessCallback, 0, &zErrMsg);
    }
    for (int dptr = 0; dptr < ddataLen; ++dptr) {
        for (int cn = 0; cn < CLASS_NEEDED_NUM; ++cn) {
            if (strcmp(ddata[dptr].label, class_needed_list[cn]) == 0) {
                sprintf(buf, insertData, 
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
    return;
}