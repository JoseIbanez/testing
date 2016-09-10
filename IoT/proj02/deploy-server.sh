#==================================================
echo "S.O. configuration ..."

cat > /etc/default/locale << EOF
LC_ALL=en_US.UTF-8
LANG=en_US.UTF-8
EOF



#==================================================
echo "New repos ..."
apt-get update -y

#==================================================
echo "Installing pakages ..."
apt-get install -y \
        joe \
        mosquitto-clients \
        python-pip

pip install --upgrade boto3

#==================================================
echo "Installing ..."

#==================================================
echo "Configuring app ..."

#==================================================
echo "Restar app ..."
