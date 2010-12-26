#!/bin/bash
#
# standalone Forban "client" written in Bash
# 
# Software required: tcpdump
#

function GetAnnounce {
sudo tcpdump -c 1 -t -p -n -l -A -s0 -ien1 "udp and port 12555 and udp[8:2]==0x666f" 2>/dev/null
}

function GetName {
# $1 is the announce message
awk 'NR==2' | cut -d';' -f3
}

function GetUUID {
# $1 is the announce message
awk 'NR==2' | cut -d';' -f5
}

function GetSourceIP {
# $1 is the announce message
# Only work in IPv4 until now
awk 'NR==1' | awk '{print $2}' | cut -d. -f1,2,3,4       
}

function GetURL {
#$1 is the IP
awk '{print "http://" $1 ":12555/"}'
}

function ForbanDiscover {
        while [ 1 ];
        do
                A=`GetAnnounce`
                X=`echo "${A}" | GetSourceIP`
                UUID=`echo "${A}" | GetUUID`
                NAME=`echo "${A}" | GetName`        
                echo "Found Forban" ${NAME} "("${UUID}")"
                echo ${X} | GetURL
        done
}

case "$1" in
        monitor)    ForbanDiscover
                    ;;
        *)          echo $0 "[monitor]"
esac

