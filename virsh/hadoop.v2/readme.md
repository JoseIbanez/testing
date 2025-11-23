
# Single node

href: https://medium.com/@sattar.husnain123/hadoop-single-node-installation-on-ubuntu-d73da510b57e

ssh -V
systemctl status ssh
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys


cd ~
wget https://dlcdn.apache.org/hadoop/common/hadoop-3.4.1/hadoop-3.4.1.tar.gz
tar -xzf hadoop-3.4.1.tar.gz 
sudo mv hadoop-3.4.1 /usr/local/hadoop
sudo chown -R hadoop:hadoop /usr/local/hadoop

vim.tiny ~/.bashrc
source  ~/.bashrc 

   18  echo $JAVA_HOME
   19  hadoop version
   20  echo $HADOOP_HOME
   21  nano $HADOOP_HOME/etc/hadoop/hadoop-env.sh
   22  echo $JAVA_HOME
   23  vim $HADOOP_HOME/etc/hadoop/hadoop-env.sh
   24  ls $HADOOP_HOME/
   25  mkdir -p $HADOOP_HOME/hdfs/namenode
   26  mkdir -p $HADOOP_HOME/hdfs/datanode
   27  sudo chown -R hadoop:hadoop $HADOOP_HOME/hdfs
   28  vim $HADOOP_HOME/etc/hadoop/core-site.xml
   29  vim.tiny $HADOOP_HOME/etc/hadoop/core-site.xml
   30  vim $HADOOP_HOME/etc/hadoop/hdfs-site.xml
   31  vim.tiny $HADOOP_HOME/etc/hadoop/hdfs-site.xml
   32  vim.tiny $HADOOP_HOME/etc/hadoop/mapred-site.xml
   33  vim.tiny $HADOOP_HOME/etc/hadoop/yarn-site.xml


# format fs
   
hdfs namenode -format
ls /usr/local/hadoop/hdfs/namenode
ls -l /usr/local/hadoop/hdfs/namenode/current/

# start services

   40  start-dfs.sh 
   41  start-yarn.sh 
   42  jps


# test job
   43  exit
   44  ls
   45  cd wordcount/
   46  ls
   47  history 
   48  hadoop -ls /user/
   49  hadoop fs -ls /user/
   50  hadoop fs -ls /user/data/
   51  hadoop fs -ls /user/data/wordcount
   52  hadoop fs -ls /user/data/wordcount/output2
   53  hadoop fs -cat /user/data/wordcount/output2/_SUCCESS
   54  hadoop fs -cat /user/data/wordcount/output2/part-r-00000
   55  ls
   56  cd
   57  ls
   58  cd wordcount/
   59  ls
   60  cd ..
   61  ls
   62  history 



# With docker compose

href: https://github.com/spraharaj-projects/hadoop-environment