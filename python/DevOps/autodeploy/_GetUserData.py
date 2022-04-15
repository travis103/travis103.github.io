#coding=utf-8  
def GetUserData(aSName):
    if aSName.startswith('Pre-Joboffline'):
        userData = """#!/bin/bash
sed -i 's/.*\(conflist.51onion.cn\)/10.20.21.87    conflist.51onion.cn/' /etc/hosts
sed -i 's/.*\(confinfo.51onion.cn\)/10.20.21.87    confinfo.51onion.cn/' /etc/hosts
NAME=`hostname`
sed -i "1s/$/& $NAME/g" /etc/hosts
sed -i 's/UTC/\/usr\/share\/zoneinfo\/Asia\/Chongqing/' /etc/sysconfig/clock
ln -sf /usr/share/zoneinfo/Asia/Chongqing /etc/localtime
mkdir -p /public/logs/
mkdir -p /public/pdf/pdf/
mkdir -p /public/pdf/html/
export AWS_ACCESS_KEY_ID=AKIAPSQQP76JXA7M6LVQ
export AWS_SECRET_ACCESS_KEY=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
export AWS_DEFAULT_REGION=cn-north-1
source /etc/profile
mkdir -p /data/appdatas/cat/
aws s3 cp s3://deployingfiles/pre/pre.client.xml /data/appdatas/cat/client.xml
aws s3 cp s3://deployingfiles/pre/precredentials /public/credentials
aws s3 cp s3://deployingfiles/pre/pre_id_rsa /public/id_rsa
aws s3 sync s3://deployingfiles/pre/TProfiler-1.0 /public/TProfiler-1.0
aws s3 sync s3://deployingfiles/pre/btrace-bin-1.3.8.3 /public/btrace-bin-1.3.8.3
chmod 400 /public/id_rsa
chmod 400 /public/credentials
sed -i -e 's/<dubbo:registry address=\".*\"/<dubbo:registry address=\"zookeeper:\/\/10.20.37.5\:2181\?backup\=10.20.37.6\:2181,10.20.37.7\:2181\"/g' /home/apache-tomcat-7.0.59/webapps/ala-jobs-tasks/WEB-INF/classes/config/biz-dubbo.xml
aws s3 cp s3://deployingfiles/pre/job-log4j.properties /home/apache-tomcat-7.0.59/webapps/ala-jobs-tasks/WEB-INF/classes/log4j.properties
#=======================================================================joboffline
webDir="/home/apache-tomcat-7.0.59/webapps/ala-jobs-tasks/WEB-INF/web.xml"
systemDir="/home/apache-tomcat-7.0.59/webapps/ala-jobs-tasks/WEB-INF/classes/system.properties"
#获得需要更新的文件列表
getFileNames=($(aws s3 ls s3://deployingfiles/pre/jobofflinefiles/ | awk '{if($3!="0") print $4}'))
for((i=0;i<${#getFileNames[@]};i++))
do
        if [ "${getFileNames[$i]}" = "web.xml" ]
        then
                aws s3 cp s3://deployingfiles/pre/jobofflinefiles/${getFileNames[$i]} $webDir
        elif [ "${getFileNames[$i]}" = "system.properties" ]
        then
                aws s3 cp s3://deployingfiles/pre/jobofflinefiles/${getFileNames[$i]} $systemDir
        fi
done
rm -rf /home/apache-tomcat-7.0.59/logs/*
rm -rf /public/logs/*
aws s3 cp s3://deployingfiles/pre/jobofflinefiles/catalina.sh /home/apache-tomcat-7.0.59/bin/catalina.sh
chmod 700 /home/apache-tomcat-7.0.59/bin/*
#===============================================在SoA启动后启动
#
useradd tomcat -s /home/apache-tomcat-7.0.59/bin/startup.sh
chown -R tomcat /public
chown -R tomcat /home/apache-tomcat-7.0.59
chgrp -R tomcat /home/apache-tomcat-7.0.59
#
/home/apache-tomcat-7.0.59/bin/startup.sh
"""
    elif aSName.startswith('Pre-'):
        userData = """#!/bin/bash
#===============================================================================================RoP,SoA,PMS,3rdParty公用部分
sed -i 's/.*\(conflist.51onion.cn\)/10.20.21.87    conflist.51onion.cn/' /etc/hosts
sed -i 's/.*\(confinfo.51onion.cn\)/10.20.21.87    confinfo.51onion.cn/' /etc/hosts
NAME=`hostname`
sed -i "1s/$/& $NAME/g" /etc/hosts
sed -i 's/UTC/\/usr\/share\/zoneinfo\/Asia\/Chongqing/' /etc/sysconfig/clock
ln -sf /usr/share/zoneinfo/Asia/Chongqing /etc/localtime
mkdir -p /public/logs/
mkdir -p /public/pdf/
export AWS_ACCESS_KEY_ID=AKIAPSQQP76JXA7M6LVQ
export AWS_SECRET_ACCESS_KEY=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
export AWS_DEFAULT_REGION=cn-north-1
source /etc/profile
mkdir -p /data/appdatas/cat/
aws s3 cp s3://deployingfiles/pre/pre.client.xml /data/appdatas/cat/client.xml
rm -rf /home/ala/WEB-INF/jettyBin/*
aws s3 cp s3://deployingfiles/pre/precredentials /public/credentials
aws s3 cp s3://deployingfiles/pre/pre_id_rsa /public/id_rsa
aws s3 sync s3://deployingfiles/pre/TProfiler-1.0 /public/TProfiler-1.0
aws s3 sync s3://deployingfiles/pre/btrace-bin-1.3.8.3 /public/btrace-bin-1.3.8.3
chmod 400 /public/credentials
chmod 400 /public/id_rsa
aws s3 sync s3://deployingfiles/pre/jettyBin /home/ala/WEB-INF/jettyBin
chmod 700 -R /home/ala/WEB-INF/jettyBin
rm -rf /public/logs/*
rm -rf /home/apache-tomcat-7.0.59/logs/*
#==========================================顺序启动SoA-Job优先
instanceNum=`hostname | cut -d \- -f 4`
if [ 0 -le $instanceNum ] && [ $instanceNum -le 3 ]
then
        instanceType="RoP";
elif [ 4 -le $instanceNum ] && [ $instanceNum -le 7 ]
then
        instanceType="SoA";
elif [ 12 -le $instanceNum ] && [ $instanceNum -le 15 ]
then
        instanceType="PMS";
elif [ 16 -le $instanceNum ] && [ $instanceNum -le 19 ]
then
        instanceType="3rdParty";
fi
#==========================================SoA获得弹性IP
if [ $instanceType = "SoA" ]
then
    oriIPAddress=(54.223.89.159)
    #获得当前实例ID
    instanceID=`curl -s http://169.254.169.254/latest/meta-data/instance-id`
    #获得尚未分配的弹性IP
    getIPAddress=($(aws ec2 describe-addresses --output text|awk '{if($3=="vpc") print $4}'))
    for((i=0;i<=${#getIPAddress[@]};i++))
    do
            for((j=0;j<=${#oriIPAddress[@]};j++))
            do
                    if [ "${oriIPAddress[$j]}" == "${getIPAddress[$i]}" ]
                    then
                            aws ec2 associate-address --public-ip ${getIPAddress[$i]} --instance-id $instanceID
                            break;
                    fi
            done
    done
    aws s3 cp s3://deployingfiles/pre/soa-log4j.properties /home/apache-tomcat-7.0.59/webapps/ala-service-container/WEB-INF/classes/log4j.properties
    sed -i 's/deploy.env=test/deploy.env=stage/' /home/apache-tomcat-7.0.59/webapps/ala-service-container/WEB-INF/classes/system.properties
    aws s3 cp s3://deployingfiles/pre/jobofflinefiles/catalina.sh /home/apache-tomcat-7.0.59/bin/catalina.sh
    chmod 700 /home/apache-tomcat-7.0.59/bin/*
    #
    useradd tomcat -s /home/apache-tomcat-7.0.59/bin/startup.sh
    chown -R tomcat /public
    chown -R tomcat /home/apache-tomcat-7.0.59
    chgrp -R tomcat /home/apache-tomcat-7.0.59
    #
    /home/apache-tomcat-7.0.59/bin/startup.sh
#===========================================RoP、PMS和3rdParty在Job启动后启动
elif [ $instanceType = "PMS" ]
then
    rm -f /home/bi/WEB-INF/classes/log4j.properties
    rm -f /home/ala/WEB-INF/classes/log4j.properties
    aws s3 cp s3://deployingfiles/pre/bi-log4j.properties /home/bi/WEB-INF/classes/log4j.properties
    aws s3 cp s3://deployingfiles/pre/pms-log4j.properties /home/ala/WEB-INF/classes/log4j.properties
    rm -rf /home/bi/WEB-INF/jettyBin/*
    aws s3 sync s3://deployingfiles/pre/jettyBin /home/bi/WEB-INF/jettyBin
    chmod 700 -R /home/bi/WEB-INF/jettyBin
    #
    useradd tomcat -s /home/bi/WEB-INF/jettyBin/start.sh
    useradd tomcat -s /home/ala/WEB-INF/jettyBin/start.sh
    chown -R tomcat /public
    chown -R tomcat /home/ala
    chgrp -R tomcat /home/ala
    #
    /home/bi/WEB-INF/jettyBin/start.sh stage
    /home/ala/WEB-INF/jettyBin/start.sh stage
#===========================================3rdParty
elif [ $instanceType = "3rdParty" ]
then
    aws s3 cp s3://deployingfiles/pre/3rd-log4j.properties /home/ala/WEB-INF/classes/log4j.properties
    #
    useradd tomcat -s /home/ala/WEB-INF/jettyBin/start.sh
    chown -R tomcat /public
    chown -R tomcat /home/ala
    chgrp -R tomcat /home/ala
    #
    /home/ala/WEB-INF/jettyBin/start.sh stage
#===========================================RoP官网部署，间隔时间1分钟
elif [ $instanceType = "RoP" ]
then
    aws s3 cp s3://deployingfiles/pre/rop-log4j.properties /home/ala/WEB-INF/classes/log4j.properties
    yum -y install nginx
    aws s3 cp s3://deployingfiles/pre/nginx.conf /etc/nginx/
    aws s3 cp s3://deployingfiles/pre/appm.51onion.com.conf /etc/nginx/
    service nginx restart

    #
    useradd tomcat -s /home/ala/WEB-INF/jettyBin/start.sh
    chown -R tomcat /public
    chown -R tomcat /home/ala
    chgrp -R tomcat /home/ala
    #
    /home/ala/WEB-INF/jettyBin/start.sh stage
    while [ 1 -eq 1 ]
    do
        aws s3 sync s3://webfront/pre-env/tomcat7-1888 /home/ec2-user/tomcat7-1888 --exact-timestamps
        sleep 60s
    done
fi
                """
    elif aSName.startswith('Prod-Joboffline'):
        userData = """#!/bin/bash
sed -i 's/.*\(conflist.51onion.cn\)//' /etc/hosts
sed -i 's/.*\(confinfo.51onion.cn\)//' /etc/hosts
NAME=`hostname`
sed -i "1s/$/& $NAME/g" /etc/hosts
sed -i 's/UTC/\/usr\/share\/zoneinfo\/Asia\/Chongqing/' /etc/sysconfig/clock
ln -sf /usr/share/zoneinfo/Asia/Chongqing /etc/localtime
mkdir -p /public/logs/
export AWS_ACCESS_KEY_ID=AKIAO3WNN5G4IX5AUL3A
export AWS_SECRET_ACCESS_KEY=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
export AWS_DEFAULT_REGION=cn-north-1
source /etc/profile
mkdir -p /data/appdatas/cat/
aws s3 cp s3://deployingfiles/prod/prod.client.xml /data/appdatas/cat/client.xml
aws s3 cp s3://deployingfiles/prod/prodcredentials /public/credentials
aws s3 cp s3://deployingfiles/prod/prod_id_rsa /public/id_rsa
chmod 400 /public/credentials
chmod 400 /public/id_rsa
sed -i 's/10.20.254.100/10.30.254.100/' /home/apache-tomcat-7.0.59/webapps/ala-jobs-tasks/WEB-INF/classes/log4j.properties
sed -i 's/10.20.37.5:2181?backup=10.20.37.6:2181,10.20.37.7:2181/10.30.36.5:2181?backup=10.30.38.6:2181,10.30.36.7:2181,10.30.38.8:2181/' /home/apache-tomcat-7.0.59/webapps/ala-jobs-tasks/WEB-INF/classes/config/biz-dubbo.xml
sed -i 's/stage/prod/' /home/apache-tomcat-7.0.59/webapps/ala-jobs-tasks/WEB-INF/classes/system.properties
#=======================================================================joboffline
oriIPAddress=(54.223.148.25 54.223.153.76 54.223.179.228 54.223.177.13 54.223.181.48 54.223.188.243 54.223.147.156 54.223.177.190 54.223.221.160 54.223.232.138 54.223.233.190 54.223.238.211 54.223.231.83)
#获得当前实例ID
instanceID=`curl -s http://169.254.169.254/latest/meta-data/instance-id`
#获得尚未分配的弹性IP
getIPAddress=($(aws ec2 describe-addresses --output text|awk '{if($3=="vpc") print $4}'))
for((i=0;i<=${#getIPAddress[@]};i++))
do
        for((j=0;j<=${#oriIPAddress[@]};j++))
        do
                if [ "${oriIPAddress[$j]}" == "${getIPAddress[$i]}" ]
                then
                         while [ 1 -eq 1 ]
                        do
                            checkResult=`aws ec2 describe-addresses --output text|grep $instanceID|wc -l`
                            if [ $checkResult = 0 ]
                            then
                                aws ec2 associate-address --public-ip ${getIPAddress[$i]} --instance-id $instanceID
                            else
                                break;
                            fi
                        done
                fi
        done
done
rm -rf /home/apache-tomcat-7.0.59/logs/*
rm -rf /public/logs/*
chmod 700 /home/apache-tomcat-7.0.59/bin/*
/home/apache-tomcat-7.0.59/bin/startup.sh
            """
    elif aSName.startswith('Prod-'):
        userData = """#!/bin/bash
sed -i 's/.*\(conflist.51onion.cn\)//' /etc/hosts
sed -i 's/.*\(confinfo.51onion.cn\)//' /etc/hosts
NAME=`hostname`
sed -i "1s/$/& $NAME/g" /etc/hosts
sed -i 's/UTC/\/usr\/share\/zoneinfo\/Asia\/Chongqing/' /etc/sysconfig/clock
ln -sf /usr/share/zoneinfo/Asia/Chongqing /etc/localtime
sed -i 's/10.20.254.100/10.30.254.100/' /home/ala/WEB-INF/classes/log4j.properties
mkdir -p /public/logs/
export AWS_ACCESS_KEY_ID=AKIAO3WNN5G4IX5AUL3A
export AWS_SECRET_ACCESS_KEY=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
export AWS_DEFAULT_REGION=cn-north-1
source /etc/profile
mkdir -p /data/appdatas/cat/
aws s3 cp s3://deployingfiles/prod/prod.client.xml /data/appdatas/cat/client.xml
aws s3 cp s3://deployingfiles/prod/prodcredentials /public/credentials
aws s3 cp s3://deployingfiles/prod/prod_id_rsa /public/id_rsa
chmod 400 /public/credentials
chmod 400 /public/id_rsa
rm -rf /home/ala/WEB-INF/jettyBin/*
aws s3 sync s3://deployingfiles/prod/jettyBinProd/jettyBin /home/ala/WEB-INF/jettyBin
chmod 700 -R /home/ala/WEB-INF/jettyBin
rm -rf /public/logs/*
rm -rf /home/apache-tomcat-7.0.59/logs/*
#获得当前实例ID
instanceID=`curl -s http://169.254.169.254/latest/meta-data/instance-id`
#==========================================顺序启动SoA-Job优先
instanceNum=`hostname | cut -d \- -f 4`
if [ 0 -le $instanceNum ] && [ $instanceNum -le 3 ]
then
        instanceType="RoP";
elif [ 4 -le $instanceNum ] && [ $instanceNum -le 7 ]
then
        instanceType="SoA";
elif [ 12 -le $instanceNum ] && [ $instanceNum -le 15 ]
then
        instanceType="PMS";
elif [ 16 -le $instanceNum ] && [ $instanceNum -le 19 ]
then
        instanceType="3rdParty";
fi
#==========================================SoA获得弹性IP
if [ $instanceType = "SoA" ]
then
    oriIPAddress=(54.223.148.25 54.223.153.76 54.223.179.228 54.223.177.13 54.223.181.48 54.223.188.243 54.223.147.156 54.223.177.190 54.223.221.160 54.223.232.138 54.223.233.190 54.223.238.211 54.223.231.83)    
    #获得尚未分配的弹性IP
    getIPAddress=($(aws ec2 describe-addresses --output text|awk '{if($3=="vpc") print $4}'))
    for((i=0;i<=${#getIPAddress[@]};i++))
    do
            for((j=0;j<=${#oriIPAddress[@]};j++))
            do
                    if [ "${oriIPAddress[$j]}" == "${getIPAddress[$i]}" ]
                    then
                        while [ 1 -eq 1 ]
                        do
                            checkResult=`aws ec2 describe-addresses --output text|grep $instanceID|wc -l`
                            if [ $checkResult = 0 ]
                            then
                                aws ec2 associate-address --public-ip ${getIPAddress[$i]} --instance-id $instanceID
                            else
                                break;
                            fi
                        done
                    fi
            done
    done
    rm -rf /home/apache-tomcat-7.0.59/logs/*
    sed -i 's/10.20.254.100/10.30.254.100/' /home/apache-tomcat-7.0.59/webapps/ala-service-container/WEB-INF/classes/log4j.properties
    sed -i 's/deploy.env=stage/deploy.env=prod/' /home/apache-tomcat-7.0.59/webapps/ala-service-container/WEB-INF/classes/system.properties
    rm -rf /public/qianhai_cer/*
    aws s3 sync s3://deployingfiles/prod/qianhai_cer /public/qianhai_cer
    chmod 700 -R /home/apache-tomcat-7.0.59/bin/*
    /home/apache-tomcat-7.0.59/bin/startup.sh
#===========================================RoP、PMS和3rdParty在Job启动后启动
elif [ $instanceType = "3rdParty" ]
then
    /home/ala/WEB-INF/jettyBin/start.sh prod
#===========================================PMS在Job启动后启动，添加固定IP
elif [ $instanceType = "PMS" ]
then
    aws ec2 associate-address --public-ip 54.223.249.248 --instance-id $instanceID
    aws s3 cp s3://deployingfiles/prod/prod_id_rsa /public/id_rsa
    sed -i 's/10.20.254.100/10.30.254.100/' /home/bi/WEB-INF/classes/log4j.properties
    rm -rf /home/bi/WEB-INF/jettyBin/*
    aws s3 sync s3://deployingfiles/pre/jettyBin /home/bi/WEB-INF/jettyBin #程序需要较小的内存，所以拿预发布的配置
    chmod 700 -R /home/bi/WEB-INF/jettyBin
    /home/bi/WEB-INF/jettyBin/start.sh prod
    /home/ala/WEB-INF/jettyBin/start.sh prod
#===========================================RoP官网部署，间隔时间1分钟
elif [ $instanceType = "RoP" ]
then
    aws s3 sync s3://webfront/tomcat7-1888 /home/ec2-user/tomcat7-1888
    aws s3 cp s3://deployingfiles/prod/nginxdeploy/nginx.conf /etc/nginx/
    aws s3 cp s3://deployingfiles/prod/nginxdeploy/m.51onion.com.conf /etc/nginx/
    service nginx restart
    /home/ala/WEB-INF/jettyBin/start.sh prod
    while [ 1 -eq 1 ]
    do
        aws s3 sync s3://webfront/tomcat7-1888 /home/ec2-user/tomcat7-1888 --exact-timestamps
        sleep 60s
    done
fi
            """
    return userData
