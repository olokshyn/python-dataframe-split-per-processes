#!/bin/bash

set -e

python_path="$1"
script_path="$2"
shift 2
args="$@"

rm /tmp/mem.log
rm /tmp/show_mem.plt

cat <<EOF > "/tmp/show_mem.plt"
set term png small size 800,600
set output "mem-graph.png"

set ylabel "%MEM"
set y2label "VSZ"

set ytics nomirror
set y2tics nomirror in

set yrange [0:*]
set y2range [0:*]

plot "/tmp/mem.log" using 1 with lines axes x1y1 title "%MEM", \
     "/tmp/mem.log" using 2 with lines axes x1y2 title "VSZ"

EOF

echo "Starting the process"
$python_path $script_path $args &

while true; do
  pids="$(pgrep -f $script_path)"
  if [[ -z "$pids" ]]; then
    echo "Processes have finished"
    exit 0
  fi
  echo "Found PIDs: $pids"
  total_mem="0"
  total_vsz="0"
  for pid in $pids; do
    read -r mem vsz <<<$(ps -p $pid -o %mem=,vsz=)
    mem=${mem%.*}
    if [[ -n "$mem" ]] && [[ -n "$vsz" ]]; then
      echo "For pid $pid got %mem=$mem and vsz=$vsz"
      total_mem=$(($total_mem + $mem))
      total_vsz=$(($total_vsz + $vsz))
    fi
  done
  echo "Total: %mem=$total_mem and vsz=$total_vsz"
  echo $total_mem $total_vsz >> /tmp/mem.log
  gnuplot /tmp/show_mem.plt
  sleep 1
done
