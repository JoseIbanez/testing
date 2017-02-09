# InfluxDB
#==================================
echo "Configure Additional Repo"
curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
source /etc/lsb-release
sudo add-apt-repository -y "deb https://repos.influxdata.com/${DISTRIB_ID,,} ${DISTRIB_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/influxdb.list

echo "Installing deps"
sudo apt-get update && sudo apt-get install influxdb


echo "Post configuration"


echo "Restarting"
sudo service influxdb start
