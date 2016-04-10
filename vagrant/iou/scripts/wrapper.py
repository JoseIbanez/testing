#!/usr/bin/python

__author__     = 'Andrea Dainese'
__copyright__  = 'Andrea Dainese'
__license__    = 'GPL'
__version__    = '0.0.1'
__maintainer__ = 'Amdrea Daimese'
__email__      = 'andrea.dainese@gmail.com'

import asyncore, getopt, socket, select, signal, subprocess, sys, threading, time

bin = ''
port = 0
xtitle = 'Terminal Server'
bin_args = ''
terminate = False

# https://code.google.com/p/miniboa/source/browse/trunk/miniboa/telnet.py
#--[ Telnet Commands ]---------------------------------------------------------
SE     = chr(240) # End of subnegotiation parameters
NOP    = chr(241) # No operation
DATMK  = chr(242) # Data stream portion of a sync.
BREAK  = chr(243) # NVT Character BRK
IP     = chr(244) # Interrupt Process
AO     = chr(245) # Abort Output
AYT    = chr(246) # Are you there
EC     = chr(247) # Erase Character
EL     = chr(248) # Erase Line
GA     = chr(249) # The Go Ahead Signal
SB     = chr(250) # Sub-option to follow
WILL   = chr(251) # Will; request or confirm option begin
WONT   = chr(252) # Wont; deny option request
DO     = chr(253) # Do = Request or confirm remote option
DONT   = chr(254) # Don't = Demand or confirm option halt
IAC    = chr(255) # Interpret as Command
SEND   = chr(001) # Sub-process negotiation SEND command
IS     = chr(000) # Sub-process negotiation IS command
#--[ Telnet Options ]----------------------------------------------------------
BINARY = chr(  0) # Transmit Binary
ECHO   = chr(  1) # Echo characters back to sender
RECON  = chr(  2) # Reconnection
SGA    = chr(  3) # Suppress Go-Ahead
TTYPE  = chr( 24) # Terminal Type
NAWS   = chr( 31) # Negotiate About Window Size
LINEMO = chr( 34) # Line Mode

TELNET_CMD = [SE, NOP, DATMK, BREAK, IP, AO, AYT, EC, EL, GA, SB, WILL, WONT, DO, DONT, IAC, SEND, IS]
TELNET_OPT = [BINARY, ECHO, RECON, SGA, TTYPE, NAWS, LINEMO]

# http://www.ma.utexas.edu/cgi-bin/man-cgi?kill+1	
def signal_handler(signal, frame):
	global terminate
	print 'DEBUG: Signal handler called with signal', signal
	if signal == 1:
		print 'DEBUG: SIGHUP catched, closing socket'
		try:
			sc.close()
		except:
			print 'DEBUG: socket already closed'
	elif signal == 2:
		terminate = True
		print 'DEBUG: SIGINT catched (CTRL+C), closing socket and process'
		p.kill()
		try:
			sc.close()
		except:
			print 'DEBUG: socket already closed'
	elif signal == 15:
		terminate = True
		print 'DEBUG: SIGTERM catched, closing socket and process'
		p.kill()
		try:
			sc.close()
		except:
			print 'DEBUG: socket already closed'

def isTelnetCmd(rcv):
	if any(rcv in cmd for cmd in TELNET_CMD):
		print 'DEBUG: telnet command received'
		return True
	if any(rcv in opt for opt in TELNET_OPT):
		print 'DEBUG: telnet option received'
		return True
	return False

def manageTelentCmd(rcv):
	global SE, NOP, DATMK, BREAK, IP, AO, AYT, EC, EL, GA, SB, WILL, WONT, DO, DONT, IAC, SEND, IS, BINARY, ECHO, RECON, SGA, TTYPE, NAWS, LINEMO
	if rcv == SE: print 'DEBUG: telnet SE received'
	if rcv == NOP: print 'DEBUG: telnet NOP received'
	if rcv == DATMK: print 'DEBUG: telnet DATMK received'
	if rcv == BREAK: print 'DEBUG: telnet BREAK received'
	if rcv == IP: print 'DEBUG: telnet IP received'
	if rcv == AO: print 'DEBUG: telnet AO received'
	if rcv == AYT: print 'DEBUG: telnet AYT received'
	if rcv == EC: print 'DEBUG: telnet EC received'
	if rcv == EL: print 'DEBUG: telnet EL received'
	if rcv == GA: print 'DEBUG: telnet GA received'
	if rcv == SB: print 'DEBUG: telnet SB received'
	if rcv == WILL: print 'DEBUG: telnet WILL received'
	if rcv == WONT: print 'DEBUG: telnet WONT received'
	if rcv == DO: print 'DEBUG: telnet DO received'
	if rcv == DONT: print 'DEBUG: telnet DONT received'
	if rcv == IAC: print 'DEBUG: telnet IAC received'
	if rcv == SEND: print 'DEBUG: telnet SEND received'
	if rcv == IS: print 'DEBUG: telnet IS received'
	if rcv == BINARY: print 'DEBUG: telnet BINARY received'
	if rcv == ECHO: print 'DEBUG: telnet ECHO received'
	if rcv == RECON: print 'DEBUG: telnet RECON received'
	if rcv == SGA: print 'DEBUG: telnet SGA received'
	if rcv == TTYPE: print 'DEBUG: telnet TTYPE received'
	if rcv == NAWS: print 'DEBUG: telnet NAWS received'
	if rcv == LINEMO: print 'DEBUG: telnet LINEMO received'

