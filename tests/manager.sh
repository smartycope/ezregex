#!/bin/bash

# This script is used to run the tests. It should be run from inside the docker container

function test_py() {
    echo "Running python tests..."
    python3 dialect_runners/py.py
    echo "Done."
}

function test_js() {
    echo "Running javascript tests..."
    node dialect_runners/js.js
    echo "Done."
}

function test_r() {
    echo "Running r tests..."
    Rscript dialect_runners/r.R
    echo "Done."
}

function test_pcre() {
    echo "Running pcre tests..."
    if [ ! -f dialect_runners/pcre ]; then
        echo "Compiling pcre..."
        gcc -o dialect_runners/pcre dialect_runners/pcre.c -lpcre -lcjson -w
    fi
    ./dialect_runners/pcre
    echo "Done."
}

# Just test the dialects
function test_dialect() {
    echo "Running dialect tests for $1..."
    # If the compiled regexs don't exist, compile them
    if [ ! -f data/compiled_regexs.jsonc ]; then
        echo "Compiling regexs..."
        python3 compile_regexs.py
        # Check that it exited successfully
        if [ $? -ne 0 ]; then
            echo "Failed to compile regexs. Likely, regexs.jsonc is invalid."
            exit 1
        fi
        echo "Done."
    fi

    if [ "$1" == "py" ]; then
        test_py
    elif [ "$1" == "js" ]; then
        test_js
    elif [ "$1" == "r" ]; then
        test_r
    elif [ "$1" == "pcre" ]; then
        test_pcre
    elif [ "$1" == "all" ]; then
        test_py
        test_js
        test_r
        test_pcre
    else
        echo "Usage: $0 dialect py | js | r | pcre | all"
        exit 1
    fi
}

# Run most of the pytests
function run_pytests() {
    echo "Running pytests..."
    python3 -m pytest -k "not test_generate and not test_invert"
    echo "Done."
}

# These 2 get seperated cause they can take a while to run, and don't
# always need to be tested
# Just test the generate module
function test_generate() {
    echo "Running generate tests..."
    python3 -m pytest ./test_generate.py
    echo "Done."
}
# Just test the invert module
function test_invert() {
    echo "Running invert tests..."
    python3 -m pytest ./test_invert.py
    echo "Done."
}

# Run all the tests
function test_all() {
    test_dialect all
    run_pytests
    test_generate
    test_invert
}

# Run enough of the tests
function test_most() {
    test_dialect all
    run_pytests
    # This one takes forever, and will not be modified often
    # test_generate
    test_invert
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
else
    echo "Usage: $0 all | most | generate | invert | dialect <dialect>"
    exit 1
fi
