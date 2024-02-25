package main

type Peer struct {
	address string
	delay int
	capacity int
	lastUpdate int
}

type PeerList []Peer

type Frame struct {
	id int
	streamId string
	timestamp int
	data string
	jumpCounter int
}

type System struct {
	address string
	peerList []Peer
	streamId string
	stream  map[string]Frame
}

type SystemState struct {
	address string
	peerList []Peer
	streamId string
	lastFrame int
	pendingFrames []int
}



