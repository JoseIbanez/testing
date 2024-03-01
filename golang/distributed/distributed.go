package main

type Peer struct {
	Address    string `json:"address"`
	Delay      int    `json:"delay"`
	Capacity   int    `json:"capacity"`
	lastUpdate int64
}
type PeerList []Peer

type Message struct {
	Command     string       `json:"cmd,omitempty"`
	PeerList    PeerList     `json:"peerList,omitempty"`
	Frame       *Frame       `json:"frame,omitempty"`
	SystemState *SystemState `json:"state,omitempty"`
	Ping        *Ping        `json:"ping,omitempty"`
}

type Frame struct {
	id          int
	streamId    string
	timestamp   int
	data        string
	jumpCounter int
}

type System struct {
	address  string
	peerList []Peer
	streamId string
	stream   map[string]Frame
}

type Ping struct {
	A_out int64 `json:"a_out"`
	B_in  int64 `json:"b_in"`
	B_out int64 `json:"c_out"`
	A_in  int64 `json:"a_in"`
}

type SystemState struct {
	Id            string `json:"id"`
	Address       string `json:"address"`
	peerList      *PeerList
	StreamId      string `json:"streamId"`
	LastFrame     int    `json:"lastFrame"`
	PendingFrames []int  `json:"pendingFrames,omitempty"`
}
