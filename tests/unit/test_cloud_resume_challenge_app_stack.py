import aws_cdk as core
import aws_cdk.assertions as assertions

from cloud_resume_challenge_app.cloud_resume_challenge_app_stack import CloudResumeChallengeAppStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cloud_resume_challenge_app/cloud_resume_challenge_app_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CloudResumeChallengeAppStack(app, "cloud-resume-challenge-app")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
