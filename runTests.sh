#!/bin/bash

# Run unit tests
echo "Running unit tests..."
pytest
if [ $? -ne 0 ]; then
    echo "Unit tests failed!"
    exit 1
fi

# Run component tests
echo "Running component test..."
# TODO: Now there is only one component test...
#cd component_tests
expected=$(cat component_tests/multiple_forms_out.txt | tr '\n' ' ') 
actual=$(python interactive.py < component_tests/multiple_forms_in.txt | tr '\n' ' ')
if [ ! "$expected" == "$actual" ]; then
    echo "Component test failed!"
    echo "Expected value: $expected"
    echo $actual > toto.txt
    echo "Actual value: $actual"
    exit 1
fi

echo "All tests passed!"
exit 0
 


