# MLTradingApi

## installation instructions: 

### 1. Create a VPC in AWS:

steps:
  - go to amazon VPC service
  - select **create VPC**
  - select **VPC and more**
  - in Name tag - optional type the vpc name **(ml-api)**
  - in IPv4 CIDR block type **10.0.0.0/16**
  - in IPv6 CIDR block select **No IPv6 CIDR block**
  - in Number of Availability Zones (AZs) choose **1**
  - in Number of public subnets choose **1**
  - in Number of private subnets choose **2**
  - in NAT gateways choose **None**
  - VPC endpoints chose **s3 Gateway**
  - finally click in  **Create VPC**
    
### 2. Create a Nat Gateway

steps:
  - in VPC services go to VPC dashboard
  - in Virtual private network section choose **NAT gateways**
  - into Nat gateways section choose **Create NAT gateway**
  - type a name of the nat gateway **(ml-nat-gateway-01)**
  - in Subnet chose the previus public subnet created in the VPC
  - in Connectivity type choose **Public**
  - Chose **Create NAT gateway**

### 3. Create Security Groups

  ### security group to trainapi
steps:
  - go to Security section of VPC dashboard
  - select Security groups
  - select **Create** security group
  - in Security group name type **"train-sec-group"**
  - in description type **"allows TCP 8000 access"**
  - in VPC choose the previus VPC created **(ml-api)**
  - select "add-rule" in Inbound rules section
  - in **Type** choose **SSH**
  - then again select **add rule**
  - in Type choose **Custom  TCP**, and in Port range choose **8000**
  - In Destionation choose **Anywhere-IPv4**
  - finally select **Create security group**
    
  ### security group to inference api
steps:
  - do the same, but in Security group name type **"inference-sec-group"**
  - in description type **"allows TCP 8001 access"**
  - in Type choose **Custom  TCP**, and in Port range choose **8001**
  - do the same to everything else

  ### security group to Client and Plot apis
steps:
  - do the same, but in Security group name type **"client-sec-group"**
  - in description type **"allows TCP 80, 8002 access"**
  - in Type choose **Custom  TCP**, and in Port range choose **80**
  - add another rule whit the **8002** port like the above rule
  - do the same to everything else

### 4. Create an EC2 instance to trainapi
steps:
  - go to EC2 amazon service
  - in Instances section into EC2 dashboard select Launch instances
  - in Name and tags type **trainapi**
  - in Application and OS Images (Amazon Machine Image)  select **Ubuntu Server 24.04 LTS (HVM)**
  - in Instance type choose **t2.large** or higher
  - in Key pair (login) select Create a new key pair
  - in Private key file format choose **RSA**
  - in Private key file format choose **.pem**
  - select Create key pair, and save in a secure place the key.pem downloaded to access to EC2 instance through the .pem key via ssh
  - in Network settings section select **edit**
  - VPC - required select the previus vpc created (ml-api-vpc)
  - in Subnet select the previus private subnet created into ml-api-vpc **(ml-api-subnet-private-1-us-east-1a)**
  - in Auto-assign public IP select **Disable**
  - in Firewall (security groups) select **Select existing security group**
  - in Common security groups select ***train-sec-group**
  - expand **Advanced network configuration**
  - in Primary IP type **10.0.1.33**, leave the same in this section of Advanced network configuration
  - in Configure storage select section change to **1x10 GiB**
  - in Advanced details section down to User **data - optional** section and in the tex box upload the build.sh file of trainapi directory from this proyect or copy and paste the next bash code:

```
#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

# NOTE: This script is intended to be run as EC2 User Data, which executes as the 'root' user.
# Therefore, 'sudo' is not strictly necessary for the commands below, but it's kept for clarity
# and so the script can be easily adapted to run in other environments.

cd /root/

# 1. Update package lists and install dependencies
# Combined update, upgrade, and installation of all necessary packages in one go.
# Added 'git' which was missing.
apt-get update -y
apt-get upgrade -y
apt-get install -y ca-certificates curl gnupg lsb-release git

# 2. Add Docker's official GPG key and set up the repository
# This part is mostly unchanged but ensures directories exist before use.
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null

# 3. Install Docker Engine
# Update package list again to include the new Docker repo, then install.
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# The Docker service is automatically started and enabled on install with modern packages,
# but we can be explicit just in case.
systemctl start docker
systemctl enable docker

# 4. Clone the Application Repository
# Clones the project into the root user's home directory (/root/)

git clone https://github.com/andresmg42/MLTradingApi.git

cd MLTradingApi/trainapi

# Build and run the containers.
# NOTE: Using 'docker compose' (with a space) which is the command for the v2 plugin.
# The '-d' flag is CRITICAL to run the containers in detached (background) mode,
# allowing the startup script to complete.
# The 'usermod' command has been removed as it is ineffective and unnecessary here.
docker compose build
docker compose up -d
```
  - select **Launch instance**

