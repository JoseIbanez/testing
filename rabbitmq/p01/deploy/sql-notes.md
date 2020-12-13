#
DBNAME="vc_deployments"
sudo -s -u postgres psql -v ON_ERROR_STOP=1 --dbname $DBNAME