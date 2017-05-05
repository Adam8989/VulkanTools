#!/usr/bin/python3
#
# Copyright (c) 2013-2017 The Khronos Group Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse, cProfile, pdb, string, sys, time
from reg import *
from generator import write
from cgenerator import CGeneratorOptions, COutputGenerator
# LoaderAndValidationLayer Generator Modifications
from threading_generator import  ThreadGeneratorOptions, ThreadOutputGenerator
from parameter_validation_generator import ParamCheckerGeneratorOptions, ParamCheckerOutputGenerator
from unique_objects_generator import UniqueObjectsGeneratorOptions, UniqueObjectsOutputGenerator
from dispatch_table_helper_generator import DispatchTableHelperOutputGenerator, DispatchTableHelperOutputGeneratorOptions
from helper_file_generator import HelperFileOutputGenerator, HelperFileOutputGeneratorOptions
from loader_extension_generator import LoaderExtensionOutputGenerator, LoaderExtensionGeneratorOptions
from api_dump_generator import ApiDumpGeneratorOptions, ApiDumpOutputGenerator, COMMON_CODEGEN, TEXT_CODEGEN
from vktrace_file_generator import VkTraceFileOutputGenerator, VkTraceFileOutputGeneratorOptions

# Simple timer functions
startTime = None

def startTimer(timeit):
    global startTime
    startTime = time.clock()

def endTimer(timeit, msg):
    global startTime
    endTime = time.clock()
    if (timeit):
        write(msg, endTime - startTime, file=sys.stderr)
        startTime = None

# Turn a list of strings into a regexp string matching exactly those strings
def makeREstring(list):
    return '^(' + '|'.join(list) + ')$'

