import os
import imp


"""
This script allows creating a directory structure that corresponds to the
parameterized inputs present in the file test/integration/test_display_callback.py
Run this from the root of the ansible-runner directory
It will write these files to a folder named "callback-testing-playbooks"
"""


callback_tests = imp.load_source('test.integration.test_display_callback', 'test/integration/test_display_callback.py')


BASE_DIR = 'callback-testing-playbooks'
names = [test_name for test_name in dir(callback_tests) if test_name.startswith('test_')]
for name in names:

    print('')
    print(f'Processing test {name}')

    bare_name = name[len('test_callback_plugin_'):]
    if not os.path.exists(f'{BASE_DIR}/{bare_name}'):
        os.makedirs(f'{BASE_DIR}/{bare_name}')
    the_test = getattr(callback_tests, name)
    for test_marker in the_test.pytestmark:
        if test_marker.name == 'parametrize':
            inputs = test_marker.args[1]
            break
    else:
        raise Exception(f'Test {the_test} not parameterized in expected way.')

    for input in inputs:
        for k, v in input.items():
            filename = f'{BASE_DIR}/{bare_name}/{k}'
            print(f'  Writing file {filename}')
            if not os.path.exists(filename):
                with open(filename, 'w') as f:
                    f.write(v)
