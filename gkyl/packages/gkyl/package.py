# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gkyl(WafPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url = "https://github.com/ammarhakim/gkyl.git"
    git = "https://github.com/ammarhakim/gkyl.git"

    version('main', branch='main')

    # gkyl build does not currently work without MPI
    #variant("mpi", default=False, description="Build with MPI support")

    variant("sqlite", default=False, description="enable sqlite3 support")


    depends_on('luajit')
    depends_on('blas')
    depends_on('mpi')
    depends_on('superlu')
    depends_on('gkylzero+mpi')
    depends_on('adios2+mpi')

    maintainers("ammarhakim")

    license("UNKNOWN")

    def configure_args(self):
        spec = self.spec
        config = dict()
        args = []
        config["enable-mpi"] = ""
        config["mpi-inc-dir"] = spec["mpi"].prefix.include
        config["mpi-lib-dir"] = spec["mpi"].prefix.lib
        #config["mpi-link-libs"] = spec["mpi"].libs.joined()
        mpispec = spec["mpi"]
        mpicc = mpispec.mpicc
        mpicxx = mpispec.mpicxx
        args.extend([f"CC={mpicc}",f"CXX={mpicxx}",f"MPICC={mpicc}",f"MPICXX={mpicxx}"])

        config["enable-adios"] = ""
        config["adios-inc-dir"] = spec["adios2"].prefix.include
        config["adios-lib-dir"] = spec["adios2"].prefix.lib

        gkylzero = spec["gkylzero"]
        config["enable-gkylzero"] = ""
        #config["gkylzero-inc-dir"] = f"{gkylzero.prefix}/gkylzero/include"
        #config["gkylzero-lib-dir"] = f"{gkylzero.prefix}/gkylzero/lib"
        config["gkylzero-inc-dir"] = gkylzero.headers.directories[0]
        config["gkylzero-lib-dir"] = gkylzero.libs.directories[0]

        config["enable-superlu"] = ""
        config["superlu-inc-dir"] = spec["superlu"].prefix.include
        config["superlu-lib-dir"] = spec["superlu"].prefix.lib

        config["enable-openblas"] = ""
        config["openblas-inc-dir"] = spec["blas"].prefix.include
        config["openblas-lib-dir"] = spec["blas"].prefix.lib

        lj = spec["luajit"]
        config["luajit-inc-dir"] = f"{lj.prefix.include}/luajit-{lj.version[0:2]}"
        config["luajit-lib-dir"] = lj.prefix.lib
        config["luajit-share-dir"] = lj.prefix.share

        config["disable-nccl"] = ""
        config["disable-cuda"] = ""

        if spec.satisfies("+sqlite"):
            config["enable-sqlite"] = ""
        else:
            config["disable-sqlite"] = ""

        args.extend([ f"--{key}={val}" if val else f"--{key}" for key,val in config.items()])

        return args
