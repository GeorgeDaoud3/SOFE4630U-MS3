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
## Deploy Redis using GKE:
1. Watch the first 7:45 minutes in the following video to get familiar with [redis commands](https://youtu.be/jgpVdJB2sKQ).  
2. Both the deployment and the service are included in the same file. To deploy the file tp GKE, run the following commads 
   ```cmd
   cd ~/SOFE4630U-MS3/Redis
   kubectl create -f redis.yaml
   ```
   Check that status of deployment, service, and pod. Note that the password is set within the yaml file to **sofe4630u**.
3.	Get Redis external IP.
   ```cmd
   kubectl get services
   ```
   ![MS3 figure5](figures/cl3-6.jpg)      
4. To access the Redis datastorage,
   1. You can install redis client on your machine as shown in the previous video. However, let’s install it over GCP console.
   ```cmd
	sudo apt-get install redis-tools
   ```
   **Note**: this installation in not persistent and you need to repeat it each time the session is ended.
   2. Know let’s log in to server using the command after replacing the **<Redis-IP>** by the IP obtained in step 3. Note that **sofe4630u** is the password used 
   ```cmd
   redis-cli -h <Redis-IP> -a sofe4630u
   ```
   3. No try to run the following commands. Note, there are 16 different databases to select within redis. The first command selects the first database (0)
   ``` cmd
   select 0
   set var 100
   get var
   keys *
   del var
   keys *
   ```
   4. Finally to exit Redis command line interface, type
   ```cmd
   exit
   ```
5. To access, redis with python, 
   1. Install its library on your local machine (or GCP console) 
   ``` cmd
   pip install redis
   ```
   2. In the cloned Github at path **/redis/code/**, there are two python files and a jpg image. 
      * **SendImage.py**, will read the image **ontarioTech.jpg** and store it in Redis associated with a key **OntarioTech** at database 0.
      * **ReceiveImage.py**, will read the value associated with the key **OntarioTech** from the Redis server and will save it into **received.jpg** image.
      * You have to set the Redis Server Ip in the second line in both SendImage.py and ReceiveImage.py.
      * Run SendImage, then check the keys in the redis server. Finally, Run ReceiveImage and check if the received.jpg image.
## Configure Kafka Connector with MySQL sink,
1. Watch the following video about [Kafka connect](https://youtu.be/YXgXw25E5RU).
2. Log in to your **Confluent Kafka account** you created in the first milestone. Make sure you are still in the trial period.
3. As described is the first milestone, create a topic and name it **Readings**. This topic will be accessed by the connector for data.
4.	Add a Schema to the topic to be used by the connector to create a table in MySQL database. The three following steps will be run only once to setrp schema registry and will not be repeated for any other schemas
   1. Select **Reading** topic, choose **schema**, click **setup Schema Registry**.
   ![MS3 figure6](figures/cl3-8.jpg)      
   2. To setup the **schema Registry**, at **Stream Governance Packages**, choose **Essentials**.
   3. Then choose **Google Cloud** as Cloud provider and **us-central1** as the Region. Then, click **Enable**
   ![MS3 figure7](figures/cl3-9.jpg)
   4. Now, the **schema Registry** is configured, go back to the topic and choose **schema** again as in step a) and choose **Set a schema**.
   ![MS3 figure8](figures/cl3-10.jpg)
   5. Choose **Avro** as the serialization format and copy the [following script](connectors/mysql/schema.txt) as the schema, then click **create**.
5. Create a MySQL source connector.
   1. Within the cluster, choose **connectors**, search for **MySQL**, and finally select **MySQL sink**
   ![MS3 figure9](figures/cl3-7.jpg)
   2. Fill the configuration as in 
      1. **Topic selection**:
         * **Topic name** : **Readings**
      2. **Kafka credentials**: use the existing API key you have created in the first Milestone
      3. **Authentication**: Enter the information of the MySQL server we already have deployed on GKE
         * **Connection host**: The MySQL IP you obtained before
         * **Connection port**: **3306**
         * **Connection user**: **usr**
         * **Connection password**: **sofe4630u**
         * **Database name**: Readings
         * **SSL mode**: **prefer**
      4. **Configuration**: (click show advance configurations)
         * **Input Kafka record value format**: **AVRO**
         * **Insert mode**: **UPSERT**
         * **Auto create table**: **true**
         * **Auto add columns**: **true**
         * **PK mode**: **record_value**
         * **PK fields**: **ID**
         * **Input Kafka record key format**: **string**
      5. **Sizing**: 
         * **Tasks**:1
      6. Review and launch: 
         * **Connector name**: **smartMeter2MySQL**
   3. It will take few minutes until the connector is running.
6. Send data to the topic from your local machine (or GCP console)
   1. Install Avro library.
   ```cmd
   pip install avro
   ```
   2. Copy the schema ID
	
   ![MS3 figure10](figures/cl3-11.jpg)
   
    3. Three files are needed found at the path
