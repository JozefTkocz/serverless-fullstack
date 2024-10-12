from mypy_boto3_sns import SNSClient


class EmailClient:
    def __init__(self, sns: SNSClient, topic: str):
        self.sns = sns
        self.topic = topic

    def send_email(self, email: str, body: str):
        pass

    def register_email(self, email: str) -> str:
        """
        Sends the subscription confirmation email to the provided email.

        Returns the SNS subscription ARN, so confirmation status can be
        checked at a later time.
        """
        response = self.sns.subscribe(
            TopicArn=self.topic,
            Protocol="email",
            Endpoint=email,
            # todo: set filter policy to only email this subscriber when a value is set
            # Attributes={"string": "string"},
            # todo: return and store the subscription ARN
            ReturnSubscriptionArn=True,
        )
        print(response)
        return response["SubscriptionArn"]

    def check_subscription(self, arn: str) -> bool:
        """
        Returns True if the subscription has been confirmed, otherwise False
        """
        response = self.sns.get_subscription_attributes(SubscriptionArn=arn)
        return not response["Attributes"]["PendingConfirmation"]
