#!/usr/bin/expect

set username "cisco"
set password "password"
set enablepassword "secret"

set timeout 3
set port [lrange $argv 0 0]

spawn telnet 127.0.0.1 $port

expect {
	"*Escape character*" {
		send "\r"
		sleep 2
		expect {
			eof {
				send "\r"
				exp_continue
			}
			 ">" {
				send "enable\r"
				expect "Password" {
					send "cisco\n"
					exp_continue
				}
				exp_continue
			}
			"#" {
				send "copy running-config unix://running-config\n"
				expect "Destination filename" {
					send "\n"
					exp_continue
				}
				expect "Do you want to over write" {
					send "\n"
					exp_continue
				}
				expect "bytes copied" {
					send "quit\n"
				}
			}
		}
	}
}
close

#for i in $(seq 1 32); do ./export_conf.sh 2$(printf "%03d" $i); done
