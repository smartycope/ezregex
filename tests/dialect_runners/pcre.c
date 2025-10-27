#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define PCRE2_CODE_UNIT_WIDTH 8
#include <pcre2.h>
#include <cjson/cJSON.h>

#define OVECCOUNT 30 /* should be a multiple of 3 */

void myassert(int matched, int should_be, cJSON *i, const char *failing) {
    if ((matched != 0) != should_be) {
        const char *ezregex = cJSON_GetObjectItem(i, "ezregex")->valuestring;
        const char *regex   = cJSON_GetObjectItem(i, "regex")->valuestring;
        printf(
            "\n----------------------- TEST FAILED -----------------------\n"
            "language       = `c`\n"
            "pattern        = `%s`\n"
            "compiled regex = `%s`\n"
            "pattern should %smatch `%s`\n",
            ezregex, regex, should_be ? "" : "NOT ", failing
        );
        exit(1);
    }
}

char *read_file(const char *filename) {
    FILE *fp = fopen(filename, "rb");
    if (!fp) {
        perror("Failed to open file");
        exit(1);
    }
    fseek(fp, 0, SEEK_END);
    long len = ftell(fp);
    rewind(fp);
    char *data = malloc(len + 1);
    if (!data) {
        fprintf(stderr, "Out of memory\n");
        exit(1);
    }
    fread(data, 1, len, fp);
    data[len] = '\0';
    fclose(fp);
    return data;
}

int main() {
    const char *filename = "data/compiled_regexs.json";
    char *json_text = read_file(filename);

    cJSON *root = cJSON_Parse(json_text);
    if (!root) {
        fprintf(stderr, "Error parsing JSON\n");
        free(json_text);
        return 1;
    }

    cJSON *regexs = cJSON_GetObjectItem(root, "regexs");
    if (!cJSON_IsArray(regexs)) {
        fprintf(stderr, "Invalid JSON format\n");
        cJSON_Delete(root);
        free(json_text);
        return 1;
    }

    cJSON *i;
    cJSON_ArrayForEach(i, regexs) {
        const char *pattern = cJSON_GetObjectItem(i, "regex")->valuestring;

        const char *error;
        int erroffset;
        pcre2_code *re = pcre2_compile(pattern, 0, &error, &erroffset, NULL);
        if (!re) {
            fprintf(stderr, "Regex compilation failed at offset %d: %s\n", erroffset, error);
            exit(1);
        }

        cJSON *should = cJSON_GetObjectItem(i, "should");
        cJSON *shouldnt = cJSON_GetObjectItem(i, "shouldnt");

        cJSON *m;
        cJSON_ArrayForEach(m, should) {
            const char *text = m->valuestring;
            int ovector[OVECCOUNT];
            int rc = pcre2_match(re, text, strlen(text), 0, 0, ovector, OVECCOUNT);
            myassert(rc >= 0, 1, i, text);
        }

        cJSON_ArrayForEach(m, shouldnt) {
            const char *text = m->valuestring;
            int ovector[OVECCOUNT];
            int rc = pcre2_match(re, text, strlen(text), 0, 0, ovector, OVECCOUNT);
            myassert(rc >= 0, 0, i, text);
        }

        pcre2_code_free(re);
    }

    printf("pass\n");

    cJSON_Delete(root);
    free(json_text);
    return 0;
}
