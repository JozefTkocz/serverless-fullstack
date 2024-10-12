from mypy_boto3_dynamodb import DynamoDBClient
from mypy_boto3_dynamodb.type_defs import GetItemOutputTypeDef
from pydantic import BaseModel


class User(BaseModel):
    email: str
    subscription_arn: str = ""
    otp: str = ""
    otp_expires: int = 0
    auth_token: str = ""
    auth_token_expires: int = 0


class UsersTable:
    def __init__(self, dynamo_db: DynamoDBClient, table_name: str):
        self.client = dynamo_db
        self.table_name = table_name

    def key(self, email: str) -> dict[str, dict[str, str]]:
        return {"UserId": {"S": email}}

    def item_to_user(self, item: dict) -> User:
        return User(
            email=str(item["UserId"]),
            subscription_arn=str(item["subscription_arn"]),
            otp=str(item["otp"]),
            otp_expires=int(item["otp_expires"]),
            auth_token=str(item["auth_token"]),
            auth_token_expires=int(item["auth_token_expires"]),
        )

    def user_to_item(self, user: User) -> dict:
        return {
            "UserId": {"S": user.email},
            "subscription_arn": {"S": user.subscription_arn},
            "otp": {"S": user.otp},
            "otp_expires": {"N": str(user.otp_expires)},
            "auth_token": {"S": user.auth_token},
            "auth_token_expires": {"N": str(user.auth_token_expires)},
        }

    def create(self, email: str) -> User:
        if self.get(email):
            raise ValueError("User already exists!")

        new_user = User(email=email)
        self.client.put_item(
            TableName=self.table_name,
            Item=self.user_to_item(new_user),
        )
        return new_user

    def get(self, email: str) -> User | None:
        response: GetItemOutputTypeDef = self.client.get_item(
            TableName=self.table_name, Key=self.key(email)
        )
        if not (user := response.get("Item")):
            return None
        else:
            return self.item_to_user(user)

    def update(self, user: User) -> User:
        self.client.put_item(
            TableName=self.table_name,
            Item=self.user_to_item(user),
        )
        return user
