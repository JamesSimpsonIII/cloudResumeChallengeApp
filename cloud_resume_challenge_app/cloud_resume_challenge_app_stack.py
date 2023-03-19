from aws_cdk import (
    Stack,
    aws_s3 as s3_,
    aws_lambda as lambda_,
    aws_cloudfront as cf_,
    aws_cloudfront_origins as origins_,
    aws_route53_patterns as routepatterns_,
    aws_route53 as route53_,
    aws_certificatemanager as acm_,
    aws_route53_targets as targets_,
    aws_dynamodb as dynamodb_,
    aws_apigateway as apigateway_,
    aws_s3_deployment as s3deployment_,

)
from constructs import Construct

class CloudResumeChallengeAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        s3 = s3_.Bucket(self, "CloudResumeChallengeBucket",
            public_read_access=True,
            website_index_document="index.html"
        )

        deployment = s3deployment_.BucketDeployment(self, "bucketDeployment", 
            destination_bucket=s3,
            sources=[s3deployment_.Source.asset("./website")],
            )
        
        cert = acm_.Certificate.from_certificate_arn(self, "Cert", 
            certificate_arn="arn:aws:acm:us-east-1:858275275074:certificate/7affde59-0844-47cd-a0b8-374e2a9335e1"
        )

        distribution = cf_.Distribution(self, "HTTPSDistribution",

            default_root_object="index.html",
             
            default_behavior=cf_.BehaviorOptions(
                origin=origins_.S3Origin(s3),
                allowed_methods=cf_.AllowedMethods.ALLOW_ALL,
                viewer_protocol_policy=cf_.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),

            domain_names=["www.jamesgiantcloud.com", "jamesgiantcloud.com"],
            certificate=cert
        )
        
        zone = route53_.HostedZone.from_hosted_zone_attributes(self, "CitClouds",
            hosted_zone_id="Z0229982UI3W7UOHGZMT",
             zone_name="jamesgiantcloud.com"
        )

        record = route53_.ARecord(self, "AliasRecord",
            zone=zone,
            target=route53_.RecordTarget.from_alias(targets_.CloudFrontTarget(distribution))
        )
        
        countTable = dynamodb_.Table(self, "hitCounterTable",
            table_name="hitCounterTable",
            billing_mode=dynamodb_.BillingMode.PAY_PER_REQUEST,
            partition_key=dynamodb_.Attribute(name="id", type=dynamodb_.AttributeType.STRING)

        )

        hitsLambda = lambda_.Function(self, "hitCounterLambda",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="handler.handler",
            code=lambda_.Code.from_asset("lambdaFns/getVisitorCount/"),
            environment={
                "TABLE_NAME" : countTable.table_name,
            }
        )
        countTable.grant_read_write_data(hitsLambda)

        fn_url = hitsLambda.add_function_url(
            auth_type=lambda_.FunctionUrlAuthType.NONE,
            cors=lambda_.FunctionUrlCorsOptions(
                allowed_origins=["*"]
            )
        )

        



# certificate = acm_.Certificate.from_certificate_arn(self, "Certificate",
        #     "arn:aws:acm:us-east-1:858275275074:certificate/22d2b42b-9863-4cbc-b6df-adbbfcce060a"
        # )

        # redirect = routepatterns_.HttpsRedirect(self, "HTTPSRedirectToCloudfront",
        #     record_names=["www.citclouds.com", "citclouds.com"],
        #     target_domain="https://d3l1ecgd2c1ch0.cloudfront.net",
        #     # certificate=certificate,
        #     zone=route53_.HostedZone.from_hosted_zone_attributes(self, "CitClouds",
        #         hosted_zone_id="Z0416114OODAQBF1OZSL",
        #         zone_name="citclouds.com",
        #     )

        # )