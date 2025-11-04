#!/bin/bash

# This script is used to run the tests. It should be run from inside the docker container
function compile_tests() {
    if [ ! -f data/compiled_regexs.jsonc ]; then
        echo "Compiling regexs..."
        python3 compile_regexs.py
        # Check that it exited successfully
        if [ $? -ne 0 ]; then
            echo "Failed to compile regexs."
            exit 1
        else
            echo "Done."
        fi
    else
        echo "Regexs already compiled, skipping"
    fi
}

function test_py() {
    echo "Running python tests..."
    python3 dialect_runners/py.py
    if [ $? -ne 0 ]; then
        echo "Failed."
        exit 1
    fi
    echo "Done."
}

function test_js() {
    echo "Running javascript tests..."
    node dialect_runners/js.js
    if [ $? -ne 0 ]; then
        echo "Failed."
        exit 1
    fi
    echo "Done."
}

function test_r() {
    echo "Running r tests... "
    Rscript dialect_runners/r.R
    if [ $? -ne 0 ]; then
        echo "Failed."
        exit 1
    fi
    echo "Done."
}

function test_pcre() {
    echo "Running pcre2 tests..."
    gcc -o dialect_runners/pcre2 dialect_runners/pcre2.c -lpcre2-8 -lcjson -w
    if [ $? -ne 0 ]; then
        echo "Failed to compile pcre2 C script"
        exit 1
    fi
    ./dialect_runners/pcre2
    if [ $? -ne 0 ]; then
        echo "Failed."
        exit 1
    fi
    echo "Done."
}

function test_dialects_misc() {
    echo "Running misc tests..."
    pytest dialect_runners/misc.py
    if [ $? -ne 0 ]; then
        echo "Failed."
        exit 1
    fi
    echo "Done."
}

# Just test the dialects
function test_dialect() {
    echo "Running dialect tests for $1..."
    compile_tests

    if [ "$1" == "py" ]; then
        test_py
    elif [ "$1" == "js" ]; then
        test_js
    elif [ "$1" == "r" ]; then
        test_r
    elif [ "$1" == "pcre2" ]; then
        test_pcre
    elif [ "$1" == "all" ]; then
        test_py
        test_js
        test_r
        test_pcre
        test_dialects_misc
    elif [ "$1" == "misc" ]; then
        test_dialects_misc
    else
        echo "Usage: $0 dialect py | js | r | pcre2 | all | misc"
        exit 1
    fi
}

# Run most of the pytests
function run_pytests() {
    echo "Running pytests..."
    pytest -k "not generate and not invert"
    if [ $? -ne 0 ]; then
        echo "Failed."
        exit 1
    fi
    echo "Done."
}

# These 2 get seperated cause they can take a while to run, and don't
# always need to be tested
# Just test the generate module
function test_generate() {
    echo "Running generate tests..."
    python3 -m pytest ./test_generate.py
    if [ $? -ne 0 ]; then
        echo "Failed."
        exit 1
    fi
    echo "Done."
}
# Just test the invert module
function test_invert() {
    echo "Running invert tests..."
    compile_tests
    python3 invert.py "$@"
    if [ $? -ne 0 ]; then
        echo "Failed."
        exit 1
    fi
    echo "Done."
}

# Run all the tests
function test_all() {
    test_dialect all
    run_pytests
    test_generate
    test_invert
    echo "All tests pass successfully!"
}

# Run enough of the tests
function test_most() {
    test_dialect all
    run_pytests
    # This one takes forever, and will not be modified often
    # test_generate
    test_invert
    echo "All tests pass successfully!"
}

# Handle arguments
if [ "$1" == "all" ]; then
    test_all
elif [ "$1" == "most" ]; then
    test_most
elif [ "$1" == "generate" ]; then
    test_generate
elif [ "$1" == "invert" ]; then
    test_invert
elif [ "$1" == "dialect" ]; then
    test_dialect "$2"
elif [ "$1" == "pytests" ]; then
    run_pytests
else
    echo "Usage: $0 all | most | generate | invert | dialect <dialect> | pytests"
    exit 1
fi
