from mypy_boto3_dynamodb import DynamoDBClient
from mypy_boto3_dynamodb.type_defs import GetItemOutputTypeDef
from pydantic import BaseModel


class User(BaseModel):
    email: str
    subscription_arn: str = ""
    otp: str = ""
    auth_token: str = ""
    token_expiry: int = 0


class UsersTable:
    def __init__(self, dynamo_db: DynamoDBClient, table_name: str):
        self.client = dynamo_db
        self.table_name = table_name

    def create(self, email: str) -> User:
        # Check to see if user is already registered
        if self.get(email):
            raise ValueError("User already exists!")

        # If not, make a new model and save
        new_user = User(email=email)

        self.client.put_item(
            TableName="Users",
            Item={
                "email": {"S": new_user.email},
                "subscription_arn": {"S": new_user.email},
                "otp": {"S": new_user.otp},
                "auth_token": {"S": new_user.auth_token},
                "token_expires": {"N": str(new_user.token_expiry)},
            },
        )
        return new_user

    def get(self, email: str) -> User | None:
        response: GetItemOutputTypeDef = self.client.get_item(
            TableName=self.table_name, Key={"email": email}
        )
        if not (user := response["Item"]):
            return None
        else:
            return User(email=str(user["email"]))
