#!/usr/bin/env python3

import logging
import os
import re
import subprocess
import sys

topdir = os.path.abspath(sys.argv[1])

ALL_REMOTES = {
    'ufs-weather-model' : {
        '.' : {
            'noaa-gsl'  : 'https://github.com/NOAA-GSL/ufs-weather-model',
            'ufs-community' : 'https://github.com/ufs-community/ufs-weather-model',
            'ncar'      : 'https://github.com/NCAR/ufs-weather-model',
            'dom'       : 'https://github.com/climbfuji/ufs-weather-model',
            'mike'      : 'https://github.com/mdtoy/ufs-weather-model',
            'dustin'    : 'https://github.com/dustinswales/ufs-weather-model',
            'jun'       : 'https://github.com/junwang-noaa/ufs-weather-model',
            'shan'      : 'https://github.com/shansun6/ufs-weather-model',
            'valery'    : 'https://github.com/valeryyudin-noaa/ufs-weather-model',
            'helin'     : 'https://github.com/helinwei-noaa/ufs-weather-model',
            'brian'     : 'https://github.com/briancurtis-noaa/ufs-weather-model',
            'dusan'     : 'https://github.com/dusanjovic-noaa/ufs-weather-model',
            'jiande'    : 'https://github.com/jiandewang/ufs-weather-model',
            },
        'FV3' : {
            'noaa-gsl'  : 'https://github.com/NOAA-GSL/fv3atm',
            'noaa-emc'  : 'https://github.com/NOAA-EMC/fv3atm',
            'ncar'      : 'https://github.com/NCAR/fv3atm',
            'dom'       : 'https://github.com/climbfuji/fv3atm',
            'xia'       : 'https://github.com/XiaSun-NOAA/fv3atm',
            'man'       : 'https://github.com/mzhangw/fv3atm',
            'grant'     : 'https://github.com/grantfirl/fv3atm',
            'mike'      : 'https://github.com/mdtoy/fv3atm',
            'dustin'    : 'https://github.com/dustinswales/fv3atm',
            'jun'       : 'https://github.com/junwang-noaa/fv3atm',
            'shan'      : 'https://github.com/shansun6/fv3atm',
            'tanya'     : 'https://github.com/tanyasmirnova/fv3atm',
            'valery'    : 'https://github.com/valeryyudin-noaa/fv3atm',
            'helin'     : 'https://github.com/helinwei-noaa/fv3atm',
            },
        'FV3/ccpp/framework' : {
            'noaa-gsl'  : 'https://github.com/NOAA-GSL/ccpp-framework',
            'ncar'      : 'https://github.com/NCAR/ccpp-framework',
            'dom'       : 'https://github.com/climbfuji/ccpp-framework',
            'grant'     : 'https://github.com/grantfirl/ccpp-framework',
            'phil'      : 'https://github.com/pjpegion/ccpp-framework',
            },
        'FV3/ccpp/physics' : {
            'noaa-gsl'  : 'https://github.com/NOAA-GSL/ccpp-physics',
            'ncar'      : 'https://github.com/NCAR/ccpp-physics',
            'dom'       : 'https://github.com/climbfuji/ccpp-physics',
            'xia'       : 'https://github.com/XiaSun-NOAA/ccpp-physics',
            'man'       : 'https://github.com/mzhangw/ccpp-physics',
            'grant'     : 'https://github.com/grantfirl/ccpp-physics',
            'mike'      : 'https://github.com/mdtoy/ccpp-physics',
            'dustin'    : 'https://github.com/dustinswales/ccpp-physics',
            'shan'      : 'https://github.com/shansun6/ccpp-physics',
            'joe'       : 'https://github.com/joeolson42/ccpp-physics',
            'tanya'     : 'https://github.com/tanyasmirnova/ccpp-physics',
            'valery'    : 'https://github.com/valeryyudin-noaa/ccpp-physics',
            'helin'     : 'https://github.com/helinwei-noaa/ccpp-physics',
            'ufs-community' : 'https://github.com/ufs-community/ccpp-physics',
            },
        'FV3/ccpp/physics/physics/rte-rrtmgp' : {
            'esr'       : 'https://github.com/earth-system-radiation/rte-rrtmgp',
            'dom'       : 'https://github.com/climbfuji/rte-rrtmgp',
            },
        'FV3/atmos_cubed_sphere' : {
            'noaa-emc'  : 'https://github.com/NOAA-EMC/GFDL_atmos_cubed_sphere',
            'noaa-gfdl' : 'https://github.com/NOAA-GFDL/GFDL_atmos_cubed_sphere',
            'noaa-gsl'  : 'https://github.com/NOAA-GSL/GFDL_atmos_cubed_sphere',
            'ncar'      : 'https://github.com/NCAR/GFDL_atmos_cubed_sphere',
            'dom'       : 'https://github.com/climbfuji/GFDL_atmos_cubed_sphere',
            'jun'       : 'https://github.com/junwang-noaa/GFDL_atmos_cubed_sphere',
            },
        'stochastic_physics' : {
            'noaa-psl'  : 'https://github.com/NOAA-PSD/stochastic_physics',
            'noaa-gsl'  : 'https://github.com/NOAA-GSL/stochastic_physics',
            'dom'       : 'https://github.com/climbfuji/stochastic_physics',
            'tanya'     : 'https://github.com/tanyasmirnova/stochastic_physics',
            },
        },
    'spack-stack' : {
        '.' : {
            'jcsda'     : 'https://github.com/jcsda/spack-stack',
            'dom'       : 'https://github.com/climbfuji/spack-stack',
            'alex'      : 'https://github.com/alexanderrichert-noaa/spack-stack',
            'cam'       : 'https://github.com/ulmononian/spack-stack',
            },
        'spack' : {
            'jcsda'     : 'https://github.com/jcsda/spack',
            'dom'       : 'https://github.com/climbfuji/spack',
            'alex'      : 'https://github.com/alexanderrichert-noaa/spack',
            'cam'       : 'https://github.com/ulmononian/NOAA-EMC_spack',
            'spack'     : 'https://github.com/spack/spack',
            },
        'doc/CMakeModules' : {
            'noaa-emc'  : 'https://github.com/NOAA-EMC/CMakeModules',
            'dom'       : 'https://github.com/climbfuji/CMakeModules',
            },
        },
    'spack' : {
        '.' : {
            'jcsda'     : 'https://github.com/jcsda/spack',
            'dom'       : 'https://github.com/climbfuji/spack',
            'alex'      : 'https://github.com/alexanderrichert-noaa/spack',
            'cam'       : 'https://github.com/ulmononian/NOAA-EMC_spack',
            'spack'     : 'https://github.com/spack/spack',
            },
        },
    # JEDI repos
    'ewok' : {
        '.' : {
            'internal'  : 'https://github.com/jcsda-internal/ewok',
            },
        },
    'fv3-jedi' : {
        '.' : {
            'internal'  : 'https://github.com/jcsda-internal/fv3-jedi',
            'public'    : 'https://github.com/jcsda/fv3-jedi',
            },
        },
    'fv3-jedi-data' : {
        '.' : {
            'internal'  : 'https://github.com/jcsda-internal/fv3-jedi-data',
            },
        },
    'ioda-data' : {
        '.' : {
            'internal'  : 'https://github.com/jcsda-internal/ioda-data',
            },
        },
    'ioda' : {
        '.' : {
            'internal'  : 'https://github.com/jcsda-internal/ioda',
            'public'    : 'https://github.com/jcsda/ioda',
            },
        },
    'jedi-docs' : {
        '.' : {
            'internal'  : 'https://github.com/jcsda-internal/jedi-docs',
            'public'    : 'https://github.com/jcsda/jedi-docs',
            },
        },
    'oops' : {
        '.' : {
            'internal'  : 'https://github.com/jcsda-internal/oops',
            'public'    : 'https://github.com/jcsda/oops',
            },
        },
    'r2d2' : {
        '.' : {
            'internal'  : 'https://github.com/jcsda-internal/r2d2',
            },
        },
    'r2d2-data' : {
        '.' : {
            'internal'  : 'https://github.com/jcsda-internal/r2d2-data',
            },
        },
    'saber' : {
        '.' : {
            'internal'  : 'https://github.com/jcsda-internal/saber',
            'public'    : 'https://github.com/jcsda/saber',
            },
        },
    'simobs' : {
        '.' : {
            'internal'  : 'https://github.com/jcsda-internal/simobs',
            },
        },
    'soca' : {
        '.' : {
            'internal'  : 'https://github.com/jcsda-internal/soca',
            'public'    : 'https://github.com/jcsda/soca',
            },
        },
    'solo' : {
        '.' : {
            'internal'  : 'https://github.com/jcsda-internal/solo',
            },
        },
    'ufo' : {
        '.' : {
            'internal'  : 'https://github.com/jcsda-internal/ufo',
            'public'    : 'https://github.com/jcsda/ufo',
            },
        },
    'ufo-data' : {
        '.' : {
            'internal'  : 'https://github.com/jcsda-internal/ufo-data',
            },
        },
    'vader' : {
        '.' : {
            'internal'  : 'https://github.com/jcsda-internal/vader',
            'public'    : 'https://github.com/jcsda/vader',
            },
        },
    'domtools' : {
        '.' : {
            'dom'       : 'https://github.com/climbfuji/domtools',
            },
        },
    }

