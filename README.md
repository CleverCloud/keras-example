# Painting style transfer on photos

We aim to quickly and easly make our own favorite pictures look like a famous painter production. Hence we provide an easy way to provide some style examples and our personal pictures. It's even possible to blend styles.

> Core engine provide from https://github.com/titu1994/Neural-Style-Transfer.git and has been made by **Somshubra Majumdar**. We thank him cheerly for his great job.

## Clever Grid
### What is it ?
[Clever Grid](https://www.clevergrid.io/) is a GPU as a Service platform allowing any developer or data scientist to train their Machine Learning models seamlessly. They only have to provide the necessary code. No tidious driver configuration and dependency management is involved except the code dependencies.

### How it Works
Based on [Clever Cloud](http://clever-cloud.com/), Clever Grid provides two running modes.
1. Runner : Run a script just once. It can be used to train networks
1. Web service : Build a Web service and put it in production

> **These instances are stateless !! It means that data stored on disk cannot be saved. You need to use an add-on like Cellar instead. Cellar is Clever Cloud's S3 API compatible object storage**

These instances run the provided code.
 
Setup is done using environment variables. This is for example how you specify the starting script (in Bash or Python).

> for further information, refer to https://www.clever-cloud.com/doc/

## Painting style transfer on photos 
### Explaination
We only need a start.sh file *(which can also be a python file -> don't forget to change the starting env variable)*. Here's what we need to do:
* First we get the data source from our Cellar source bucket. They are the pictures we want to apply style on
* We get some painting we want to use as style source from Cellar
* We run Somshubra Majumdar's awesome script with the needed arguments. (It can be adjusted for better results. Ref on Somshubra Majumdar's documentation)
* We send the result back to our Cellar bucket

#### Needed Environment Variables:

1. To manage storage:

       BUCKET_RESULT
       BUCKET_SOURCE
       BUCKET_STYLE

1. To manage Cellar add-on:
   
       CELLAR_ADDON_HOST
       CELLAR_ADDON_KEY_ID
       CELLAR_ADDON_KEY_SECRET

   > These are automatically setup when an Addon is linked to an Application


> We use three additional python files to get and send data in Cellar : *bucket_management.py*, *get_bucket_content.py*, *send_to_bucket.py*

### Helpers
We provide some helpers python script based on *.env* file.
> environment variables must be the same than in the Clever Grid application
#### Helper Usage :
    python cl_get_results.py param
*param* is a destination folder where we get results from buckets

    python cl_send_source.py param
*param* is the source folder where pictures to process are stored

    python cl_get_style.py param
*param* is the style folder where painting style examples are stored

## Quick Start :

> You need the Clever Cloud CLI client. See: https://www.clever-cloud.com/doc/clever-tools/getting_started/

> If you do not have a Clever Cloud account, you can get on for free here: https://api.clever-cloud.com/v2/sessions/signup

> Steps 5 to 8 are to help you send your data into a Cellar storage object.

1. Login to your Clever Grid Account

       clever login

1. Link to your python_ml runner application

       clever link <APP_ID>

   > You need to have a *Python Runner* application in https://dashboard.clevergrid.io *(see the section : Create an application on Clever Grid)*

   > <APP_ID> can be find on the application *overview* page      

1. Add your clever grid application repository to your current git project :

       git remote add clever git+ssh://git@ppush-clevergrid-clevercloud-customers.services.clever-cloud.com/<YOUR_APP_ID>.git

    > note the <YOUR_APP_ID> field
    
1. Set the needed environment variables:

   * In the *Environment Variables* menu under our Application menu in the clever grid console

   OR

   * Whit the clever CLI (Command Line tools) :
       
         clever env set BUCKET_RESULT <BUCKET_RESULT_NAME>
         clever env set BUCKET_SOURCE <BUCKET_SOURCE_NAME>
         clever env set BUCKET_STYLE <BUCKET_STYLE_NAME>
         clever env set CC_MLPYTHON_START_SCRIPT start.sh

1. (optional) push the code to your application:

       git push clever

    > *clever* is the remote Clever Grid git repository name

1. (optional) install required packages:
    > Needed for helpers scripts

       pip intall -r requirement.txt
       
1. (optional) set up a *.env* file with the same environment variables than in the Clever Grid application
    > this step allow you to use helpers python script to send your data to Cellar

       echo "BUCKET_RESULT=<BUCKET_RESULT_NAME>" > .env
       echo "BUCKET_SOURCE=<BUCKET_SOURCE_NAME>" >>.env
       echo "BUCKET_STYLE=<BUCKET_STYLE_NAME>" >> .env

1. (optional) use helpers scripts to send your data to Cellar:

       python cl_send_source.py picture_source_folder
       python cl_send_style.py.py style_source_folder
  
1. Finally start your application with

       clever deploy

    > for all restart, use **clever restart** instead of **deploy**

1. Wait until the end (see logs into the console or in your terminal). Then get the result:

       python cl_get_results.py dest_folder
 

## Create an application on Clever Grid  
1. login to https://dashboard.clevergrid.io
1. choose your organisation
1. create an application
1. select the Python Runner and name it
1. choose your instance size and the number of nodes needed

## Issues and Limits
This is a quick usage demonstration of Clever Grid. It is not optimized and the usage of to many style source files and
pictures to treat can raise an OOM (Out Of Memory) during the execution !

