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
python_cmd=python
python_exists=$(command -v python)
if [ "$python_exists" == "" ]; then
    python_cmd=python3
fi

# TODO: Now there is only one component test...
expected=$(cat component_tests/multiple_forms_out.txt | tr '\n' ' ') 
actual=$($python_cmd main.py < component_tests/multiple_forms_in.txt | tr '\n' ' ')
if [ ! "$expected" == "$actual" ]; then
    echo "Component test failed!"
    echo "Expected value: $expected"
    echo $actual > toto.txt
    echo "Actual value: $actual"
    exit 1
fi

echo "All tests passed!"
exit 0
 


