#!/bin/bash

set -e

if [[ $# -ne 2 ]]; then
  echo "Insufficient arguments provided:"
  #echo " - provide system name as first argument, possible values: cheyenne, gaea, hera, jet, orion"
  echo " - provide system name as first argument, possible values: cheyenne, orion"
  echo " - provide target directory as second argument"
  exit 1
fi

SYSTEM=$1
TARGET=$2

case ${SYSTEM} in
  cheyenne)
    GROUP=ncar
    ;;
  #gaea)
  #  GROUP=esrl
  #  ;;
  #hera)
  #  GROUP=nems
  #  ;;
  #jet)
  #  GROUP=h-nems
  #  ;;
  orion)
    GROUP=nems
    ;;
  *)
    echo "Unknown system ${SYSTEM}"
    exit 1
    ;;
esac

if [[ ! -d ${TARGET} ]]; then
  echo "Directory ${TARGET} does not exist!"
  exit 1
fi

echo "Adjusting permissions ..."
chgrp -R ${GROUP} ${TARGET}
chmod -R g+rw ${TARGET}
chmod -R o+r ${TARGET}
chmod a+x `find ./${TARGET} -type d`

echo "Done."
