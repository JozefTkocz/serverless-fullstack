from mypy_boto3_sns import SNSClient


class EmailClient:
    def __init__(self, sns: SNSClient, topic: str):
        self.sns = sns
        self.topic = topic

    def send_email(self, email: str, body: str):
        pass

    def register_email(self, email: str):
        response = self.sns.subscribe(
            TopicArn=self.topic,
            Protocol="email",
            Endpoint=email,
            # todo: set filter policy to only email this subscriber when a value is set
            # Attributes={"string": "string"},
            # todo: return and store the subscription ARN
            ReturnSubscriptionArn=False,
        )
        print(response)
        return response

    def check_subscription(self, arn: str):
        pass
