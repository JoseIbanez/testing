#!/usr/bin/perl

use strict 'vars';
use File::Basename;
use Getopt::Long;
use IO::Socket;
use POSIX qw(:sys_wait_h);
use IO::Select;

my $version = "0.1";	# wrapper-linux version
my $image;				# storing IOU full image name (e.g. /opt/iou/bin/I86BI_LINUX-IPBASE-M-12.4)
my $port;				# storing telnet port (e.g. 2001)
my $path;				# storing IOU running path (e.g. /opt/iou/bin) 
my $iou_pid;			# pid for iou process

sub main::HELP_MESSAGE {
    print STDERR "Usage: splice [-a arch] [-e exclude_file] [-l log_file] [-r] DIR...\n\n";
    print STDERR "Repositories should be listed in increasing priority order\n";
    print STDERR "  -a <arch>  Target different arch than this host\n";
    print STDERR "  -e <file>  Exclude keys listed in this file\n";
    print STDERR "  -l <file>  Write comprehensive log to file\n";
    print STDERR "  -n         No new keys.  Build package list from root repo only\n";
    print STDERR "  -r         Replace only mode.  Don't upgrade to later versions.\n";
}
sub main::VERSION_MESSAGE {
	print "version\n";
}
sub REAPER {
    1 until (-1 == waitpid(-1, WNOHANG));
    $SIG{CHLD} = \&REAPER;                 # unless $] >= 5.002
}

# Getting options (m = IOU image, p = telnet port, @ARGV = IOU options)
GetOptions (
	'm=s' => \$image,
	'p=i' => \$port,
);
$path = dirname($image);

print "Starting IOU: $image @ARGV\n";

use IPC::Open3;

#my($chld_out, $chld_in, $chld_err);
#$iou_pid = open3(\*WRITER, \*READER, \*ERROR, "cd $path; $image @ARGV");
#$iou_pid = open3(\*WRITER, \*READER, \*ERROR, "/bin/bash");





#my $pid = open3(\*WRITE, \*READ,\*ERROR,"/bin/bash");
my $iou_pid = open3(\*WRITE, \*READ,\*ERROR,"cd $path; $image @ARGV");
            #if \*ERROR is false, STDERR is sent to STDOUT  
			
my $selread = new IO::Select();
my $selerror = new IO::Select();
my $selwrite = new IO::Select();
$selread->add(\*READ);
$selerror->add(\*ERROR);




# may not be best use of IO::Select, but it works :-) 

my($error,$answer)=('','');

while(1){

print "Enter expression for bc, i.e. 2 + 2\n";
chomp(my $query = <STDIN>);

#send query to bc 
print WRITE "$query\n";

#timing delay needed tp let bc output 
select(undef,undef,undef,.01);

#see which filehandles have output 
if($selread->can_read(0)){print "ready->read\n"}
if($selerror->can_read(0)){print "ready->error\n"}

#get any error from bc 
sysread(ERROR,$error,4096) if $selerror->can_read(0);
if($error){print "\e[1;31m ERROR-> $error \e[0m \n"}

#get the answer from bc 
sysread(READ,$answer,4096) if $selread->can_read(0);
if($answer){print "$query = $answer\n"}

($error,$answer)=('','');
}

waitpid($iou_pid, 1);
# It is important to waitpid on your child process,   
# otherwise zombies could be created.  
# It is important to waitpid on your child process,   
# otherwise zombies could be created.  




#open(IOU, "cd $path; $image @ARGV |") || die "Failed: $!\n";

#while (<IOU>) {
#	print;
#}

# http://perldoc.perl.org/perlipc.html#Using-open()-for-IPC
# Complete Dissociation of Child from Parent
#open(IOU, "cd $path; $image @ARGV |") || die "Failed: $!\n";

exit 0;

