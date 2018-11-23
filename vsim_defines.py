#!/usr/bin/env python
#
# vsim_defines.py
# Francesco Conti <f.conti@unibo.it>
#
# Copyright (C) 2015 ETH Zurich, University of Bologna
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.
#

# templates for vcompile.csh scripts
VSIM_PREAMBLE = """#!/bin/tcsh
source ${PULP_PATH}/%s/vcompile/setup.csh

##############################################################################
# Settings
##############################################################################

set IP=%s

##############################################################################
# Check settings
##############################################################################

# check if environment variables are defined
if (! $?MSIM_LIBS_PATH ) then
  echo "${Red} MSIM_LIBS_PATH is not defined ${NC}"
  exit 1
endif

if (! $?IPS_PATH ) then
  echo "${Red} IPS_PATH is not defined ${NC}"
  exit 1
endif

set LIB_NAME="${IP}"
set LIB_PATH="${MSIM_LIBS_PATH}/${LIB_NAME}"
set IP_PATH="${IPS_PATH}/%s"
set RTL_PATH="${RTL_PATH}"


##############################################################################
# Preparing library
##############################################################################

echo "${Green}--> Compiling ${IP}... ${NC}"

rm -rf $LIB_PATH

if ( -d "./INCA_libs/${LIB_NAME}/" ) then
	rm -rf ./INCA_libs/${LIB_NAME}/
endif

mkdir ./INCA_libs/${LIB_NAME}
echo "DEFINE ${LIB_NAME} ./INCA_libs/${LIB_NAME}"/ >> cds.lib

setenv Target_File  `find ${IP_PATH} -name "*.sv" -o -name "*.v" -o -name "*.vhd"`
# find ${IP_PATH} -name "*.sv" -o -name "*.v"
# echo "${Green} $Target_File"

# ncvlog -q -sv -nocop -cdslib cds.lib -nowarn NONPRT -work ${LIB_NAME} 	 $Target_File -nowarn DLNOHV -incdir $IP_PATH -incdir ${IP_PATH}/include -nowarn NOTIND -nowarn UEXPSC \n

##############################################################################
# Compiling RTL
##############################################################################
"""

VSIM_POSTAMBLE ="""
echo "${Cyan}--> ${IP} compilation complete! ${NC}"
exit 0

##############################################################################
# Error handler
##############################################################################

error:
echo "${NC}"
exit 1
"""

VSIM_PREAMBLE_SUBIP = """
echo "${Green}Compiling component: ${Brown} %s ${NC}"
echo "${Red}"
"""
VSIM_VLOG_INCDIR_CMD = ""

## Add -suppress 2583 to remove warning about always_comb|ff wrapped with
# generate struct that can be only checked after elaboration at vopt stage
VSIM_VLOG_CMD =""" 
set Dbg1 = "%s"
set Dbg2 = "%s"
set Dbg3 = "%s"
# echo "$Dbg1"
# echo "$Dbg2"
# echo "$Dbg3"

set DirPath_aux = ~${Dbg3}
set DirPath		= ${Dbg3:h}
# echo "Dbg3 = $Dbg3"
set FileExt    = ${DirPath_aux:e}
# echo "FileExt = $FileExt"
ncvlog -q -sv -nocop -cdslib cds.lib -nowarn NONPRT -work ${LIB_NAME} $Dbg3 -sv -nowarn DLNOHV -incdir $Dbg2 -incdir ${Dbg2}/include -sv -incdir $DirPath -sv -nowarn NOTIND -nowarn UEXPSC \n

"""

VSIM_VCOM_CMD = """
set Dbg2 = "%s"
set Dbg3 = "%s"
# echo "$Dbg3"

set DirPath_aux = ~${Dbg3}
set DirPath		= ${DirPath_aux:h}
ncvhdl -q -nocop -cdslib cds.lib -nowarn NONPRT -work ${LIB_NAME} -v93	 $Dbg3 -nowarn DLNOHV -nowarn NOTIND -nowarn UEXPSC \n
# echo "${Blue} ncvhdl -q -nocop -cdslib cds.lib -nowarn NONPRT -work ${LIB_NAME} -v93	 $Dbg3 -nowarn DLNOHV "
# echo "${Red}"
"""


# templates for vsim.tcl
VSIM_TCL_PREAMBLE = """set VSIM_IP_LIBS " \\\

"""

VSIM_TCL_CMD = """
  Vsim_tcl_cmd_arg = %s
  echo "VSIM_TCL_CMD, $Vsim_tcl_cmd_arg" 
"""

VSIM_TCL_POSTAMBLE = """
 echo "VSIM_TCL_POSTAMBLE" 
 """


# templates for vcompile_libs.tc
VCOMPILE_LIBS_PREAMBLE = """#!/usr/bin/tcsh

echo \"\"
echo \"${Green}--> Compiling PULP IPs libraries... ${NC}\"
echo 'include $CDS_INST_DIR/tools/inca/files/cds.lib' >> cds.lib
"""

VCOMPILE_LIBS_CMD = """

tcsh ${PULP_PATH}/%s/vcompile/ips/vcompile_%s.csh || exit 1\n
"""
VCOMPILE_LIBS_XILINX_CMD = "tcsh ${PULP_PATH}/fpga/sim/vcompile/ips/vcompile_%s.csh || exit 1\n"
