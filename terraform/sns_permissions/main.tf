

data "aws_iam_policy_document" "sns_publish_policy" {
  statement {

    effect = "Allow"

    actions = [
      "sns:Publish",
      "sns:Subscribe",
      "sns:GetTopicAttributes",
      "sns:ListSubscriptionsByTopic"
    ]

    resources = [
      var.sns_arn
    ]
  }
}

resource "aws_iam_policy" "sns_policy" {
  name_prefix = var.policy_name
  policy      = data.aws_iam_policy_document.sns_publish_policy.json
}

# Attach the policy to an IAM role
resource "aws_iam_role_policy_attachment" "policy_attachements" {
  role       = var.iam_role
  policy_arn = aws_iam_policy.sns_policy.arn
}
