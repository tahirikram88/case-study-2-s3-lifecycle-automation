
resource "aws_iam_role" "lambda_role" {
  name = "s3-lifecycle-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{ Effect="Allow", Principal={Service="lambda.amazonaws.com"}, Action="sts:AssumeRole" }]
  })
}

resource "aws_iam_policy" "lambda_policy" {
  name = "s3-lifecycle-policy"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Effect="Allow", Action=["s3:ListAllMyBuckets","s3:GetBucketLifecycleConfiguration","s3:PutBucketLifecycleConfiguration","s3:GetBucketTagging"], Resource="*" },
      { Effect="Allow", Action="cloudwatch:GetMetricStatistics", Resource="*" },
      { Effect="Allow", Action=["logs:CreateLogGroup","logs:CreateLogStream","logs:PutLogEvents"], Resource="*" }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach" {
  role = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}
