from mypy_boto3_sns import SNSClient


class EmailClient:
    email_attribute = "email"

    def __init__(self, sns: SNSClient, topic: str):
        self.sns = sns
        self.topic = topic

    def send_email(self, email: str, subject: str, body: str):
        # Send the email with the filter policy thing so only the specific users gets the email
        response = self.sns.publish(
            TopicArn=self.topic,
            Message=body,
            Subject=subject,
            MessageAttributes={
                self.email_attribute: {"DataType": "string", "StringValue": f"{email}"}
            },
        )
        print(response)

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
            Attributes={"FilterPolicy": f"{self.email_attribute: {email}}"},
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
