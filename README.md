# Cloud-Computing-SelfieLessActs
mini project based on  Cloud on selfieless acts 

There are 5 stages of the project-
1) Cretaing a VM .
2) Writing API's.
3)Creating containers and placing the API's in two seperate containers.(acts and users).
4)Creating load balancers to routte to containers paced in two different VM's.
5)Creating an orchestrator.

# 1st Stage - Creating an VM
create a VM according to your needs in amzon aws , i used all the bassic architecture as mentioned by our mentor.

# 2nd Stage- Writing API's
first of all an API(Application Program Interface) is nothing but a URL . it's like you go to a webpage like youtube and then you click on to something which redirects you to another page . its the same we have a URL(mention by @app.route()) and what you want to do can be defined in the function below it.once you underatand how to write one API its goig to be simple.

# 3rd Stage - Creating Containers 
creating a Dockerfile is the main part. once you understand how a Dockefile is created its going to be easy. i used file systems to as my database so my dockerfile was simple if you are using a sql database you might want to refer to some youtube videos.

# 4th Stage - Creating a load balancers
i followed the tutorial mentioned by amazon aws . just follow step by step to create application load balancer.

# 5th Stage - Creating an Orchestrator
Orchestrator is something like load balancer but it manages load by increasing or decreasig the containers  which is checked by health API ,fault tolerence API and autoscaling API. 
