#!/usr/bin/env python3
"""
    Copyright (C) 2018-2019 Rene Rivera.
    Use, modification and distribution are subject to the
    Boost Software License, Version 1.0. (See accompanying file
    LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""
import argparse
import json
import multiprocessing
import os
import os.path
import pprint
import random
import re
import shutil
from subprocess import check_call, call, check_output
from time import sleep
from timeit import default_timer


def roundi(f):
    return int(round(f))


class Commands():
    def __init__(self):
        self.args = argparse.Namespace()
        self.args.trace = False
        self.args.debug = False

    def __check_call__(self, command):
        if self.args.trace:
            print('EXEC: "' + '" "'.join(command) + '"')
        if not self.args.debug:
            return check_call(command)
        else:
            return None

    def __call__(self, command):
        if self.args.trace:
            print('EXEC: "' + '" "'.join(command) + '"')
        if not self.args.debug:
            return call(command)
        else:
            return None

    def __check_output__(self, command):
        if self.args.trace:
            print('EXEC: "' + '" "'.join(command) + '"')
        if not self.args.debug:
            return check_output(command).decode('utf8')
        else:
            return ""

    def __re_search__(self, p, s, default=None):
        s = re.search(p, s)
        return s.group(1) if s else default

    def __load_data__(self, json_file):
        with open(json_file, "r") as f:
            return json.load(f)

    def __save_data__(self, json_file, data):
        json_out = json.dumps(
            data, sort_keys=True, indent=2, separators=(',', ': '))
        if not self.args.debug:
            with open(json_file, "w") as f:
                f.write(json_out)
        return json_out


class Main(Commands):
    def __init__(self):
        parser = argparse.ArgumentParser()
        # common args
        parser.add_argument('--debug', action='store_true')
        parser.add_argument('--trace', action='store_true')
        # subclass args
        self.__init_parser__(parser)
        # get the args
        self.args = parser.parse_args()
        # run the script
        self.__run__()

    def __init_parser__(self, parser):
        pass

    def __run__(self):
        pass


class PushDir():
    def __init__(self, *dirs):
        self.dir = os.path.abspath(os.path.join(*dirs))

    def __enter__(self):
        self.cwd = os.getcwd()
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        os.chdir(self.dir)
        return self.dir

    def __exit__(self, type, value, traceback):
        os.chdir(self.cwd)


class Test(Main):
    def __init_parser__(self, parser):
        parser.add_argument(
            '--test', default='build',
            help='The test to run. Can be one of: build.')
        parser.add_argument(
            '--kind', default='headers,modules',
            help='The type of tests to run. Can be a command separated list of any of: headers, modules.')
        parser.add_argument(
            '--dir', required=True,
            help='The directory root to generate the test files.')
        parser.add_argument(
            '--count', default=150, type=int,
            help='Number of TUs to generate and process.')
        parser.add_argument(
            '--complexity', default=0.3, type=float,
            help='Complexity of generated code in each TU from 0 to 1, where 1 is most complex.')
        parser.add_argument(
            '--dag-depth', default='2,3',
            help='The range of DAG depths to test as two comma separated values.')
        parser.add_argument(
            '--dep-factor', default=1.0, type=float,
            help='Ratio of dependencies from the TUs in one DAG depth to the previous TUs.')
        parser.add_argument(
            '--dep-max', default=3, type=int,
            help='Maximum number of generated dependencies in source files.')
        parser.add_argument(
            '--jobs', default=2, type=int,
            help='Maximum number of parallel jobs to use.')
        parser.add_argument(
            '--use-std', default=False, action='store_true',
            help='Generate references to standard library in the source.')
        parser.add_argument(
            '--def-templates', default=False, action='store_true',
            help='Generate test template definitions in the source.')
        parser.add_argument(
            '--def-ints', default=False, action='store_true',
            help='Generate integer variable declarations in the source.')
        parser.add_argument(
            '--json-out', required=True,
            help='Output resulting test data table as JSON to a file.')
        parser.add_argument(
            '--dag-samples', default=20, type=int,
            help='Number of samples to test in the dag range.')

    def __run__(self):
        self.dir = os.getcwd()
        args_dag_depth = self.args.dag_depth.split(',')
        args_dag_depth = [int(i) for i in args_dag_depth]
        if len(args_dag_depth) == 1:
            args_dag_depth.append(args_dag_depth[0]+1)
        args_kind = self.args.kind
        data = []
        dag_depth_range = range(
            args_dag_depth[0], args_dag_depth[1],
            max([1, int((args_dag_depth[1]-args_dag_depth[0])/self.args.dag_samples)]))
        test_x = getattr(self, '__test_%s__' % (self.args.test), False)
        for dag_depth in dag_depth_range:
            self.args.dag_depth = dag_depth
            self.args.kind = args_kind
            sample = test_x()
            data.append(sample)
            pprint.pprint(sample)
        pprint.pprint(data)
        json_data = [["dag_depth", "headers", "modules"]]
        for d in data:
            data_row = [d['dag_depth']]
            if 'headers' in d:
                data_row.append(d['headers'])
            if 'modules' in d:
                data_row.append(d['modules'])
            json_data.append(data_row)
        if self.args.json_out:
            self.__save_data__(self.args.json_out, json_data)

    def __test_build__(self):
        args_dir = self.args.dir
        result = {
            'dag_depth': self.args.dag_depth,
        }
        if hasattr(self.args, 'kind'):
            for kind in self.args.kind.split(','):
                result['dag_jobs_'+kind] = 0.0
                self.args.kind = kind
                print("KIND: %s" % (kind))
                gen_x = getattr(self, '__generate_%s__' % (kind), False)
                run_x = getattr(self, '__run_%s__' % (kind), False)
                self.args.dir = os.path.join(args_dir, kind)
                if gen_x:
                    x = gen_x()
                    if run_x:
                        t0 = default_timer()
                        result['dag_jobs_'+kind] = run_x(x)
                        t1 = default_timer()
                        print(t1-t0)
                        result[kind] = t1-t0
        return result

    __std_includes__ = [
        '#include <regex>',
        '#include <iostream>',
    ]

    __std_imports__ = [
        'import std.core;',
        'import std.io;',
    ]

    @property
    def std_includes(self):
        if self.args.use_std:
            if self.args.kind == 'headers':
                l = roundi(float(self.args.complexity)
                           * len(self.__std_includes__))
                return self.__std_includes__[0:l]
            elif self.args.kind == 'modules':
                l = roundi(float(self.args.complexity)
                           * len(self.__std_imports__))
                return self.__std_imports__[0:l]
        else:
            return []

    @property
    def cpp_code(self):
        result = []
        export = 'export' if self.args.kind == 'modules' else ''
        if self.args.def_ints:
            for i in range(roundi(float(self.args.complexity)*1000)):
                result.append(
                    '''{export} int i{id} = {id};'''.format(
                        id=i+1, export=export))
        if self.args.def_templates:
            result.append(
                '''{export} template <typename T> struct s0 {{ enum t {{ a }}; }};'''.format(
                    export=export))
            for i in range(roundi(float(self.args.complexity)*1000)):
                result.append(
                    '''{export} template <typename T> struct s{id} {{ typedef typename s{id_base}<T>::t t; }};'''.format(
                        id=i+1, id_base=i, export=export))
        return result

    @property
    def cxx(self):
        result = os.getenv('CXX')
        if not result and os.path.isfile('/Developer/Tools/gcc-modules/bin/g++-mxx'):
            result = '/Developer/Tools/gcc-modules/bin/g++-mxx'
        if not result and os.path.isfile(os.path.join(os.getenv('HOME'), 'gcc-modules', 'bin', 'g++-mxx')):
            result = os.path.isfile(os.path.join(
                os.getenv('HOME'), 'gcc-modules', 'bin', 'g++-mxx'))
        if not result:
            result = 'g++-mxx'
        return result

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ MODULES...

    def __generate_modules__(self):
        with PushDir(self.args.dir) as dir:
            shutil.rmtree(dir)
        dag_levels = self.__generate_dag__()
        modules_levels = []
        if self.args.use_std:
            std_modules_dir = os.path.join(
                self.dir, '..', 'std-modules', 'libstd-modules')
            with PushDir(self.args.dir) as dir:
                os.symlink(
                    os.path.join(std_modules_dir, 'std-core.mxx'),
                    os.path.join(dir, 'std.core.cpp'))
                os.symlink(
                    os.path.join(std_modules_dir, 'std-io.mxx'),
                    os.path.join(dir, 'std.io.cpp'))
                os.symlink(
                    os.path.join(std_modules_dir, 'std-regex.mxx'),
                    os.path.join(dir, 'std.regex.cpp'))
                os.symlink(
                    os.path.join(std_modules_dir, 'std-threading.mxx'),
                    os.path.join(dir, 'std.threading.cpp'))
                modules_levels.append([
                    os.path.join(dir, 'std.core.cpp'),
                ])
                modules_levels.append([
                    os.path.join(dir, 'std.io.cpp'),
                ])
        with PushDir(self.args.dir) as dir:
            dag_deps = {}
            for dag_level in dag_levels:
                modules_level = []
                for m in dag_level:
                    dag_deps[m['index']] = m['deps']
                    modules_level.append(os.path.join(
                        dir, 'm%s' % (m['index']) + '.cpp'))
                modules_levels.append(modules_level)
            for n in range(int(self.args.count)):
                module_id = 'm%s' % (n)
                module_mxx = os.path.join(dir, module_id + '.cpp')
                module_deps = ['m%s' % (n) for n in dag_deps[n]]
                module_source = self.__make_module_source__(
                    module_id, module_deps)
                if self.args.debug:
                    print('FILE: %s' % (module_mxx))
                    print(module_source)
                    print('-----')
                else:
                    with open(module_mxx, 'w') as f:
                        f.write(module_source)
        return modules_levels

    def __run_modules__(self, levels):
        if self.args.trace:
            print('MODULES_LEVELS:')
            pprint.pprint(levels)
        jobs = 0
        for level in levels:
            jobs += len(level)
            pool = multiprocessing.Pool(processes=int(self.args.jobs))
            pool.map(__pool_function__,
                     [[self, '__compile_module__', m] for m in level])
            pool.close()
            pool.join()
        return float(jobs)/float(len(levels))

    # CXX -fmodules-ts m0.cpp -c -O0
    def __compile_module__(self, m):
        with PushDir(os.path.dirname(m)):
            cc = [
                self.cxx,
                '-fmodules-ts', '-c', '-O0',
                os.path.basename(m)]
            if self.args.use_std:
                cc.extend(['-I', os.path.join(self.dir, '..', 'std-modules')])
            if self.args.debug:
                sleep(random.uniform(0.0, 0.1))
                print('C++: "%s"' % ('" "'.join(cc)))
            else:
                t0 = default_timer()
                self.__check_call__(cc)
                t1 = default_timer()
                if self.args.trace:
                    print('C++: "%s" => %s' % ('" "'.join(cc), t1-t0))

    __module_template__ = '''\
export module {id};
{std_includes}
{imports}
namespace {id}_ns
{{
{exports}
}}
'''

    __module_import_template__ = '''\
import {id};
'''

    def __make_module_source__(self, id, imports):
        module_size = len(self.__module_template__)
        module_imports = []
        for i in imports:
            module_size += Test.__append__(
                module_imports,
                self.__module_import_template__.format(id=i))
        module_exports = []
        module_size += Test.__append__(
            module_exports, '''export int n = 0;''')
        for c in self.cpp_code:
            module_size += Test.__append__(module_exports, c)
        module_source = self.__module_template__.format(
            id=id,
            std_includes='\n'.join(self.std_includes),
            imports=''.join(module_imports),
            exports='\n'.join(module_exports))
        return module_source

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ HEADERS...

    def __generate_headers__(self):
        with PushDir(self.args.dir) as dir:
            shutil.rmtree(dir)
        dag_levels = self.__generate_dag__()
        levels = []
        id_t = 'h%s'
        with PushDir(self.args.dir) as dir:
            dag_deps = {}
            level = []
            for dag_level in dag_levels:
                for m in dag_level:
                    dag_deps[m['index']] = m['deps']
                    level.append(os.path.join(
                        dir, id_t % (m['index']) + '.cpp'))
            levels.append(level)
            for n in range(int(self.args.count)):
                id = id_t % (n)
                hpp = os.path.join(dir, id + '.hpp')
                cpp = os.path.join(dir, id + '.cpp')
                deps = [id_t % (n) for n in dag_deps[n]]
                source = self.__make_headers_source__(id, deps)
                if self.args.debug:
                    print('FILE: %s' % (hpp))
                    print(source[0])
                    print('-----')
                    print('FILE: %s' % (cpp))
                    print(source[1])
                    print('-----')
                else:
                    with open(hpp, 'w') as f:
                        f.write(source[0])
                    with open(cpp, 'w') as f:
                        f.write(source[1])
        return levels

    def __run_headers__(self, levels):
        if self.args.trace:
            print('LEVELS:')
            pprint.pprint(levels)
        jobs = 0
        for level in levels:
            jobs += len(level)
            pool = multiprocessing.Pool(processes=int(self.args.jobs))
            pool.map(__pool_function__,
                     [[self, '__compile_headers__', m] for m in level])
            pool.close()
            pool.join()
        return float(jobs)/float(len(levels))

    # CXX m0.cpp -c -O0
    def __compile_headers__(self, m):
        with PushDir(os.path.dirname(m)):
            cc = [
                self.cxx,
                '-c', '-O0',
                os.path.basename(m)
            ]
            if self.args.debug:
                sleep(random.uniform(0.0, 0.1))
                print('C++: "%s"' % ('" "'.join(cc)))
            else:
                t0 = default_timer()
                self.__check_call__(cc)
                t1 = default_timer()
                if self.args.trace:
                    print('C++: "%s" => %s' % ('" "'.join(cc), t1-t0))

    __headers_template__ = '''\
#ifndef H_GUARD_{id}
#define H_GUARD_{id}
{includes}
{std_includes}
namespace {id}_ns
{{
{exports}
}}
#endif
'''

    __headers_cpp_template__ = '''\
#include "{id}.hpp"
'''

    __headers_include_template__ = '''\
#include "{id}.hpp"
'''

    def __make_headers_source__(self, id, imports):
        size = len(self.__headers_template__)
        includes = []
        for i in imports:
            size += Test.__append__(
                includes,
                self.__headers_include_template__.format(id=i))
        exports = []
        size += Test.__append__(
            exports, '''int n = 0;''')
        for c in self.cpp_code:
            size += Test.__append__(exports, c)
        source = self.__headers_template__.format(
            id=id,
            std_includes='\n'.join(self.std_includes),
            includes=''.join(includes),
            exports='\n'.join(exports))
        source_cpp = self.__headers_cpp_template__.format(
            id=id)
        return [source, source_cpp]

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DAG...

    def __generate_dag__(self):
        dag_levels = []
        dag_step = float(self.args.count)/float(self.args.dag_depth)
        # All the deps from the first dag level down to the n-2
        dag_deps_top = []
        # The deps from dag level n-1
        dag_deps_prev = []
        i = 0
        r = 0.0
        while i < int(self.args.count):
            j = min(int(i+dag_step+r), int(self.args.count))
            r = i+dag_step+r-j
            if j+int((dag_step+r)/2) > int(self.args.count):
                j = int(self.args.count)
            if self.args.trace:
                print('GENERATE_DAG: range = [%s, %s), residue = %s, step = %s' % (
                    i, j, r, dag_step))
            dag_dep_count = min(
                roundi(self.args.dep_factor*j), int(self.args.dep_max))
            dag_level = []
            for m in range(i, j):
                dep_count = min(dag_dep_count, len(
                    dag_deps_prev)+len(dag_deps_top))
                dep_count = 0 if i == 0 else max(1, dep_count)
                dag_deps = []
                dag_deps.extend(self.__choices__(dag_deps_prev, 1))
                if dep_count > 1:
                    dag_deps.extend(self.__choices__(
                        dag_deps_top, dep_count-1))
                if self.args.trace:
                    print('GENERATE_DAG: dag = %s, deps = %s' %(m, dag_deps))
                dag_level.append({
                    'index': m,
                    'deps': dag_deps
                })
            dag_levels.append(dag_level)
            dag_deps_top = list(range(0, i))
            dag_deps_prev = list(range(i, j))
            i = j
        if self.args.trace:
            print('DAG_LEVELS:')
            pprint.pprint(dag_levels)
        return dag_levels

    def __choices__(self, sequence, count):
        # return random.choices(sequence, k=count)
        result = set()
        if len(sequence) > 0:
            count = min(count, len(sequence))
            while len(result) < count:
                result.add(random.choice(sequence))
        return result

    @staticmethod
    def __append__(container, item):
        container.append(item)
        return len(item)+1


def __pool_function__(x):
    f = getattr(x[0], x[1])
    return f(*x[2:])


# P1441R0 modules_perf
# ./parallel_perf.py --dir=/Users/grafik/devcache/cpp_stats --kind=headers,modules --jobs=8 --dep-max=3 --count=300 --complexity=0.3 --def-ints --dag-depth=3,300

if __name__ == "__main__":
    Test()
