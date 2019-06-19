# Painting style transfer on photos
We aim to quickly and easly make our own favorites pictures look like a famous painter production.
Hence, we provide an easy way to provide some styles examples and our pictures. It's even possible to blend styles.

> Core engine provide from https://github.com/titu1994/Neural-Style-Transfer.git and has been made by **Somshubra Majumdar**. We thank him cheerly for his great job.

## Clever Grid platform
### What is it ?
Clever-grid is an easy to use GPU provider which aim to address issues of  the most wide kind of developers, from users to the hard coders.

### How it's Works
Based on the Clever Cloud platform. Clever Grid provide two running modes.
1. A runner : to run a script just once. It can be used for Train networks
1. Web service : To build a Web service which can be requested for any reasons

> **Theses instances are state less !! That mean that data is not saved. You need to use an add-on like Cellar (the Clever Cloud S3 like object storage)**

We lean on add-on like Cellar to keep the data.

Configuration is passed by environment variables


## Painting style transfer on photos 
### explanation
We only need a start.sh file *(which can also be a python file -> don't forget to change the starting env variable)*. Some operations are done :
* We firstly get the data source from our cellar source bucket. It's pictures we want change
* We get some painting we want uses as style source from Cellar too
* We run the amazing Somshubra Majumdar's script with wanted arguments. (It can be adjust for  better results. Ref on Somshubra Majumdar's documentation)
* We send the result on Cellar

> We use three additionally python files to get and send data in Cellar : *bucket_management.py*, *get_bucket_content.py*, *send_to_bucket.py*

### helpers
We provide some helpers python script based on *.env* file.
> environment Variables must be the same than in Clever Grid application
#### Helper usage :
    cl_get_results.py param
*param* is a destination folder where get results from buckets

    cl_send_source.py param
*param* is the source folder where pictures to process are stores

    cl_get_style.py param
*param* is the style folder where paints styles example are stores

## Quick Start :

1. Login to your Clever Grid Account

       clever login

1. link to your python_ml runner application

       clever link <APP_ID>

> You need to have a *Python Runner* application in https://dashboard.clevergrid.io *(see the section : Create an application on Clever Grid)*

> <APP_ID> can be find on the *overview* page      
1. add your clever grid application repository to you current git project :

       git remote add clever git+ssh://git@ppush-clevergrid-clevercloud-customers.services.clever-cloud.com/<YOUR_APP_ID>.git

    > note the <YOUR_APP_ID> field
    
1. Set environment variable needed :

   * From Clever Grid Console

   OR

   * Whit the clever Client :
       
         clever env set BUCKET_RESULT demo-painting-test-results
         clever env set BUCKET_SOURCE demo-painting-test-source
         clever env set BUCKET_STYLE demo-painting-style-source
         clever env set CC_MLPYTHON_START_SCRIPT start.sh

1. push the code to your application :

       git push clever

    > *clever* is the remote Clever Grid repository name prior named

1. run :

       pip intall -r requirement.txt
  
1. set up a *.env* file with the same environment variables than in the Clever Grid application

       echo "BUCKET_RESULT=demo-painting-test-results" > .env
       echo "BUCKET_SOURCE=demo-painting-test-source" >>.env
       echo "BUCKET_STYLE=demo-painting-style-source" >> .env

1. run :

       python cl_send_source.py picture_source_folder
       python cl_send_style.py.py style_source_folder
  
1. Finally start your application with

       clever deploy

    > for all restart, use **clever restart** instead of **deploy**

##Create an application on Clever Grid  
1. login in https://dashboard.clevergrid.io
1. choose your organisation
1. create an application
1. select the Python Runner and name it
1. choose your instance size the number of nodes needed

## Issues and Limits
This is a quick usage demonstration of Clever Grid. It is not optimized and the usage of to many style source files and
pictures to treat can raise an OOM (Out Of Memory) during the execution !