### 5. Create an EC2 instance to inferenceapi
steps:
  - go to EC2 amazon service
  - in Instances section into EC2 dashboard select **Launch instances**
  - in Name and tags type **inference**
  - in Application and OS Images (Amazon Machine Image)  select **Ubuntu Server 24.04 LTS (HVM)**
  - in Instance type choose **t2.medium** or higher
  - in Key pair (login) select Create a new key pair or use the previus key pair created in the trainapi instance
  - in Private key file format choose **RSA**
  - in Private key file format choose **.pem**
  - select Create key pair, and save in a secure place the key.pem downloaded to access to EC2 instance through the .pem key via ssh
  - in Network settings section select **edit**
  - in **VPC - required** select the previus vpc created **(ml-api-vpc)**
  - in Subnet select the previus private subnet created into ml-api-vpc **(ml-api-subnet-private-2-us-east-1a)**
  - in Auto-assign public IP select **Disable**
  - in Firewall (security groups) select **Select existing security group**
  - in Common security groups select ***inference-sec-group**
  - expand **Advanced network configuration**
  - in Primary IP type **10.0.2.177**, leave the same in this section of Advanced network configuration
  - in Configure storage leave by default
  - in Advanced details section down to User **data - optional** section and in the tex box upload the build.sh file of inferenceapi directory from this proyect or copy and paste the previus bash code in the launch of trainapi EC2 instance but change this next two lines which are located almost at the end of the bash code to:
```
cd  MLTradingApi/inferenceapi
```
  - select **Launch instance**}

### 6. Create an EC2 instance to client
steps:
  - go to EC2 amazon service
  - in Instances section into EC2 dashboard select Launch instances
  - in Name and tags type **client**
  - in Application and OS Images (Amazon Machine Image)  select **Ubuntu Server 24.04 LTS (HVM)**
  - in Instance type choose **t2.medium** or higher
  - in Key pair (login) select Create a new key pair or use the previus key pair created in the trainapi instance
  - in Private key file format choose **RSA**
  - in Private key file format choose **.pem**
  - select Create key pair, and save in a secure place the key.pem downloaded to access to EC2 instance through the .pem key via ssh
  - in Network settings section select **edit**
  - VPC - required select the previus vpc created **(ml-api-vpc)**
  - in Subnet select the previus public subnet created into ml-api-vpc **(ml-api-subnet-public-1-us-east-1a)**
  - in Auto-assign public IP select **Disable**
  - in Firewall (security groups) select **Select existing security group**
  - in Common security groups select ***client-sec-group**
  - in Configure storage leave by default
  - in Advanced details section down to User **data - optional** section and in the tex box upload the build.sh file of inferenceapi directory from this proyect or copy and paste the previus bash code in the launch of trainapi EC2 instance but change this next two lines which are located almost at the end of the bash code to:
```
cd MLTradingApi/client-plot
```
  - select **Launch instance**

### 7. Browse to Client Interface to prove the MLTradingApi

steps:
  - go to EC2 AWS service
  - in the EC2 dashboard select instances
  - in the instances list deployed, select client
  - in **Details** section look for **Public DNS** or **Public IPv4 address**
  - copy and paste whatever previus address you want in a browser
  - Into API deployed you will see a simple form to train the model
  - in the first input choose a index of those available
  - choose a start date and end date to train the model
  - then, click in **Train Model**
  - wait a moment while the train is executed, for S&P500 it can take at least two minuts
  - then selet the ticker which you want to make the inference in the new form
  - again choose the start and end dates to make the inference
  - click in **Made Inference**, this also take any minuts
  - finally click in the new button called **Generate Gráphic**, this will show a graphic from the inference
  - to make a new train, only close the graphic and select **New Train** at the top of the form.





 
  
    
    
    
    


 

