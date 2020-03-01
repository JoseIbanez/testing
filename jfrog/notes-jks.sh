# Create new Keystore
keytool -keystore package.jks -genkey -alias _dunesrsa_alias_ -storepass 'VMware1!'

# Delete default alias
keytool -delete -alias _dunesrsa_alias_ -keystore package.jks -storepass 'VMware1!'

# Generate new Key
keytool -genkey -keyalg RSA -keysize 2048 -alias _dunesrsa_alias_ -keystore package.jks -storepass 'VMware1!' -validity 3650 -dname 'CN=CI,OU=GDC,O=VF,L=Madrid,ST=Madrid,C=ES,emailAddress=administrator@vsphere.local'

##  Optional  ##

# Generate Certificate Signing Request
keytool -certreq -alias _dunesrsa_alias_ -keypass 'VMware1!' -keystore package.jre -storepass 'VMware1!' -file packageCertRequest.csr

# Import the signed certificate
keytool -importcert -alias _dunesrsa_alias_ -keypass 'VMware1!' -file packageCertRequest.crt -keystore package.jks -storepass 'VMware1!'

# Export/Backup Certificate
keytool -exportcert -alias _dunesrsa_alias_ -keystore package.jks -storepass 'VMware1!' -file packageCertExport