URL_PATTERN = re.compile(u'^https\:\/\/github\.com\/(.+)\/(.+)$')

def execute(cmd, abort = True):
    """Runs a local command in a shell. Waits for completion and
    returns status, stdout and stderr. If abort = True, abort in
    case an error occurs during the execution of the command."""

    # Set debug to true if logging level is debug
    debug = logging.getLogger().getEffectiveLevel() == logging.DEBUG

    logging.info('Executing "{0}"'.format(cmd))
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                         stderr = subprocess.PIPE, shell = True)
    (stdout, stderr) = p.communicate()
    status = p.returncode
    if debug:
        message = 'Execution of "{0}" returned with exit code {1}\n'.format(cmd, status)
        message += '    stdout: "{0}"\n'.format(stdout.decode(encoding='ascii', errors='ignore').rstrip('\n'))
        message += '    stderr: "{0}"'.format(stderr.decode(encoding='ascii', errors='ignore').rstrip('\n'))
        logging.debug(message)
    if not status == 0:
        message = 'Execution of command {0} failed, exit code {1}\n'.format(cmd, status)
        message += '    stdout: "{0}"\n'.format(stdout.decode(encoding='ascii', errors='ignore').rstrip('\n'))
        message += '    stderr: "{0}"'.format(stderr.decode(encoding='ascii', errors='ignore').rstrip('\n'))
        if abort:
            raise Exception(message)
        else:
            logging.error(message)
    return (status, stdout.decode(encoding='ascii', errors='ignore').rstrip('\n'),
                    stderr.decode(encoding='ascii', errors='ignore').rstrip('\n'))

