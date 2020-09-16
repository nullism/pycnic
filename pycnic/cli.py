#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import inspect
import os
import sys

# Local imports
from pycnic.core import WSGI


class DummyFile(object):
    """Class that will no-op writes to stdout and stderr."""
    def write(self, x): pass


class nostdout(object):
    """Capture any stdout and stderr from importing the files.

    During the import of the user-specified files, sometimes code will
    get run. This silences whatever would print during that in order to
    keep the console output of the Pycnic CLI clean.
    """

    def __enter__(self):
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        sys.stdout = DummyFile()
        sys.stderr = DummyFile()
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr


def print_description(cls, max_route_length, max_method_length):
    """Extract the docstring from the class and print it.

    Formatted to fit underneath the class name in all output formats."""
    if not cls.__doc__:
        return

    doc_string = cls.__doc__
    doc_lines = doc_string.split('\n')
    right_justify = max_route_length+2+max_method_length
    print('Description:'.rjust(right_justify) + '  ' + doc_lines[0].strip())
    for line in doc_lines[1:]:
        print(''.rjust(max_route_length+4+max_method_length) + line.strip())
    print('')


def alpha_sort(routes, verbose=False):
    """Sort routes alphabetically by their regex pattern.

    Regexes are not inherently sortable by the patterns they match,
    so this treates the pattern as a string and sorts accordingly.
    """
    routes.sort(key=lambda x: x[0])
    max_route_length = 5  # Length of the word "route"
    max_method_length = 6  # Length of the word "method"
    # Determine justified string lengths
    for route in routes:
        methods_str = ', '.join(route[1])
        max_route_length = max(max_route_length, len(route[0]))
        max_method_length = max(max_method_length, len(methods_str))

    ljust_method_word = 'Method'.ljust(max_method_length)
    ljust_route_word = 'Route'.ljust(max_route_length)
    print(ljust_route_word + '  ' + ljust_method_word + '  Class')
    print('')

    # Print justified strings
    for route in routes:
        ljust_route = route[0].ljust(max_route_length)
        methods_str = ', '.join(route[1]).upper()
        ljust_methods = methods_str.ljust(max_method_length)
        route_cls_name = full_class_name(route[2])
        print('  '.join([ljust_route, ljust_methods, route_cls_name]))
        if verbose:
            print_description(route[2], max_route_length, max_method_length)


def class_sort(routes, verbose=False):
    """Sort routes alphabetically by their class name."""
    routes.sort(key=lambda x: full_class_name(x[2]))
    max_route_length = 5  # Length of the word "route"
    max_method_length = 6  # Length of the word "method"
    # Determine justified string lengths
    for route in routes:
        methods_str = ', '.join(route[1])
        max_route_length = max(max_route_length, len(route[0]))
        max_method_length = max(max_method_length, len(methods_str))

    ljust_method_word = 'Method'.ljust(max_method_length)
    ljust_route_word = 'Route'.ljust(max_route_length)
    print(ljust_route_word + '  ' + ljust_method_word + '  Class')
    print('')

    # Print justified strings
    for route in routes:
        ljust_route = route[0].ljust(max_route_length)
        methods_str = ', '.join(route[1]).upper()
        ljust_methods = methods_str.ljust(max_method_length)
        route_cls_name = full_class_name(route[2])
        print('  '.join([ljust_route, ljust_methods, route_cls_name]))
        if verbose:
            print_description(route[2], max_route_length, max_method_length)


def no_sort(routes, verbose=False):
    """Don't process the list at all, simply format it."""
    max_route_length = 5  # Length of the word "route"
    max_method_length = 6  # Length of the word "method"
    # Determine justified string lengths
    for route in routes:
        methods_str = ', '.join(route[1])
        max_route_length = max(max_route_length, len(route[0]))
        max_method_length = max(max_method_length, len(methods_str))

    ljust_method_word = 'Method'.ljust(max_method_length)
    ljust_route_word = 'Route'.ljust(max_route_length)
    print(ljust_route_word + '  ' + ljust_method_word + '  Class')
    print('')

    # Print justified strings
    for route in routes:
        ljust_route = route[0].ljust(max_route_length)
        methods_str = ', '.join(route[1]).upper()
        ljust_methods = methods_str.ljust(max_method_length)
        route_cls_name = full_class_name(route[2])
        print('  '.join([ljust_route, ljust_methods, route_cls_name]))
        if verbose:
            print_description(route[2], max_route_length, max_method_length)


def method_sort(routes, verbose=False):
    """Group by methods, but do not sort."""
    method_routes = {
        'get': [],
        'head': [],
        'post': [],
        'put': [],
        'delete': [],
        'connect': [],
        'options': [],
        'trace': [],
        'patch': [],
    }

    # Find which routes support which methods, and place into dict accordingly
    for route, methods, route_class in routes:
        for m in methods:
            method_routes[m].append((route, route_class))

    # Start at length of word "METHOD"
    max_method_length = 6  # Length of the word "method"
    for key in method_routes:
        if len(method_routes[key]) > 0:
            max_method_length = max(max_method_length, len(key))

    max_route_length = 5  # Length of the word "route"
    for route in routes:
        max_route_length = max(max_route_length, len(route[0]))

    # Print out the information.
    ljust_method_word = 'Method'.ljust(max_method_length)
    ljust_route_word = 'Route'.ljust(max_route_length)
    print(ljust_method_word + '  ' + ljust_route_word + '  Class')
    for key in method_routes:
        if len(method_routes[key]) <= 0:
            continue
        print('')
        for a in method_routes[key]:
            ljust_route = a[0].ljust(max_route_length)
            ljust_method = key.upper().ljust(max_method_length)
            route_cls_name = full_class_name(a[1])
            print('  '.join([ljust_method, ljust_route, route_cls_name]))
            if verbose:
                print_description(a[1], max_route_length, max_method_length)


