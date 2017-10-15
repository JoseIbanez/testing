#!/bin/bash


wget https://osm-download.etsi.org/ftp/osm-2.0-two/install_from_source.sh
chmod +x install_from_source.sh
#./install_from_source.sh -b tags/v2.0.2


wget https://osm-download.etsi.org/ftp/osm-2.0-two/install_osm.sh
chmod +x install_osm.sh
./install_osm.sh -b tags/v2.0.2
