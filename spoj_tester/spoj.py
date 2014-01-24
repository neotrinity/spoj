import sys
import os
from subprocess import CalledProcessError, check_output


def display_help():
    print "Usage: %s [folder_name]" % sys.argv[0]
    print ""
    print "If folder_name is not provided then the current working directory is assumed"
    print ""
    print "-" * 80
    print "In the folder the following files are expected :"
    print "1. one *.py file"
    print "2. one in.txt file"
    print "3. one exp_out.txt file [ Expected output file ]"
    print "-" * 80

if len(sys.argv[1:]) > 1:
    display_help()

folder = sys.argv[1] if len(sys.argv) == 2 else '.'

def match(actual_output, expected_output):
    actual_lines = actual_output.split('\n')
    expected_lines = expected_output.split('\n')
    if len(actual_lines) != len(expected_lines):
        return False

    matched = True
    for i, line in enumerate(expected_lines):
        try:
            if line.rstrip('\r') != actual_lines[i].rstrip('\r'):
                matched = False
                break
        except IndexError as e:
            matched = False
            break
    return matched


try:
    files = os.listdir(folder)
    py_file = [x for x in files if x.endswith(r'.py')]
    if ('in.txt' in files and
        'exp_out.txt' in files and
        len(py_file) == 1):
        try:
            li = ['python', os.path.join(folder, py_file[0])]
            in_f = open(os.path.join(folder, 'in.txt'))
            output = check_output(li, stdin=in_f)
            expected_output = open(os.path.join(folder, 'exp_out.txt')).read()
            if not match(output, expected_output):
                print "Error in Code:"
                print '-' * 80
                print ''
                print 'Expected Output:'
                print expected_output
                print '-' * 80
                print ''
                print 'Actual Output:'
                print output
                print '-' * 80
                print ''
            else:
                print '-+-' * 35
                print 'Matched !!!!!!!!!'
                print '-+-' * 35
        except CalledProcessError as e:
            print str(e)
            display_help()
            sys.exit(-1)
    else:
        print "Files not present as expected..."
        display_help()
        sys.exit(-1)


except Exception as e:
    print str(e)
    display_help()
    sys.exit(-1)
