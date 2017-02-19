#!/usr/bin/perl

use strict;
use warnings;

#my $file = $ARGV[0];
#open my $fi, $file or die "Could not open $file: $!";


my $file = shift @ARGV;

my $fi;
my $is_stdin = 0;
if (defined $file){
  open $fi, "<", $file or die $!;
} else {
  $fi = *STDIN;
  $is_stdin++;
}

my $phase=0;
my $lastLine="";

my $aux;
my $col;
my $value;
my $cust;
my $date;
my $kpi;
my $domain;

while( my $line = <$fi>)  {
    chomp $line;
    $line =~ s/^\s+|\s+$//g;

    if ($line =~ /.*: /) {

        ($col,$value) = split(' ',$line,2);


        if ($col eq "cust:") {
           $cust=$value;
        }

        if ($col eq "ldate:") {
           $date=$value;
        }

        if ($col eq "domain:") {
           $domain=$value;
        }

        if ($col eq "kpi:") {
           $kpi=$value;
           $phase=1;
           next;
        }

    }

    if (length($line) < 1) {
       $phase=0;
       $cust="";
       $date="";
       $kpi="";
       next;
    }


    if (($phase == 1)) {
        $value=$line;
        $phase=0;
        printf("%s,%s,%s,%s,%s\n",$cust,$kpi,$domain,$value,$date);
    }





}


close $fi unless $is_stdin;
