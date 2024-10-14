# Define a policy for read/write table access
data "aws_iam_policy_document" "s3_policy_document" {
  statement {
    actions = [
      "dynamodb:BatchGetItem",
      "dynamodb:BatchWriteItem",
      "dynamodb:ConditionCheckItem",
      "dynamodb:PutItem",
      "dynamodb:DescribeTable",
      "dynamodb:DeleteItem",
      "dynamodb:GetItem",
      "dynamodb:Scan",
      "dynamodb:Query",
      "dynamodb:UpdateItem"
    ]
    resources = [
      var.s3_bucket_arn
    ]
  }
}

resource "aws_iam_policy" "s3_policy" {
  name   = var.policy_name
  policy = data.aws_iam_policy_document.s3_policy_document.json
}

# Attach the policy to an IAM role
resource "aws_iam_role_policy_attachment" "policy_attachement" {
  role       = var.iam_role
  policy_arn = aws_iam_policy.s3_policy.arn
}
