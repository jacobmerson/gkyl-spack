# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install gkylzero
#
# You can edit this file again by typing:
#
#     spack edit gkylzero
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Gkylzero(MakefilePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url = "https://github.com/ammarhakim/gkylzero.git"
    git = "https://github.com/ammarhakim/gkylzero.git"

    version('main', branch='main')

    variant("mpi", default=False, description="Build with MPI support")
    variant("cuda", default=False, description="Build with CUDA support")
    # TODO add cuda_arch 
    variant("lua", default=False, description="Build with lua support")

    depends_on('blas')
    depends_on('lapack')
    depends_on('superlu build_system=cmake')

    depends_on('mpi', when='+mpi')
    depends_on('parmetis', when='+mpi')
    depends_on('superlu-dist', when='+mpi')

    depends_on('cuda', when='+cuda')

    # if os is mac use openresty luajit
    depends_on('luajit', when='+lua')

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers("github_user1", "github_user2")

    #ARCH_FLAGS=$ARCH_FLAGS

    def edit(self, spec, prefix):
        config = { "CC": spack_cc, "PREFIX": prefix}
        config['USE_MPI']=0
        config['USE_LUA']=0
        #config['LAPACK_INC']=spec["lapack"].libs.joined()
        config['LAPACK_INC']=spec["lapack"].prefix.lib
        config['LAPACK_LIB']=spec["lapack"].prefix.include
        config['SUPERLU_INC']=spec["superlu"].prefix.lib
        #config['SUPERLU_INC']=spec["superlu"].libs.joined()
        config['SUPERLU_LIB']=spec["superlu"].prefix.include
        #
        if spec.satisfies('+mpi'):
            config['USE_MPI']=1
            config['CONF_MPI_LIB_DIR']=spec["mpi"].prefix.lib
            config['CONF_MPI_INCLUDE_DIR']=spec["mpi"].prefix.include
        if spec.satisfies('+lua'):
            config['USE_LUA']=1
            config['CONF_LUA_LIB_DIR']=spec["luajit"].prefix.lib
            config['CONF_LUA_INCLUDE_DIR']=spec["luajit"].prefix.include
            #FIXME figure out what this should be...
            config['CONF_LUA_LIB']=spec["luajit"].libs.joined()

        if spec.satisfies('+cuda'):
            #CUDAMATH_LIBDIR=$CUDAMATH_LIBDIR
            #CUDA_ARCH=$CUDA_ARCH
            pass

        with open("config.mak", "w") as inc:
            for key in config:
                inc.write(f"{key} = {config[key]}\n")
