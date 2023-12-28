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


class Gkylzero(MakefilePackage, CudaPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url = "https://github.com/ammarhakim/gkylzero.git"
    git = "https://github.com/ammarhakim/gkylzero.git"

    version('main', branch='main')


    # do not need Cuda variant explicitly since it comes from the CudaPackage
    variant("mpi", default=False, description="Build with MPI support")
    variant("lua", default=False, description="Build with lua support")
    

    depends_on('blas')
    depends_on('lapack')
    depends_on('superlu build_system=cmake')

    depends_on('mpi', when='+mpi')
    depends_on('parmetis', when='+mpi')
    depends_on('superlu-dist', when='+mpi')

    # if os is mac use openresty luajit
    depends_on('luajit', when='+lua')

    conflicts("+cuda", when="cuda_arch=none")

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers("github_user1", "github_user2")

    #ARCH_FLAGS=$ARCH_FLAGS
    @property
    def libs(self):
        return find_libraries('*',root=join_path(self.prefix,"gkylzero/lib"))

    @property
    def headers(self):
        return find_headers('*',root=join_path(self.prefix,"gkylzero/include"))

    def edit(self, spec, prefix):
        #config = { "CC": spack_cc, "PREFIX": prefix}
        config = {"PREFIX": prefix}
        if spec.satisfies("+cuda"):
            # gkyl makefile breaks if you include full path for nvcc compiler!
            #config["CC"] = join_path(spec["cuda"].prefix.bin, "nvcc")
            config["CC"] = "nvcc"
        else:
            config["CC"] = self.compiler.cc
        # default settings for MPI and LUA (will be modified later)
        config['USE_MPI']=0
        config['USE_LUA']=0
        #config['LAPACK_INC']=spec["lapack"].libs.joined()
        config['LAPACK_INC']=spec["lapack"].prefix.include
        config['LAPACK_LIB']=spec["lapack"].libs.joined()
        config['SUPERLU_INC']=spec["superlu"].prefix.include
        #config['SUPERLU_INC']=spec["superlu"].libs.joined()
        config['SUPERLU_LIB']=spec["superlu"].libs.joined()
        #
        if spec.satisfies('+mpi'):
            config['USE_MPI']=1
            config['CONF_MPI_LIB_DIR']=spec["mpi"].prefix.lib
            config['CONF_MPI_INCLUDE_DIR']=spec["mpi"].prefix.include
            mpispec = spec["mpi"]
            config["CC"] = mpispec.mpicc
        if spec.satisfies('+lua'):
            config['USE_LUA']=1
            config['CONF_LUA_LIB_DIR']=spec["luajit"].prefix.lib
            config['CONF_LUA_INCLUDE_DIR']=spec["luajit"].prefix.include
            #FIXME figure out what this should be...
            config['CONF_LUA_LIB']=spec["luajit"].libs.joined()

        if spec.satisfies('+cuda'):
            #CUDAMATH_LIBDIR=$CUDAMATH_LIBDIR
            cuda_arch = spec.variants['cuda_arch'].value
            if cuda_arch != 'none':
                config['CUDA_ARCH'] = cuda_arch[0]
            else:
                raise InstallError('cuda_arch cannot be none for cuda build')

        with open("config.mak", "w") as inc:
            for key in config:
                inc.write(f"{key} = {config[key]}\n")
