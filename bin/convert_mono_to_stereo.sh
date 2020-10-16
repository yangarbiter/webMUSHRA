#!/bin/bash

rootdir=configs/resources/etrab
outdir=configs/resources/etrab_stereo

set -euo pipefail

find ${rootdir} -name "*.wav" | while read -r wavfile; do
    echo ${wavfile}
    outwavfile=$(echo "${wavfile}" | sed -e "s;${rootdir};${outdir};g")
    dir=$(dirname ${outwavfile})
    [ ! -e ${dir} ] && mkdir -p ${dir}
    sox -M "${wavfile}" "${wavfile}" -c 2 "${outwavfile}" pad 0 0.1 pad 0.1
done