def get_configured_remotes():
    """Scan all configured remotes in the current working directory"""
    configured_remotes = {}
    (status, stdout, stderr) = execute('git remote -v show')
    for line in stdout.split('\n'):
        (current_name, url, action) = line.split()
        if action == 'push':
            continue
        configured_remotes[current_name] = url
    return configured_remotes

# Configure logging
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

# First, identify the top-level repository
logging.info("Identifying top-level repository name")
os.chdir(topdir)
configured_remotes = get_configured_remotes()
repo_names = [ x.split('/')[-1] for x in list(configured_remotes.values())]
if (len(set(repo_names))==1):
    if repo_names[0].lower() in ALL_REMOTES.keys():
        REMOTES = ALL_REMOTES[repo_names[0].lower()]
    else:
        raise Exception("Top-level repository {} not configured in ALL_REMOTES".format(
            repo_names[0].lower()))
else:
    raise Exception("Cannot identify unique repository name: {}".format(set(repo_names)))
logging.info("Top-level repository name is {}".format(repo_names[0].lower()))

for subdir in REMOTES.keys():
    logging.info("Configuring remotes for subdirectory {} of {}".format(subdir, topdir))
    os.chdir(os.path.join(topdir, subdir))
    configured_remotes = get_configured_remotes()

    configured_remotes_keys = list(configured_remotes.keys())
    for current_name in configured_remotes_keys:
        current_url = configured_remotes[current_name]
        if current_name == 'origin':
            for name in REMOTES[subdir]:
                url = REMOTES[subdir][name]
                if current_url.lower() == url.lower():
                    (status, stdout, stderr) = execute('git remote rename {} {}'.format(current_name, name))
                    configured_remotes[name] = REMOTES[subdir][name]
                    del configured_remotes[current_name]
    # Find missing remotes and add them
    for name in REMOTES[subdir]:
        if not name in configured_remotes.keys():
            (status, stdout, stderr) = execute('git remote add {} {}'.format(name, REMOTES[subdir][name]))
            configured_remotes[name] = REMOTES[subdir][name]
    # Update remotes
    (status, stdout, stderr) = execute('git remote update')
    os.chdir(topdir)