def full_class_name(cls):
    """Get the fully qualified class name of an object class.

    Reference: https://stackoverflow.com/a/2020083
    """
    module = cls.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return cls.__class__.__module__  # Avoid reporting __builtin__
    else:
        return module + '.' + cls.__class__.__name__


def find_routes():
    """Find the routes in a specified class.

    This is done by spawning an instance of the class, and inspecting the
    routes attribute of that class.
    """
    # Need to deep copy to preserve original system path
    starting_sys_path = [el for el in sys.path]

    # Parse command-line arguments
    parser = argparse.ArgumentParser(prog='pycnic routes',
                                     description='Pycnic Routes')
    parser.add_argument('-sort', required=False,
                        help='Sorting method to use, if any.',
                        choices=('alpha', 'class', 'method'))
    parser.add_argument('--verbose', '-v',
                        action='store_true',
                        help='Verbose route output. \
                        Prints route class docstring.')
    parser.add_argument('path', type=str,
                        nargs='?', default='main:app',
                        help='Path to the specified application. If none \
                        given, looks in main.py for a class called app. \
                        Example: pycnic.pycnic:app')

    # Since we've already handled the command argument, discard it.
    args = parser.parse_args(sys.argv[2:])

    # Extract class name from path
    module_path, class_name = args.path.split(':')

    # Determine module name, for dynamic import
    module_name = module_path.split('.')[-1]

    # Convert module path-type to os path-type
    file_path = os.path.join(os.getcwd(), *module_path.split('.')) + '.py'

    # Make sure that the file specified actually exists
    if not os.path.isfile(file_path):
        print('File ' + file_path + ' does not exist.')
        exit(1)

    # Add the current working directory to the path so that imports will
    # function properly in the imported file.
    sys.path.append(os.getcwd())

    with nostdout() as _:
        # Dynamically load the file in order to assess the class
        if sys.version_info[0] < 3:
            # For python 2.X, we use the imp library
            # Reference: https://stackoverflow.com/a/67692
            import imp

            loaded_src = imp.load_source(module_name, file_path)
            wsgi_class = getattr(loaded_src, class_name)
        else:
            # For python 3.X, we use importlib
            # Reference: https://stackoverflow.com/a/67692
            if sys.version_info[1] >= 5:
                # For 3.5+, use importlib.util for dynamic module loading
                from importlib.util import spec_from_file_location
                import importlib.util
                spec = spec_from_file_location(module_name, file_path)
                loaded_src = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(loaded_src)
                wsgi_class = getattr(loaded_src, class_name)
            elif sys.version_info[1] in [3, 4]:
                # For 3.3 and 3.4, SourceFileLoader is the tool to use
                from importlib.machinery import SourceFileLoader
                loaded_src = SourceFileLoader(module_name, file_path)
                wsgi_class = getattr(loaded_src, class_name)
            else:
                raise ImportError('Pycnic routes is not supported for Python \
                                  versions 3.0.X through 3.2.X')

    # Restore the system PATH to its original state
    #  now that we've loaded the input project.
    sys.path = starting_sys_path

    # Make sure that the specified element is actually a subclass of the
    # WSGI class provided in pycnic.core
    if not inspect.isclass(wsgi_class):
        print(class_name + ' is not a class in ' + file_path)
        exit(1)
    if not issubclass(wsgi_class, WSGI):
        print(class_name + ' is not a subclass of pycnic.core.WSGI.')
        exit(1)

    # Reference: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
    http_methods = [
        'get',
        'head',
        'post',
        'put',
        'delete',
        'connect',
        'options',
        'trace',
        'patch'
    ]

    # Start with empty list of routes
    # This will ultimately be a list of tuples of routes and methods
    all_routes = []

    for route_regex, route_class in wsgi_class.routes:
        # Old-style python2 classes require you to access
        #  object.__class__.__name__.
        class_name = route_class.__class__.__name__

        # Get the intersection of http_methods and class methods to find
        #  what http methods are handled by the class
        class_http_methods = [
            method for method in http_methods if method in dir(route_class)
        ]

        all_routes.append((route_regex, class_http_methods, route_class))

    if args.sort:
        if args.sort == 'method':
            method_sort(all_routes, args.verbose)
        elif args.sort == 'alpha':
            alpha_sort(all_routes, args.verbose)
        elif args.sort == 'class':
            class_sort(all_routes, args.verbose)
    else:
        no_sort(all_routes, args.verbose)


def usage():
    """Print known CLI commands.

    Emulates the style of argparse's output.
    """
    allowed_commands = [
        'routes'
    ]
    allowed_commands_list_str = '{' + ', '.join(allowed_commands) + '}'
    script_name = os.path.basename(sys.argv[0])
    print('usage: ' + script_name + ' [-h] ' + allowed_commands_list_str)
    print('')
    print('Pycnic CLI')
    print('')
    print('positional arguments:')
    print('  ' + allowed_commands_list_str + '      Subcommand to run.')
    print('')
    print('optional arguments:')
    print('  -h, --help  show this help message and exit')


def main():
    """Main function referenced by entry_points in setup.py"""
    if len(sys.argv) < 2:
        usage()
        exit()
    run_type = sys.argv[1]
    if run_type == '-h':
        usage()
    elif run_type.lower() == 'routes':
        find_routes()
    else:
        usage()


if __name__ == "__main__":
    main()