# Returns a directory of [ generator function, generator options ] indexed
# by specified short names. The generator options incorporate the following
# parameters:
#
# extensions - list of extension names to include.
# protect - True if re-inclusion protection should be added to headers
# directory - path to directory in which to generate the target(s)
def makeGenOpts(extensions = [], removeExtensions = [], protect = True, directory = '.'):
    global genOpts
    genOpts = {}

    # Descriptive names for various regexp patterns used to select
    # versions and extensions
    allVersions     = allExtensions = '.*'
    noVersions      = noExtensions = None

    addExtensions     = makeREstring(extensions)
    removeExtensions  = makeREstring(removeExtensions)

    # Copyright text prefixing all headers (list of strings).
    prefixStrings = [
        '/*',
        '** Copyright (c) 2015-2017 The Khronos Group Inc.',
        '**',
        '** Licensed under the Apache License, Version 2.0 (the "License");',
        '** you may not use this file except in compliance with the License.',
        '** You may obtain a copy of the License at',
        '**',
        '**     http://www.apache.org/licenses/LICENSE-2.0',
        '**',
        '** Unless required by applicable law or agreed to in writing, software',
        '** distributed under the License is distributed on an "AS IS" BASIS,',
        '** WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.',
        '** See the License for the specific language governing permissions and',
        '** limitations under the License.',
        '*/',
        ''
    ]

    # Text specific to Vulkan headers
    vkPrefixStrings = [
        '/*',
        '** This header is generated from the Khronos Vulkan XML API Registry.',
        '**',
        '*/',
        ''
    ]

    # Defaults for generating re-inclusion protection wrappers (or not)
    protectFile = protect
    protectFeature = protect
    protectProto = protect


        #
    # LoaderAndValidationLayer Generators
    # Options for threading layer
    genOpts['thread_check.h'] = [
          ThreadOutputGenerator,
          ThreadGeneratorOptions(
            filename          = 'thread_check.h',
            directory         = directory,
            apiname           = 'vulkan',
            profile           = None,
            versions          = allVersions,
            emitversions      = allVersions,
            defaultExtensions = 'vulkan',
            addExtensions     = addExtensions,
            removeExtensions  = removeExtensions,
            prefixText        = prefixStrings + vkPrefixStrings,
            protectFeature    = False,
            apicall           = 'VKAPI_ATTR ',
            apientry          = 'VKAPI_CALL ',
            apientryp         = 'VKAPI_PTR *',
            alignFuncParam    = 48)
        ]

    # Options for parameter validation layer
    genOpts['parameter_validation.h'] = [
          ParamCheckerOutputGenerator,
          ParamCheckerGeneratorOptions(
            filename          = 'parameter_validation.h',
            directory         = directory,
            apiname           = 'vulkan',
            profile           = None,
            versions          = allVersions,
            emitversions      = allVersions,
            defaultExtensions = 'vulkan',
            addExtensions     = addExtensions,
            removeExtensions  = removeExtensions,
            prefixText        = prefixStrings + vkPrefixStrings,
            protectFeature    = False,
            apicall           = 'VKAPI_ATTR ',
            apientry          = 'VKAPI_CALL ',
            apientryp         = 'VKAPI_PTR *',
            alignFuncParam    = 48)
        ]

    # Options for unique objects layer
    genOpts['unique_objects_wrappers.h'] = [
          UniqueObjectsOutputGenerator,
          UniqueObjectsGeneratorOptions(
            filename          = 'unique_objects_wrappers.h',
            directory         = directory,
            apiname           = 'vulkan',
            profile           = None,
            versions          = allVersions,
            emitversions      = allVersions,
            defaultExtensions = 'vulkan',
            addExtensions     = addExtensions,
            removeExtensions  = removeExtensions,
            prefixText        = prefixStrings + vkPrefixStrings,
            protectFeature    = False,
            apicall           = 'VKAPI_ATTR ',
            apientry          = 'VKAPI_CALL ',
            apientryp         = 'VKAPI_PTR *',
            alignFuncParam    = 48)
        ]

    # Options for dispatch table helper generator
    genOpts['vk_dispatch_table_helper.h'] = [
          DispatchTableHelperOutputGenerator,
          DispatchTableHelperOutputGeneratorOptions(
            filename          = 'vk_dispatch_table_helper.h',
            directory         = directory,
            apiname           = 'vulkan',
            profile           = None,
            versions          = allVersions,
            emitversions      = allVersions,
            defaultExtensions = 'vulkan',
            addExtensions     = addExtensions,
            removeExtensions  = removeExtensions,
            prefixText        = prefixStrings + vkPrefixStrings,
            protectFeature    = False,
            apicall           = 'VKAPI_ATTR ',
            apientry          = 'VKAPI_CALL ',
            apientryp         = 'VKAPI_PTR *',
            alignFuncParam    = 48)
        ]

    # Options for Layer dispatch table generator
    genOpts['vk_layer_dispatch_table.h'] = [
          LoaderExtensionOutputGenerator,
          LoaderExtensionGeneratorOptions(
            filename          = 'vk_layer_dispatch_table.h',
            directory         = directory,
            apiname           = 'vulkan',
            profile           = None,
            versions          = allVersions,
            emitversions      = allVersions,
            defaultExtensions = 'vulkan',
            addExtensions     = addExtensions,
            removeExtensions  = removeExtensions,
            prefixText        = prefixStrings + vkPrefixStrings,
            protectFeature    = False,
            apicall           = 'VKAPI_ATTR ',
            apientry          = 'VKAPI_CALL ',
            apientryp         = 'VKAPI_PTR *',
            alignFuncParam    = 48)
        ]

    # Options for loader extension source generator
    genOpts['vk_loader_extensions.h'] = [
          LoaderExtensionOutputGenerator,
          LoaderExtensionGeneratorOptions(
            filename          = 'vk_loader_extensions.h',
            directory         = directory,
            apiname           = 'vulkan',
            profile           = None,
            versions          = allVersions,
            emitversions      = allVersions,
            defaultExtensions = 'vulkan',
            addExtensions     = addExtensions,
            removeExtensions  = removeExtensions,
            prefixText        = prefixStrings + vkPrefixStrings,
            protectFeature    = False,
            apicall           = 'VKAPI_ATTR ',
            apientry          = 'VKAPI_CALL ',
            apientryp         = 'VKAPI_PTR *',
            alignFuncParam    = 48)
        ]

    # Options for loader extension source generator
    genOpts['vk_loader_extensions.c'] = [
          LoaderExtensionOutputGenerator,
          LoaderExtensionGeneratorOptions(
            filename          = 'vk_loader_extensions.c',
            directory         = directory,
            apiname           = 'vulkan',
            profile           = None,
            versions          = allVersions,
            emitversions      = allVersions,
            defaultExtensions = 'vulkan',
            addExtensions     = addExtensions,
            removeExtensions  = removeExtensions,
            prefixText        = prefixStrings + vkPrefixStrings,
            protectFeature    = False,
            apicall           = 'VKAPI_ATTR ',
            apientry          = 'VKAPI_CALL ',
            apientryp         = 'VKAPI_PTR *',
            alignFuncParam    = 48)
        ]

    # Helper file generator options for vk_enum_string_helper.h
    genOpts['vk_enum_string_helper.h'] = [
          HelperFileOutputGenerator,
          HelperFileOutputGeneratorOptions(
            filename          = 'vk_enum_string_helper.h',
            directory         = directory,
            apiname           = 'vulkan',
            profile           = None,
            versions          = allVersions,
            emitversions      = allVersions,
            defaultExtensions = 'vulkan',
            addExtensions     = addExtensions,
            removeExtensions  = removeExtensions,
            prefixText        = prefixStrings + vkPrefixStrings,
            protectFeature    = False,
            apicall           = 'VKAPI_ATTR ',
            apientry          = 'VKAPI_CALL ',
            apientryp         = 'VKAPI_PTR *',
            alignFuncParam    = 48,
            helper_file_type  = 'enum_string_header')
        ]

    # Helper file generator options for vk_struct_size_helper.h
    genOpts['vk_struct_size_helper.h'] = [
          HelperFileOutputGenerator,
          HelperFileOutputGeneratorOptions(
            filename          = 'vk_struct_size_helper.h',
            directory         = directory,
            apiname           = 'vulkan',
            profile           = None,
            versions          = allVersions,
            emitversions      = allVersions,
            defaultExtensions = 'vulkan',
            addExtensions     = addExtensions,
            removeExtensions  = removeExtensions,
            prefixText        = prefixStrings + vkPrefixStrings,
            protectFeature    = False,
            apicall           = 'VKAPI_ATTR ',
            apientry          = 'VKAPI_CALL ',
            apientryp         = 'VKAPI_PTR *',
            alignFuncParam    = 48,
            helper_file_type  = 'struct_size_header')
        ]

    # Helper file generator options for vk_struct_size_helper.c
    genOpts['vk_struct_size_helper.c'] = [
          HelperFileOutputGenerator,
          HelperFileOutputGeneratorOptions(
            filename          = 'vk_struct_size_helper.c',
            directory         = directory,
            apiname           = 'vulkan',
            profile           = None,
            versions          = allVersions,
            emitversions      = allVersions,
            defaultExtensions = 'vulkan',
            addExtensions     = addExtensions,
            removeExtensions  = removeExtensions,
            prefixText        = prefixStrings + vkPrefixStrings,
            protectFeature    = False,
            apicall           = 'VKAPI_ATTR ',
            apientry          = 'VKAPI_CALL ',
            apientryp         = 'VKAPI_PTR *',
            alignFuncParam    = 48,
            helper_file_type  = 'struct_size_source')
        ]

    # Helper file generator options for vk_safe_struct.h
    genOpts['vk_safe_struct.h'] = [
          HelperFileOutputGenerator,
          HelperFileOutputGeneratorOptions(
            filename          = 'vk_safe_struct.h',
            directory         = directory,
            apiname           = 'vulkan',
            profile           = None,
            versions          = allVersions,
            emitversions      = allVersions,
            defaultExtensions = 'vulkan',
            addExtensions     = addExtensions,
            removeExtensions  = removeExtensions,
            prefixText        = prefixStrings + vkPrefixStrings,
            protectFeature    = False,
            apicall           = 'VKAPI_ATTR ',
            apientry          = 'VKAPI_CALL ',
            apientryp         = 'VKAPI_PTR *',
            alignFuncParam    = 48,
            helper_file_type  = 'safe_struct_header')
        ]

    # Helper file generator options for vk_safe_struct.cpp
    genOpts['vk_safe_struct.cpp'] = [
          HelperFileOutputGenerator,
          HelperFileOutputGeneratorOptions(
            filename          = 'vk_safe_struct.cpp',
            directory         = directory,
            apiname           = 'vulkan',
            profile           = None,
            versions          = allVersions,
            emitversions      = allVersions,
            defaultExtensions = 'vulkan',
            addExtensions     = addExtensions,
            removeExtensions  = removeExtensions,
            prefixText        = prefixStrings + vkPrefixStrings,
            protectFeature    = False,
            apicall           = 'VKAPI_ATTR ',
            apientry          = 'VKAPI_CALL ',
            apientryp         = 'VKAPI_PTR *',
            alignFuncParam    = 48,
            helper_file_type  = 'safe_struct_source')
        ]

    # Helper file generator options for vk_object_types.h
    genOpts['vk_object_types.h'] = [
          HelperFileOutputGenerator,
          HelperFileOutputGeneratorOptions(
            filename          = 'vk_object_types.h',
            directory         = directory,
            apiname           = 'vulkan',
            profile           = None,
            versions          = allVersions,
            emitversions      = allVersions,
            defaultExtensions = 'vulkan',
            addExtensions     = addExtensions,
            removeExtensions  = removeExtensions,
            prefixText        = prefixStrings + vkPrefixStrings,
            protectFeature    = False,
            apicall           = 'VKAPI_ATTR ',
            apientry          = 'VKAPI_CALL ',
            apientryp         = 'VKAPI_PTR *',
            alignFuncParam    = 48,
            helper_file_type  = 'object_types_header')
        ]


    # API dump generator options for api_dump.cpp
    genOpts['api_dump.cpp'] = [
        ApiDumpOutputGenerator,
        ApiDumpGeneratorOptions(
            input             = COMMON_CODEGEN,
            filename          = 'api_dump.cpp',
            apiname           = 'vulkan',
            profile           = None,
            versions          = allVersions,
            emitversions      = allVersions,
            defaultExtensions = 'vulkan',
            addExtensions     = None,
            removeExtensions  = None,
            prefixText        = prefixStrings + vkPrefixStrings,
            genFuncPointers   = True,
            protectFile       = protectFile,
            protectFeature    = False,
            protectProto      = None,
            protectProtoStr   = 'VK_NO_PROTOTYPES',
            apicall           = 'VKAPI_ATTR ',
            apientry          = 'VKAPI_CALL ',
            apientryp         = 'VKAPI_PTR *',
            alignFuncParam    = 48)
        ]

    # API dump generator options for api_dump_text.h
    genOpts['api_dump_text.h'] = [
        ApiDumpOutputGenerator,
        ApiDumpGeneratorOptions(
            input             = TEXT_CODEGEN,
            filename          = 'api_dump_text.h',
            apiname           = 'vulkan',
            profile           = None,
            versions          = allVersions,
            emitversions      = allVersions,
            defaultExtensions = 'vulkan',
            addExtensions     = None,
            removeExtensions  = None,
            prefixText        = prefixStrings + vkPrefixStrings,
            genFuncPointers   = True,
            protectFile       = protectFile,
            protectFeature    = False,
            protectProto      = None,
            protectProtoStr   = 'VK_NO_PROTOTYPES',
            apicall           = 'VKAPI_ATTR ',
            apientry          = 'VKAPI_CALL ',
            apientryp         = 'VKAPI_PTR *',
            alignFuncParam    = 48)
    ]

    # VkTrace file generator options for vkreplay_vk_objmapper.h
    genOpts['vkreplay_vk_objmapper.h'] = [
          VkTraceFileOutputGenerator,
          VkTraceFileOutputGeneratorOptions(
            filename          = 'vkreplay_vk_objmapper.h',
            directory         = directory,
            apiname           = 'vulkan',
            profile           = None,
            versions          = allVersions,
            emitversions      = allVersions,
            defaultExtensions = 'vulkan',
            addExtensions     = addExtensions,
            removeExtensions  = removeExtensions,
            prefixText        = prefixStrings + vkPrefixStrings,
            protectFeature    = False,
            apicall           = 'VKAPI_ATTR ',
            apientry          = 'VKAPI_CALL ',
            apientryp         = 'VKAPI_PTR *',
            alignFuncParam    = 48,
            vktrace_file_type  = 'vkreplay_objmapper_header')
        ]

    # VkTrace file generator options for vkreplay_vk_func_ptrs.h
    genOpts['vkreplay_vk_func_ptrs.h'] = [
          VkTraceFileOutputGenerator,
          VkTraceFileOutputGeneratorOptions(
            filename          = 'vkreplay_vk_func_ptrs.h',
            directory         = directory,
            apiname           = 'vulkan',
            profile           = None,
            versions          = allVersions,
            emitversions      = allVersions,
            defaultExtensions = 'vulkan',
            addExtensions     = addExtensions,
            removeExtensions  = removeExtensions,
            prefixText        = prefixStrings + vkPrefixStrings,
            protectFeature    = False,
            apicall           = 'VKAPI_ATTR ',
            apientry          = 'VKAPI_CALL ',
            apientryp         = 'VKAPI_PTR *',
            alignFuncParam    = 48,
            vktrace_file_type  = 'vkreplay_funcptr_header')
        ]

    # VkTrace file generator options for vkreplay_vk_replay_gen.cpp
    genOpts['vkreplay_vk_replay_gen.cpp'] = [
          VkTraceFileOutputGenerator,
          VkTraceFileOutputGeneratorOptions(
            filename          = 'vkreplay_vk_replay_gen.cpp',
            directory         = directory,
            apiname           = 'vulkan',
            profile           = None,
            versions          = allVersions,
            emitversions      = allVersions,
            defaultExtensions = 'vulkan',
            addExtensions     = addExtensions,
            removeExtensions  = removeExtensions,
            prefixText        = prefixStrings + vkPrefixStrings,
            protectFeature    = False,
            apicall           = 'VKAPI_ATTR ',
            apientry          = 'VKAPI_CALL ',
            apientryp         = 'VKAPI_PTR *',
            alignFuncParam    = 48,
            vktrace_file_type  = 'vkreplay_replay_gen_source')
        ]

    # VkTrace file generator options for vktrace_vk_packet_id.h
    genOpts['vktrace_vk_packet_id.h'] = [
          VkTraceFileOutputGenerator,
          VkTraceFileOutputGeneratorOptions(
            filename          = 'vktrace_vk_packet_id.h',
            directory         = directory,
            apiname           = 'vulkan',
            profile           = None,
            versions          = allVersions,
            emitversions      = allVersions,
            defaultExtensions = 'vulkan',
            addExtensions     = addExtensions,
            removeExtensions  = removeExtensions,
            prefixText        = prefixStrings + vkPrefixStrings,
            protectFeature    = False,
            apicall           = 'VKAPI_ATTR ',
            apientry          = 'VKAPI_CALL ',
            apientryp         = 'VKAPI_PTR *',
            alignFuncParam    = 48,
            vktrace_file_type  = 'vktrace_packet_id_header')
        ]

    # VkTrace file generator options for vktrace_vk_vk.h
    genOpts['vktrace_vk_vk.h'] = [
          VkTraceFileOutputGenerator,
          VkTraceFileOutputGeneratorOptions(
            filename          = 'vktrace_vk_vk.h',
            directory         = directory,
            apiname           = 'vulkan',
            profile           = None,
            versions          = allVersions,
            emitversions      = allVersions,
            defaultExtensions = 'vulkan',
            addExtensions     = addExtensions,
            removeExtensions  = removeExtensions,
            prefixText        = prefixStrings + vkPrefixStrings,
            protectFeature    = False,
            apicall           = 'VKAPI_ATTR ',
            apientry          = 'VKAPI_CALL ',
            apientryp         = 'VKAPI_PTR *',
            alignFuncParam    = 48,
            vktrace_file_type  = 'vktrace_vk_header')
        ]

    # VkTrace file generator options for vktrace_vk_vk_packets.h
    genOpts['vktrace_vk_vk_packets.h'] = [
          VkTraceFileOutputGenerator,
          VkTraceFileOutputGeneratorOptions(
            filename          = 'vktrace_vk_vk_packets.h',
            directory         = directory,
            apiname           = 'vulkan',
            profile           = None,
            versions          = allVersions,
            emitversions      = allVersions,
            defaultExtensions = 'vulkan',
            addExtensions     = addExtensions,
            removeExtensions  = removeExtensions,
            prefixText        = prefixStrings + vkPrefixStrings,
            protectFeature    = False,
            apicall           = 'VKAPI_ATTR ',
            apientry          = 'VKAPI_CALL ',
            apientryp         = 'VKAPI_PTR *',
            alignFuncParam    = 48,
            vktrace_file_type  = 'vktrace_vk_packets_header')
        ]

