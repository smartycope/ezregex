#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define PCRE2_CODE_UNIT_WIDTH 8
#include <pcre2.h>
#include <cjson/cJSON.h>



void myassert(int matched, int should_be, cJSON *i, const char *failing) {
    if ((matched != 0) != should_be) {
        const char *ezregex = cJSON_GetObjectItem(i, "ezregex")->valuestring;
        const char *regex   = cJSON_GetObjectItem(i, "regex")->valuestring;
        printf(
            "\n----------------------- TEST FAILED -----------------------\n"
            "language       = `pcre2`\n"
            "pattern        = `%s`\n"
            "compiled regex = `%s`\n"
            "pattern should %smatch `%s`\n",
            ezregex, regex, should_be ? "" : "NOT ", failing
        );
        exit(1);
    }
}

static void print_fail_repl(cJSON *i, const char *actual) {
    const char *ezregex = cJSON_GetObjectItem(i, "ezregex")->valuestring;
    const char *regex   = cJSON_GetObjectItem(i, "regex")->valuestring;
    const char *ezrepl  = cJSON_GetObjectItem(i, "ezrepl")->valuestring;
    const char *repl    = cJSON_GetObjectItem(i, "repl")->valuestring;
    const char *base    = cJSON_GetObjectItem(i, "base")->valuestring;
    const char *after   = cJSON_GetObjectItem(i, "after")->valuestring;
    fprintf(stderr,
"\n----------------------- TEST FAILED -----------------------\n"
"language       = `pcre2`\n"
"pattern        = `%s`\n"
"compiled regex = `%s`\n"
"replacement    = `%s`\n"
"compiled repl  = `%s`\n"
"base           = `%s`\n"
"after          = `%s`\n"
"actual result  = `%s`\n"
"\nReplacing\n"
"    `%s`\n"
"with\n"
"    `%s`\n"
"in\n"
"    `%s`\n"
"yielded\n"
"    `%s`\n"
"not\n"
"    `%s`\n\n",
        ezregex,
        regex,
        ezrepl,
        repl,
        base,
        after,
        actual,
        ezregex,
        ezrepl,
        base,
        actual,
        after
    );
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

int main(void) {
    // Regex tests
    const char *filename = "data/compiled_regexs.json";
    char *json_text = read_file(filename);

    cJSON *root = cJSON_Parse(json_text);
    if (!root) {
        fprintf(stderr, "Error parsing JSON\n");
        free(json_text);
        return 1;
    }

    cJSON *regexs = cJSON_GetObjectItem(root, "pcre2");
    if (!cJSON_IsArray(regexs)) {
        fprintf(stderr, "Invalid JSON format\n");
        cJSON_Delete(root);
        free(json_text);
        return 1;
    }

    cJSON *i;
    cJSON_ArrayForEach(i, regexs) {
        const char *pattern = cJSON_GetObjectItem(i, "regex")->valuestring;

        int error_number;
        PCRE2_SIZE error_offset;
        pcre2_code *re = pcre2_compile(pattern, PCRE2_ZERO_TERMINATED, 0, &error_number, &error_offset, NULL);
        if (!re) {
            fprintf(stderr, "Regex compilation failed at offset %d: %d\n", error_offset, error_number);
            myassert(0, 1, i, pattern);
        }

        cJSON *should = cJSON_GetObjectItem(i, "should");
        cJSON *shouldnt = cJSON_GetObjectItem(i, "shouldnt");

        pcre2_match_data *match_data = pcre2_match_data_create_from_pattern(re, NULL);

        cJSON *m;
        cJSON_ArrayForEach(m, should) {
            const char *text = m->valuestring;
            int rc = pcre2_match(re, text, strlen(text), 0, 0, match_data, NULL);
            myassert(rc >= 0, 1, i, text);
        }

        cJSON_ArrayForEach(m, shouldnt) {
            const char *text = m->valuestring;
            int rc = pcre2_match(re, text, strlen(text), 0, 0, match_data, NULL);
            myassert(rc >= 0, 0, i, text);
        }

        pcre2_code_free(re);
    }

    // Replacement tests
    json_text = read_file("data/compiled_replacements.json");

    root = cJSON_Parse(json_text);
    if (!root) {
        fprintf(stderr, "Error parsing JSON\n");
        free(json_text);
        return 1;
    }

    regexs = cJSON_GetObjectItem(root, "pcre2");
    if (!cJSON_IsArray(regexs)) {
        fprintf(stderr, "Invalid JSON format\n");
        cJSON_Delete(root);
        free(json_text);
        return 1;
    }

    cJSON_ArrayForEach(i, regexs) {
        const char *pattern = cJSON_GetObjectItem(i, "regex")->valuestring;
        const char *repl = cJSON_GetObjectItem(i, "repl")->valuestring;
        const char *base = cJSON_GetObjectItem(i, "base")->valuestring;
        const char *after = cJSON_GetObjectItem(i, "after")->valuestring;

        int errornumber;
        PCRE2_SIZE erroffset;
        pcre2_code *re = pcre2_compile(
            (PCRE2_SPTR)pattern,
            PCRE2_ZERO_TERMINATED,
            0,
            &errornumber,
            &erroffset,
            NULL
        );

        if (!re) {
            PCRE2_UCHAR buffer[256];
            pcre2_get_error_message(errornumber, buffer, sizeof(buffer));
            fprintf(stderr, "Error compiling `%s` at offset %zu: %s\n", pattern, erroffset, buffer);
            exit(1);
        }

        pcre2_match_data *match_data = pcre2_match_data_create_from_pattern(re, NULL);
        PCRE2_SIZE out_len = strlen(base) * 4 + 128; // generous buffer
        char *outbuf = calloc(out_len, 1);
        if (!outbuf) {
            fprintf(stderr, "Out of memory\n");
            return 1;
        }

        int rc = pcre2_substitute(
            re,
            (PCRE2_SPTR)base,
            PCRE2_ZERO_TERMINATED,
            0,
            PCRE2_SUBSTITUTE_GLOBAL, // replace all occurrences
            match_data,
            NULL,
            (PCRE2_SPTR)repl,
            PCRE2_ZERO_TERMINATED,
            (PCRE2_UCHAR *)outbuf,
            &out_len
        );

        if (rc < 0) {
            if (rc == PCRE2_ERROR_NOMEMORY)
                fprintf(stderr, "Replacement output buffer too small\n");
            else
                fprintf(stderr, "Error replacing `%s`: PCRE2 error %d\n", pattern, rc);
        }

        if (strcmp(outbuf, after) != 0 || rc < 0){
            print_fail_repl(i, outbuf);
            free(outbuf);
            return 1;
        }

        free(outbuf);
    }

    printf("pass\n");

    cJSON_Delete(root);
    free(json_text);
    return 0;
}


