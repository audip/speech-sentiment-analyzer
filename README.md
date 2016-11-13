# Anti-harassment speech analyzer
SayNoToHarassment is an app that updates real-time and shows posts that are likely to contain hate speech and harassment online, integrated with streaming API of twitter for prototyping. It provides a dashboard view of flagged tweets, outlook of how audience is perceiving and posting about on social media.

## Installation
- Install package dependencies - `pip install -r requirements.txt`
- Docker run: `docker run -d --hostname localhost -p 4369:4369 -p 5672:5672 -p 15672:15672 -p 25672:25672 rabbitmq:3-management`
- Docker detach from container `ctrl-p + ctrl-q` and attach `docker attach <container-id>`

## Inspiration
Recent indiscipline in one of the non-MLH hackathons led us to re-think what would be the best way to help organizers and companies identify the negatory speech against individuals, groups, races and ethnicities. 

## How we built it
Getting inspired by Amazon web services', we built the platform with REST and Streaming API for twitter feeds, which flows into RabbitMQ cluster on EC2 container services, running multiple workers, load balanced using Elastic load balancing and security groups managed by IAM. The workers classify posts and compute sentiment of topics in discussion to look for hate speech, derogatory and abusive speech, slang words and keep track of habitual offenders. The elastic beanstalk instances run the web server that serves aggregated results onto a dashboard by pulling up data stored in mongoDB.

## Challenges we ran into
- Streaming API are inefficient and slow to work with and served as bottleneck of pipeline.
- Load balancing deployments in AWS were difficult to manage as containers grew in number, requiring plumbing of security group, ports and task definitions.
- Without prior experience of deploying containers in the cloud, it offered a steep learning curve.
- Continous pipeline that streams data from one application to another was difficult to build. 

## Accomplishments that we're proud of
- Integrated pipeline that runs out of AWS is proud accomplishment.
- Dashboard with materia design theme that displays tweets in real-time.
- Streaming of tweets, apart from batch processing of tweets that pushes on event changes.

## What we learned
- Cloud-based services involve a lot of moving parts, security, managing health, credentials, but once deployed seamlessly integrate into a powerful workflow.
- Jinja2 templating for front end is a new for the team.

## What's next for SayNoToHarassments
- Integration with other social media channels such as Slack where users communicate.
- Scaling it to events globally through elastic load balancing for modularized services.

## Services & APIs
AWS's EC2 Container service, AWS's Elastic load balancing, AWS's DynamoDB, AWS' Elastic Bean Stalk, RabbitMQ 



