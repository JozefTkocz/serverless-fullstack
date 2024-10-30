data "aws_iam_policy_document" "s3_policy_document" {
  statement {
    actions = [
      "s3:ListBucket",
      "s3:PutObject",
      "s3:GetObject",
      "s3:GetBucketLocation",
    ]
    effect = "Allow"
    resources = [
      "${var.s3_bucket_arn}/*",
      var.s3_bucket_arn,
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
