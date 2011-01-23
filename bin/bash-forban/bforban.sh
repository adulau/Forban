#!/bin/bash
#
# standalone Forban "client" written in Bash
#
# This is just a proof-of-concept to show how
# easy it's to get a script using
# the Forban protocol
#
# Software required: tcpdump and curl

function GetAnnounce {
sudo tcpdump -c 1 -t -p -n -l -A -s0 -iany "udp and port 12555 and udp[8:2]==0x666f" 2>/dev/null
}

function GetName {
# input of tcpdump and just the forban packet
awk '/forban/' | awk '{split ($1, a, "forban");print a[2]}' | cut -d';' -f3
}

function GetUUID {
# input of tcpdump and just the forban packet
awk '/forban/'| awk '{split ($1, a, "forban");print a[2]}' | cut -d';' -f5
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

function GetIndex {
URLP=$1
INDEXSUFFIX="s/?g=forban/index"
U=${URLP}${INDEXSUFFIX}
echo ${U}
curl -f -s "${U}"
}
function ForbanSearch {
        while [ 1 ];
        do
                keywords=$1
                A=`GetAnnounce`
                X=`echo "${A}" | GetSourceIP`
                UUID=`echo "${A}" | GetUUID`
                NAME=`echo "${A}" | GetName`
                URL=`echo ${X} | GetURL`
                echo "Found Forban" ${NAME} "("${UUID}")" ${URL}
                GetIndex ${URL} | grep -i ${keywords} | awk '{print "-> " $0}'
                echo
        done
}


function ForbanDiscover {
        TYPE=$1
        [ -z $1 ] && TYPE="normal"
        URLOPEN=()

        while [ 1 ];
        do
                A=`GetAnnounce`
                X=`echo "${A}" | GetSourceIP`
                UUID=`echo "${A}" | GetUUID`
                NAME=`echo "${A}" | GetName`        
                echo "Found Forban" ${NAME} "("${UUID}")"
                URL=`echo ${X} | GetURL`
                if [ ${TYPE} == "browse" ]; then
                        urll="notvisited"
                        for urlo in ${URLOPEN[*]}
                        do
                                if [ ${urlo} == ${URL} ]; then
                                        urll="visited"
                                fi
                        done
                        if [ ${urll} == "notvisited" ]; then
                                echo "not visited, opening a browser page..."
                                if [ `uname` == "Darwin" ]; then
                                        open ${URL}
                                else
                                        firefox ${URL}
                                fi
                                URLOPEN=("${URLOPEN[@]}" "${URL}")
                        fi
                fi


                echo ${URL}
        done
}

case "$1" in
        monitor)    ForbanDiscover
                    ;;
        bmonitor)   ForbanDiscover browse
                    ;;
        search)     keywords=$2
                    ForbanSearch ${keywords}
                    ;;
        *)          echo $0 "[monitor] [bmonitor] [search {keywords}]"
esac

