#!/usr/bin/python2
#------------------------------------------------------------------------------
#    Copyright (c) 2013 EPAM Systems
#------------------------------------------------------------------------------
#
#    This file is part of Nfstrace.
#
#    Nfstrace is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 2 of the License.
#
#    Nfstrace is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Nfstrace.  If not, see <http://www.gnu.org/licenses/>.
#
#------------------------------------------------------------------------------

import sys
import os
import signal
import subprocess as subprc

def system(*popenargs, **kwargs):
    kwargs['shell'] = True
    if 'stdout' in kwargs:
        raise ValueError('stdout argument not allowed, it will be overridden.')
    process = subprc.Popen(stdout=subprc.PIPE, *popenargs, **kwargs)
    output, unused_err = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        raise RuntimeError(retcode, cmd)
    return output

def main (argv):
    # should be dir with access for user to changes
    try:
        cd_op = "cd " + argv[3]
        system(cd_op + " && rm -rf testdir")
        system(cd_op + " && mkdir testdir")
        system(cd_op + " && chmod 777 testdir")
        for i in range(0, int(argv[1])):
            cd_op = "cd " + argv[3]
            cd_op += "/testdir &&"
            system(cd_op + " dd if=/dev/zero of=testfile" + str(i) + " bs=1K count=" + argv[2])
        system(cd_op + " && ls")
        system(cd_op + " && ls")
        system(cd_op + " && ls")
        system(cd_op + " cd .. && rm -rf testdir")
    except:
        os.killpg(0, signal.SIGKILL)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print sys.argv[0] + " [number of iterations] [size in kbytes] [path to mounted NFS directory]"
        sys.exit(2)
    main(sys.argv)