def main(argv):
	global bin, bin_args, port, xtitle
	bin_args = ' '.join(sys.argv)[' '.join(sys.argv).find('--')+3:]
	try:
		opts, args = getopt.getopt(argv, ':vm:p:t:')
	except getopt.GetoptError as err:
		print 'Usage: %s -m <image name> -p <port number> -t <xterm title> -- [iou options] <router ID>' % sys.argv[0]
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-v':
			print "version 0.1"
			sys.exit(0)
		elif opt in ('-m'):
			bin = arg
		elif opt in ('-p'):
			port = int(arg)
		elif opt in ('-t'):
			xtitle = arg
	# if BIN OR PORT ARE NOT SETTED THEN USAGE()
	# BIN must be executable


if __name__ == "__main__":
	main(sys.argv[1:])
	cmd = bin + ' ' + bin_args
	print 'Starting %s on port %d with title %s' % (cmd, port, xtitle)
	p = subprocess.Popen(cmd.split(' '), bufsize=0, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	

	#time.sleep(1) # need to fix, it takes a long time to start
	
	#if p.poll() == None:
	#	print 'DEBUG: process is active'	
	#else:
	#	print 'DEBUG: cannot start process'
	#	sys.exit(1)

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(('', port))
	s.listen(4)
	sc = None

	signal.signal(signal.SIGHUP, signal_handler)
	signal.signal(signal.SIGINT, signal_handler)
	signal.signal(signal.SIGTERM, signal_handler)

	while (p.poll() == None) and (terminate == False):
		print 'DEBUG: looking for a client'
		if p.poll() == None: print 'DEBUG: process is active'
		try:
			sc, address = s.accept()
			print 'DEBUG: %s:%s connected.' % address
			if p.poll() == None: print 'DEBUG: process is active'
			sc.send('\33]0;%s\a' % xtitle)
			sc.send('Welcome to the Terminal Server, %s:%s.\n' % address)
			sc.send(IAC + WILL + ECHO)
			sc.send(IAC + WILL + SGA)
			sc.send(IAC + WILL + BINARY)
			sc.send(IAC + DO   + BINARY)
			client_active = True
		except:
			print 'DEBUG: failed to connect'
			if p.poll() == None: print 'DEBUG: process is active'
			client_active = False

		while client_active == True:
			try:
				data = select.select([p.stdout.fileno(), sc], [], [])
			except:
				print 'DEBUG: cannot use select.select'
				if p.poll() == None: print 'DEBUG: process is active'
				client_active == False
			for fd in data[0]:
				# Read from process
				if fd == p.stdout.fileno():
					p_stdout = p.stdout.read(1)
					#print 'DEBUG: output from process' + p_stdout
					try:
						sc.send(p_stdout)
					except:
						client_active = False
						print 'DEBUG: client no more active while sending'
				# Read from client
				if fd == sc:
					try:
						c_stdin = sc.recv(1)
						if c_stdin == '':
							client_active = False
							print 'DEBUG: client no more active while recv = null'
						else:
							#if isTelnetCmd(c_stdin): # Need to fix: CTRL+A == ECHO/SEND
							#	manageTelentCmd(c_stdin)
							#else:
							#print 'DEBUG: input from client' + c_stdin
							p.stdin.write(c_stdin)
					except:
						client_active = False
						print 'DEBUG: client no more active while receiving'

		try:
			print 'DEBUG: %s:%s disconnected.' % address
			if p.poll() == None: print 'DEBUG: process is active'
			sc.close()
		except:
			print 'DEBUG: socket closed'
			if p.poll() == None: print 'DEBUG: process is active'
