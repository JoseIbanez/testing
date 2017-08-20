
set title "Data usage over the last 24 hours"
unset multiplot
set xdata time
set style data lines  
set term png
set timefmt "%Y-%m-%dT%H:%M:%S"
#set format x "%Y-%m-%dT%H:%M:%S"
set xlabel "Time"
set ylabel "Temp" 
set terminal png size 1024,768
set autoscale y  
set datafile separator ","
#set autoscale x
#set xrange ["2017-08-08 00:00":"2017-08-08 23:59"]
set output "temp.png"
plot "sample.csv" using 1:3 title 'Last day'