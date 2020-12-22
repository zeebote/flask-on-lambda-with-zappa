# flask-on-lambda-with-zappa
Deploy Flask app to AWS Lambda with Zappa <br>
**Requirements:**
1. AWS account with access key to your AWS Lamdba - You can use an existing account or create a new one with AWS IAM console then go to manage access key and generate a new key. This account must have IAM role which have necessary AWS permissions to automatically manage a Zappa execution role. For detail how to create minimum Zappa excercution role, please follwow this [link](https://github.com/Miserlou/Zappa#custom-aws-iam-roles-and-policies-for-deployment)
1. Docker which is used as mimic Lambda environment for setting up Zappa and our app requirements, for detail of how to install Docker, please follow this [link](https://docs.docker.com/get-docker/)
1. Flask app - We will use the same flaskr app from this [repo](https://github.com/zeebote/flask-uwsgi-nginx-postgres-on-K8)
1. Postgres DB - In this setup, we will use AWS RDS Database for our Flaskr app, for information how to create DB on AWS RDS, please follow this [link](https://aws.amazon.com/getting-started/tutorials/create-connect-postgresql-db/). Please note the URL, DB instance identify, subnet id, security group access id, db user and db password. We will need these information for our app connect to the DB.   

**How to use**
1. Setup working virtual environment - Create workspace folder and clone the repo
   ```
   mkdir workspace && cd workspace
   git clone https://github.com/zeebote/flask-on-lambda-with-zappa .
   docker run -ti -v $(pwd):/var/task --rm lambci/lambda:build-python3.6 /bin/bash
   python3 -m venv venv 
   source venv/bin/activate
   pip install -r requirements.txt
   ```
   
1. Configure AWS credential: 
   Invoke credential configuration with AWS CLI and follow on screen instruction enter aws_access_key_id, aws_secret_access_key, region, output (json)
   ```
   aws configure
   AWS Access Key ID [None]:Your AWS Access Key
   AWS Secret Access Key [None]: Your AWS Secret Access Key 
   Default region name [None]: us-east-1
   Default output format [None]: json
   ```
1. Initilize Zappa and prepair for deployment
   `zappa init`
   Keep everything as default to finish the init as we will update zappa_settings.json per your environment settings:
   ```
   {
    "dev": {
        "app_function": "zappa_init.app",              # We need this as zappa does not recognize create_app
        "aws_region": "us-west-1",                     # Update with your region
        "profile_name": "default",
        "project_name": "flask",
        "runtime": "python3.6",
        "s3_bucket": "s3-lambda"                       # Update with your s3 bucket
        "vpc_config" : {
            "SubnetIds": [ "subnet-0d8e4578b" ],       # This is the subnet ID of RDS database 
            "SecurityGroupIds": [ "sg-246d23456" ].    # This is the security group id to access your RDS database
        }
    }
   }
   ```
1. Adding enviroment variables which are use in our Flaskr app by create a .env file then add following information
   ```
   SECRET_KEY=ds9f7sdf0s809df80s98nadf7iopfv  # This your app secret key
   FLASK_APP=flaskr                           # Flask app
   FLASK_ENV=development                      # Default is development, change to production if needed
   DATABASE_URL=postgres://db_user:db_password@url_to_aws_rds_database:5432/    # Update with the info noted when create the RDS database.
   ```
1. Deploy the app
   `zappa deploy dev`
   If everything setup correctly, you should see the Url to access your app at Lambda
   ```
   Deploying API Gateway..
   Scheduling..
   Unscheduled flask-dev-zappa-keep-warm-handler.keep_warm_callback.
   Scheduled flask-dev-zappa-keep-warm-handler.keep_warm_callback with expression rate(4 minutes)!
   Your updated Zappa deployment is live!: https://q293457687.execute-api.us-west-1.amazonaws.com/dev
   ```
   Open deployment url above with your browser, you should see your app runnning. 
   

   
   