# Generate a target based on the options in the matching genOpts{} object.
# This is encapsulated in a function so it can be profiled and/or timed.
# The args parameter is an parsed argument object containing the following
# fields that are used:
#   target - target to generate
#   directory - directory to generate it in
#   protect - True if re-inclusion wrappers should be created
#   extensions - list of additional extensions to include in generated
#   interfaces
def genTarget(args):
    global genOpts

    # Create generator options with specified parameters
    makeGenOpts(extensions = args.extension,
                removeExtensions = args.removeExtension,
                protect = args.protect,
                directory = args.directory)

    if (args.target in genOpts.keys()):
        createGenerator = genOpts[args.target][0]
        options = genOpts[args.target][1]

        if not args.quiet:
            write('* Building', options.filename, file=sys.stderr)

        startTimer(args.time)
        gen = createGenerator(errFile=errWarn,
                              warnFile=errWarn,
                              diagFile=diag)
        reg.setGenerator(gen)
        reg.apiGen(options)

        if not args.quiet:
            write('* Generated', options.filename, file=sys.stderr)
        endTimer(args.time, '* Time to generate ' + options.filename + ' =')
    else:
        write('No generator options for unknown target:',
              args.target, file=sys.stderr)

# -extension name - may be a single extension name, a a space-separated list
# of names, or a regular expression.
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-extension', action='append',
                        default=[],
                        help='Specify an extension or extensions to add to targets')
    parser.add_argument('-removeExtension', action='append',
                        default=[],
                        help='Specify an extension or extensions to remove from targets')
    parser.add_argument('-debug', action='store_true',
                        help='Enable debugging')
    parser.add_argument('-dump', action='store_true',
                        help='Enable dump to stderr')
    parser.add_argument('-diagfile', action='store',
                        default=None,
                        help='Write diagnostics to specified file')
    parser.add_argument('-errfile', action='store',
                        default=None,
                        help='Write errors and warnings to specified file instead of stderr')
    parser.add_argument('-noprotect', dest='protect', action='store_false',
                        help='Disable inclusion protection in output headers')
    parser.add_argument('-profile', action='store_true',
                        help='Enable profiling')
    parser.add_argument('-registry', action='store',
                        default='vk.xml',
                        help='Use specified registry file instead of vk.xml')
    parser.add_argument('-time', action='store_true',
                        help='Enable timing')
    parser.add_argument('-validate', action='store_true',
                        help='Enable group validation')
    parser.add_argument('-o', action='store', dest='directory',
                        default='.',
                        help='Create target and related files in specified directory')
    parser.add_argument('target', metavar='target', nargs='?',
                        help='Specify target')
    parser.add_argument('-quiet', action='store_true', default=False,
                        help='Suppress script output during normal execution.')

    args = parser.parse_args()

    # This splits arguments which are space-separated lists
    args.extension = [name for arg in args.extension for name in arg.split()]

    # Load & parse registry
    reg = Registry()

    startTimer(args.time)
    tree = etree.parse(args.registry)
    endTimer(args.time, '* Time to make ElementTree =')

    startTimer(args.time)
    reg.loadElementTree(tree)
    endTimer(args.time, '* Time to parse ElementTree =')

    if (args.validate):
        reg.validateGroups()

    if (args.dump):
        write('* Dumping registry to regdump.txt', file=sys.stderr)
        reg.dumpReg(filehandle = open('regdump.txt', 'w', encoding='utf-8'))

    # create error/warning & diagnostic files
    if (args.errfile):
        errWarn = open(args.errfile, 'w', encoding='utf-8')
    else:
        errWarn = sys.stderr

    if (args.diagfile):
        diag = open(args.diagfile, 'w', encoding='utf-8')
    else:
        diag = None

    if (args.debug):
        pdb.run('genTarget(args)')
    elif (args.profile):
        import cProfile, pstats
        cProfile.run('genTarget(args)', 'profile.txt')
        p = pstats.Stats('profile.txt')
        p.strip_dirs().sort_stats('time').print_stats(50)
    else:
        genTarget(args)
