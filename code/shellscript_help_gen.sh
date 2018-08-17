#!/bin/bash
FILE=$1

cat << EOF >> $FILE

usage="\$(basename "\$0") [-h] [-x] -- your message of the script

where:
    -h  show this help text
    -x  xxx"

while getopts ':hs:' option; do
  case "\$option" in
    h) echo "\$usage"
       exit
       ;;
    x) echo "xxx"
       ;;
    :) printf "missing argument for -%s\n" "\$OPTARG" >&2
       echo "\$usage" >&2
       exit 1
       ;;
   \?) printf "illegal option: -%s\n" "\$OPTARG" >&2
       echo "\$usage" >&2
       exit 1
       ;;
  esac
done
shift \$((OPTIND - 1))

EOF
