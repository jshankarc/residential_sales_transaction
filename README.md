# Residential Sales Transaction - ETL Process Using Python

## Introduction

The project aim is to develop an END-to-End ETL process. The resulting data will used to apply machine learning models.

## Data Source

[PSRA](https://www.propertypriceregister.ie/) - Property Services Regulatory Authority

    ├── extract                              
    └────── extract.py                       
    ├── transform                       
    ├────── tranform_handler.py         
    └────── transform.py                
    ├── load                            
    └────── load.py                     
    ├── aws_handler                         
    └────── aws_notification_handler.py 
    └────── aws_s3_handler.py           
    ├── schedule_handler                
    └────── safe_schedule.py            
    └────── scheduler.py                
    ├── static                          
    └──────  css                            
    └────── js                          
    └────── vendor                          
    ├── templates                       
    └────── base.html                      
    └────── index.html                  
    ├── route.py                            
    ├── configuration.py                
    ├── exception.py                    
    ├── logconfig.py                    
    ├── Dockerfile                      
    ├── requirements.txt                    
    └── README.md      

Other directories are pytest, output, logs

## Technologies

- Python
- Flask
- AWS - S3, SNS
- Docker
- VSCode Editor
- Postman - Simulation
- Jupyter Notebook

## Requirements

- boto3
- Flask
- Docker
- pandas

## Tasks

- [x] Project Structure
- [x] Project Configuration
- [x] Logging Configuration
- [x] AWS Transaction Handler
- [ ] Global Exception Handler
- [x] Extract
- [x] Transform
- [x] Load
- [x] Containerization - DOCKER
- [x] EC2 Deployment using Docker
- [x] S3 Bucket Event Listener
- [ ] Enable SNS HTTP endpoint
- [ ] CI/CD Pipeline
- [ ] Documentation using Sphinx

## References

[Docker - Youtube - Channel: *SelfTuts*](https://www.youtube.com/watch?v=prlixoDIfrc&ab_channel=SelfTuts)

[Docker - AWS Container](https://medium.com/@niklongstone/how-to-build-an-aws-lambda-function-with-python-3-7-the-right-way-21888e2edbe8)

[Flask (HTML Template) - Youtube - Channel: *freeCodeCamp.org*](https://www.youtube.com/watch?v=Z1RJmh_OqeA&ab_channel=freeCodeCamp.org)

[Web Form Template Design - *Colorlib*](https://colorlib.com)

### NOTE: Object Oriented Programming best practices are not followed instead some of the JAVA project design principle are implemented
