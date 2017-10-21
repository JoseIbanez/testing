#!/usr/bin/expect -f
# Set up various other variables here ($user, $password)
# Usage: ios_cmd.v6.exp <host> <label> <user> <password> <enable> <file> <ASA_RAT>"

#sanity
set timeout 30
match_max 100000

#As first thing we check to have 5 arguments:
if {[llength $argv] != 6} {
        puts "usage: ios_cmd.v6.exp <host> <label> <user> <password> <enable> <file> <ASA_RAT>"
        exit 1
        }

#We define the variables used to handle the input parameters passed to the script
set customer   [lindex $argv 0]
set host       [lindex $argv 1]
set label      [lindex $argv 2]
set secret     [lindex $argv 3]
set input_file [lindex $argv 4]
set ASA_RAT    [lindex $argv 5]

#Import user and password
source [file join [file dirname [info script]] $secret]

# Create folder to store the data extracted during the execution of the script
set now [clock seconds]
set path "../UC_ops/[clock format $now -format {%Y-%m}]/$customer/ios/[clock format $now -format {%Y%m%d-%H%M}]/"
file mkdir $path

#Update last run date
file mkdir  "../UC_ops/$customer/"
set of [open "../UC_ops/$customer/ios.last" "w"]
puts $of [clock format $now -format {%Y%m%d-%H%M}]
close $of

# Get the commands to run, one per line
set f [open $input_file]

#Login
set of [open "$path$label-login.txt" "w"]
if {[info exists $ASA_RAT]} {
        spawn ssh -b 10.108.8.50 -o "StrictHostKeyChecking no" "$user\@$host"
} else {
        spawn ssh -o "StrictHostKeyChecking no" "$user\@$host"
}
expect "assword:"
send "$password\r"

set timeout 1
set count 10

while {1} {
    expect {
            ">" {
                puts $of $expect_out(buffer)
                send "enable\n"
            }
            "assword:" {
                send "$enable\r"
            }
            -re "#$|# $" {
                puts $of $expect_out(buffer)
                send "\r"
                break
            }
            timeout {
                puts "timeout"
                puts $of $expect_out(buffer)
                send "\r"
            }
	}
    set count "[expr $count - 1]"
    if { $count < 0 } {
        exit
    }
}

expect "#"


#Capture Prompt
#set prompt $expect_out(buffer)
set prompt [string range $expect_out(buffer) 3 end]
puts "---Prompt: >>>$prompt<<<\n"


send "terminal length 0\r"
expect $prompt


# Iterate over the commands, one per line
while {[gets $f line] != -1} {
    #If the line is starting by @C, it will be considered as a comment.
    if [string match "@C *" $line] {
        continue
    } 
    #If starts by @L, we create a new file.
    if [string match "@L *" $line] {
        set name [string range $line 3 end]
        set of [open "$path$label-$name.txt" "w"]
		continue
	} 
    # The command is sent to the network element
    send "$line\r"
	sleep .4

    expect {
            "(nxos)#" {
                    puts $of $expect_out(buffer)
                    }
            "(local-mgmt)#" {
                    puts $of $expect_out(buffer)
                    }
            -re "/act#|/stby#" {
                    puts $of $expect_out(buffer)
                    }
            "(config*)#" {
                    puts $of $expect_out(buffer)
                    }
	        "$prompt" {
                    puts $of $expect_out(buffer)
                    }
            timeout {
                    puts $of $expect_out(buffer)
                    }
            full_buffer {
                    puts "full_buffer\n"
                    puts -nonewline $of $expect_out(buffer)
                    exp_continue
                    }
    }
    
}


# Exit
send "exit\r"
expect eof
#close

close $f
