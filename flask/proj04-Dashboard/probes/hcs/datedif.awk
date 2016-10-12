#!/usr/bin/awk -f
BEGIN { FS=" " }
{
  str="date '+%Y-%m-%d %h:%M' -d \"" $2 " " $3 " " period "days \""
  #print str
  str| getline wDate

  #print wDate " " today
  if (wDate > today)
    print $1 " " $2 " " $3

}
