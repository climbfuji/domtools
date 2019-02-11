#!/usr/bin/env python

__doc__ = """**Introduction**

This script clones the NEMSfv3gfs code and its submodules from the default repository on GitHub,
sets up the forks and checks out the branches as requested.

**Usage**

./checkout_nemsfv3gfs.py --help

usage: checkout_nemsfv3gfs.py [-h] [--config=CONFIG]

Checkout NEMSfv3gfs repository and submodules.

| optional arguments:
|     -h, --help       show this help message and exit
|     --config CONFIG  name of config file (default: checkout_nemsfv3gfs.cfg)

**Example configuration file checkout_nemsfv3gfs.cfg (default values)**

| [default]
| basedir = /scratch4/home/Dom.Heinzeller/NEMSfv3gfs/checkout
| gituser = climbfuji

| [NEMSfv3gfs]
| add_own_fork = True
| fork = NCAR
| branch = gmtb/ccpp

| [NEMS]
| add_own_fork = True
| fork = NCAR
| branch = gmtb/ccpp

| [FV3]
| add_own_fork = True
| fork = NCAR
| branch = gmtb/ccpp

| [FMS]
| add_own_fork = False
| fork = NCAR
| branch = GFS-FMS

| [ccpp-framework]
| add_own_fork = True
| fork = NCAR
| branch = master

| [ccpp-physics]
| add_own_fork = True
| fork = NCAR
| branch = master

**Documentation of individual subroutines**
"""

import argparse
import ConfigParser
import datetime
import os
import shutil
import subprocess
import sys

###############################################################################
# Global settings                                                             #
###############################################################################

# Template for repository URLs
REPOSITORY_URL_TEMPLATE = 'https://github.com/{fork}/{repo}.git'

# Name of default fork/branch to clone before adding own forks/branches
PARENT_REPOSITORY_DEFAULT_FORK = 'NCAR'
PARENT_REPOSITORY_DEFAULT_BRANCH = 'gmtb/ccpp'

# Name of parent repository
PARENT_REPOSITORY = 'NEMSfv3gfs'

# Names and directorieus of submodules in parent repository
SUBMODULES = {
    'NEMS' : 'NEMS',
    'FV3' : 'FV3',
    'FMS' : 'FMS',
    'ccpp-framework' : 'ccpp/framework',
    'ccpp-physics' : 'ccpp/physics',
    }

# List of all repositories (parent and submodules)
REPOSITORIES = [PARENT_REPOSITORY] + SUBMODULES.keys()

###############################################################################
# Work routines and main entry points                                         #
###############################################################################

def parse_arguments():
    """Parse command line arguments."""
    description = 'Code checkout script for NEMSfv3gfs'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--config', action='store', help='name of checkout config', 
                        default='checkout_nemsfv3gfs.cfg')
    args = parser.parse_args()
    return args.config

def parse_config(configfile):
    """Parse the specified config file and return configuration."""
    if os.path.exists(configfile):
        config = ConfigParser.RawConfigParser()
        config.read(configfile)
    else:
        raise Exception('Config file {0} not found'.format(configfile))
    # Base directory
    basedir = config.get('default', 'basedir')
    gituser = config.get('default', 'gituser')
    # Dictionaries with names of forks and branches for all repositories
    add_own_forks = {}
    forks = {}
    branches = {}
    for repository in REPOSITORIES:
        add_own_forks[repository] = config.getboolean(repository, 'add_own_fork')
        forks[repository] = config.get(repository, 'fork')
        branches[repository] = config.get(repository, 'branch')
    return (basedir, gituser, add_own_forks, forks, branches)

def execute(cmd, abort = True):
    """Runs a local command in a shell and capture the exit status.
    If abort = True, abort in case an error occurs during the
    execution of the command."""
    print "Executing '{0}'".format(cmd)
    status = os.system(cmd)
    if not status == 0:
        if abort:
            message = 'Execution of command {0} failed, return code = {1}'.format(cmd, status)
            raise Exception(message)
        else:
            message = 'WARNING: Execution of command {0} failed, return code = {1}; ignore and proceed'.format(cmd, status)
            print message
    return status

def setup_workdir(basedir):
    """Configure the work directory = base directory + name of parent repository,
    abort if this directory already exists"""
    workdir = os.path.join(basedir, PARENT_REPOSITORY)
    if os.path.isdir(workdir):
        raise Exception(' Target directory to checkout the code already exists: {0}'.format(workdir))
    return workdir

def checkout_code(workdir, gituser, add_own_forks, forks, branches):
    """Check out the main repository, initialize its submodules, add
    personal forks and switch to the requested forks/branches."""
    # Compose url of main repository for the default fork
    url = REPOSITORY_URL_TEMPLATE.format(fork=PARENT_REPOSITORY_DEFAULT_FORK, repo=PARENT_REPOSITORY)
    # Check out main repository into the work directory
    cmd = 'git clone --branch {branch} {url} {dirname}'.format(url=url,
                                                               branch=PARENT_REPOSITORY_DEFAULT_BRANCH,
                                                               dirname=workdir)
    execute(cmd)
    # Change to parent repository (work directory)
    os.chdir(workdir)
    # Initialize the submodules
    cmd = 'git submodule update --init'
    execute(cmd)
    # For each of the submodules and the main repository,
    # add the user fork if asked to do so, and check
    # out the code from the requested fork/branch
    for repo in forks.keys():
        if repo in SUBMODULES.keys():
            subdir = os.path.join(workdir, SUBMODULES[repo])
            os.chdir(subdir)
        # Rename default repository from origin to upstream
        cmd = 'git remote rename origin upstream'
        execute(cmd)
        # Add user fork if requested
        if add_own_forks[repo]:
            remote = REPOSITORY_URL_TEMPLATE.format(fork=gituser, repo=repo)
            cmd = 'git remote add origin {remote}'.format(remote=remote)
            execute(cmd)
        # Update from remote
        cmd = 'git remote update'
        execute(cmd)
        # Checkout requested fork/branch
        if forks[repo] == gituser:
            if add_own_forks[repo]:
                remote = 'origin'
            else:
                message = 'Logic error: requested to check out branch {branch}'.format(branch=branches[repo])
                message += ' from user fork for repository {repo}, but add_own_fork is False'.format(repo=repo)
                raise Exception(message)
        elif forks[repo] == PARENT_REPOSITORY_DEFAULT_FORK:
            remote = 'upstream'
        else:
            message = 'Logic error: requested to check out branch {branch}'.format(branch=branches[repo])
            message += ' from unknown fork {fork} for repository {repo}'.format(fork=forks[repo], repo=repo)
            raise Exception(message)
        cmd = 'git checkout {remote}/{branch}'.format(remote=remote, branch=branches[repo])
        execute(cmd)
        if repo in SUBMODULES.keys():
            os.chdir(workdir)
    return

def main():
    """Main routine that calls subroutines for each of the steps."""
    # Parse command line arguments
    configfile = parse_arguments()
    # Parse config file
    (basedir, gituser, add_own_forks, forks, branches) = parse_config(configfile)
    # Check that base directory exists
    if not os.path.exists(basedir):
        raise Exception('Base directory {0} does not exist'.format(basedir))
    # Configure working directory
    workdir = setup_workdir(basedir)
    # Check out the code
    checkout_code(workdir, gituser, add_own_forks, forks, branches)
    print "Location of code: {0}".format(workdir)

if __name__ == '__main__':
    main()
