# Milestone 3:  Data Storage and Kafka connects
## Objective:
* Get familiar with Docker images and containers.
* Deploy Tabular and key-Value data storage using GKE.
* Get familiar with Key-Value data storage
* Get familiar with Kafka Connects and their configuration.
## Repository:
[https://github.com/GeorgeDaoud3/SOFE4630U-MS3](https://github.com/GeorgeDaoud3/SOFE4630U-MS3)
## Docker and Kubernetes:
1. Watch The following video to understand [Docker](https://youtu.be/rOTqprHv1YE) terminologies.
2. To manage Docker images and applications, we will use Kubernetes, watch the following  video to get familiar with [Kubernetes and its components](https://youtu.be/cC46cg5FFAM).
3. To setup Google Kubernetes Engine (GKE). Open the console within your Google Cloud Platform (GCP) project.
   1. Set the default compute zone to **northamerica-northeast1-b** 
   ```cmd
   gcloud config set compute/zone northamerica-northeast1-b  
   ```
   2. Enable GKE by searching for **Kubernetes Engine**, select **Kubernetes Engine API**, click **Enable**. 
   
   ![MS3 figure1](figures/cl3-1.jpg)
   
   3. Wait until the API is enabled then, create a three-nodes cluster on GKE called **sofe4630u**. 
   ```cmd
   gcloud container clusters create sofe4630u --num-nodes=3 
   ```
   **Note**: if the authorization windows popped up, click Authorize 
   **Note**: if you got an error that there is no available resources to create the nodes, you may need to change the default compute zone (e.g. to **us-central1-a**) 
## Deploy MySQL using GKE:
1. To deploy a pre-existed MySQL image over the GKE cluster, we will use a YAML file. A YAML file is a file containing the configuration used to set the deployment
   1. Clone the gitGub repository
   ```cmd 
   cd ~
   git clone https://github.com/GeorgeDaoud3/SOFE4630U-MS3.git
   ```
   2. run the following command to deploy the mysql 
   ```cmd 
   cd ~/SOFE4630U-MS3/mySQL
   kubectl create -f mysql-deploy.yaml
   ```
   The command will deploy the template stored in the **mysql-deploy.yaml** into GKE. The file is shown in the following figure and can be interpreted as:
      * **Indentation** means nested elements
      *	**Hyphen** means an element within a list
      *	**First two lines**: indicate that the type of the yaml and its version.
      *	**Line 4**: provides a name for the deployment.
      *	**Line 6**: indicates that only a single pod will be used
      *	**Line 9**: provides the name of application that will be accessed by the pod.
      *	**Line 16**: provides the ID of the Docker image to be deployed
      *	**Lines 19-24**: define image-dependent environment variables that defines username/password (**usr/sofe4630u**) , and a schema (**Readings**).
      *	**Line 26**: defines the port number that will be used by image.
      
   ![MS3 figure2](figures/cl3-2.jpg)      
   
   3. The status of the deployment can be checked by the following command
   ```cmd 
   kubectl get deployment 
   ```
   4. While the status of pods can be accessed by the following command 
   ```cmd 
   kubectl get pods  
   ```
   check that the deployment is available and that the pod is running successfully (it may take some time until everything is settled down)
2. To give the deployment an IP address 
   1. A load Balancer service should be created using the mysql-service.yaml file from the cloned gitHub
   ```cmd 
   cd ~/SOFE4630U-MS3/mySQL
   kubectl create -f mysql-service.yaml
   ```
   The important lines in the mysql-service.yaml file are:
      * **Line 8**: the port number that will be assigned to the external IP
      * **Line 10**:  the name of application that will be targeted by the service.
     
   ![MS3 figure3](figures/cl3-3.jpg)      
   
   2. To check the status of the service, use this command 
   ```cmd 
   kubectl get service 
   ```
   
   ![MS3 figure4](figures/cl3-4.jpg)      
   
   It may take some time until the external IP address is changed from pending to a valid IP address. You may need to repeat the previous command.
3. To access the MySQL using the IP address,
   1. From the GCP console ( or any other device in which MySQL client is installed), run the following commands. Before running the command, replace the <IP-address> with the external IP obtained at the previous step. The options **-u**, **-p**, and **-h** are used to specify the **username**, **password**, and **the host IP** od the deployed server, respectively. 
   ```cmd
   mysql -uusr -psofe4630u -h<IP-address>
   ```
   2. Try to run the following SQL statements 
   ```sql
   use Readings; 
   create table meterType( ID int, type varchar(50), cost float); 
   insert into meterType values(1,'boston',100.5); 
   insert into meterType values(2,'denver',120); 
   insert into meterType values(3,'losang',155); 
   select * from meterType where cost>=110; 
   ```
   3. Exit the MySQL CLI, by running
   ```sql
   exit
   ```
   4. (**optional**) after creating a video for submission, you can delete the deployment by using the following command (**Don’t run it right now**)
   ```cmd
   kubectl delete -f mysql.yaml
   ```
