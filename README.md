
# Effective Deduplication and selective Compression in AWS S3

Note : No  Changes or Modifications are suggested during the presentation.

Cloud Storage has become a popular pay to go service to store data in an easily accessible way. This also leverages the concerns of operational cost management, and every user strives to optimize their utilization. Our main goal is to make cloud storage more efficient and reduce operating costs of the cloud environment. The S3 Cloud storage service is improvised by Deploying effective De-duplication and selective Compression of files to improve the storage utilization thereby optimizing the operational costs to the end user.


# Website
Below webpage is hosted using Ec2 Instance.This page can be used to upload the objects directly to the s3 bucket.

www.cloudclan.cf

# Architecture Diagram
<img width="768" alt="Screenshot 2022-12-14 at 1 03 27 AM" src="https://user-images.githubusercontent.com/104820355/207529452-61497fa7-9a03-461d-8bb3-1ce75a9d3fcb.png">

# Tools Used
1. AWS S3
2. AWS Dynamodb
3. AWS Lambda
4. AWS EC2
5. AWS Event Bridge
6. Flask web framework

# Implementation

1. First a S3 bucket named “myefficientbucket” was created and made it public so that files can be uploaded to it via a web page.
2. Next a web page is created to upload files to s3 bucket. This web page is created using the “Flask” framework and was hosted in an EC2 instance.
3. Next a DynamDB table called “checkSumTable” was created to store checksum of the files uploaded to s3 bucket. This checksum is used to identify whether the uploaded file to the s3 bucket is a duplicate or not.
4. This DynamDb table has the following attributes:
    * checkSum: checksum of the file
    * fileName : name of the file
    * Compressed: whether the file is compressed or not if it is compressed it contains “yes” value otherwise “no”
    * compressedSize: size of the file after compression
    * originalSize: size of the original size
    * compressionRatio: (originalSize - compressedSize)/orginalSize
    * lambdaRuntime: time taken to compress the file
    * memorySaved: originalSize - compressedSize
    * uploadedTime: uploaded date and time of the file. This attribute will be used to compress the file.
5. A lambda function “my-s3-function” is created to handle deduplication. This lambda function was given permission to delete files from S3 bucket and also to access checksum from DynamoDB table. Whenever a file is uploaded to the S3 bucket, this function will be triggered and the checksum of that file is calculated. If that checksum is already present in the dynamodb table it means it is a duplicate file and will be deleted from the S3 bucket otherwise this new checksum is added to the dynamodb table and the file is allowed to stay in the S3 bucket.
6. To implement selective compression a new lambda function “scheduledFunction” is created. For this lambda, permissions are given to get and put objects in S3 bucket and also permission to access DynamoDB table. This lambda function is triggered periodically by Eventbridge service. Upon every trigger this function gets data from DynamoDb table to check how long the files have not been used in S3 bucket. If a file hasn't been used for more than 30 days that file will be compressed and will be stored in an archive folder. And also it will update file information in DynamoDB table like compressionRatio, memorySaved, changing compressed attribute to “Yes” etc.
7. In Event Bridge service a schedule is created to trigger “scheduledFunction” periodically.



# Dyanmo DB
Here , We are sharing the Pictures of our Dyanmo db Table used for Implementation
![1](https://user-images.githubusercontent.com/104820355/207528959-9935296b-7348-4680-b50e-9b1f3b3b8b91.jpg)
![2](https://user-images.githubusercontent.com/104820355/207529002-35abfc6c-84a5-48a0-ae82-267c313de7ca.jpg)







