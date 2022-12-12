from aws_cdk import (
    aws_s3 as s3_,
    Stack,
    aws_cloudfront as cf_,
    aws_lambda as lambda_,
    aws_cloudfront_origins as origins,
    
    
)

from constructs import Construct

class CloudResumeChallengeAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "CloudResumeChallengeAppQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
        s3 = s3_.Bucket(self, "CloudResumeChallengeBucket",
            block_public_access=s3_.BlockPublicAccess.BLOCK_ALL,
        )
        
        distribution = cf_.CloudFrontWebDistribution(self, 
            default_behavior=cf_.BehaviorOptions(origin=origins.S3Origin(s3))
            default_root_object="index.html",
            allowed_methods=cf_.AllowedMethods.ALLOW_ALL,

            viewer_protocol_policy=cf_.cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
        )

        
