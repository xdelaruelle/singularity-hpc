# Singularity Registry HPC (shpc)

[![GitHub actions status](https://github.com/singularityhub/singularity-hpc/workflows/sregistry-ci/badge.svg?branch=master)](https://github.com/singularityhub/singularity-hpc/actions?query=branch%3Amain+workflow%3Asingularity-hpc)

Singularity HPC is based off of the [Singularity Registry Client](https://github.com/singularityhub/sregistry-cli), but instead of
being intended for general interaction with Singularity containers and a local database, it's optimized for managing containers
in an HPC environment. Currently, this includes:

 - [LMOD](https://lmod.readthedocs.io/en/latest/)

You can use shpc if you are:

1. a linux administrator wanting to manage containers as modules for your cluster
2. a cluster user that wants to maintain your own folder of custom modules
3. a cluster user that simply wants to pull Singularity images as GitHub packages.

These use cases will be better flushed out and documented as the library is developed.
**documentation coming shortly**

## Tests to write

 - Settings load, update, get, etc.
 - Ensure that all defaults are present in settings (except for updated at)
 

## Previous Art

There are other tools that you might be interested in!

 - [VA Research Computing](https://www.rc.virginia.edu/userinfo/rivanna/software/containers/) has a similar system, but I couldn't find any code.
 - [Community Collections](https://github.com/community-collections/community-collections)
 - [Spack](https://spack.readthedocs.io/en/latest/module_file_support.html) installs modules for software built from source (not containers).
 
## TODOS

 - finish install, write add and other commands
 - ensure that we print columns to shpc list
 - test singularity build in actions, save to registry
 - develop pull command for shpc for this type, along with GitHub action

## License

This code is licensed under the MPL 2.0 [LICENSE](LICENSE).
