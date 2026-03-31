
resource "aws_lambda_function" "lifecycle" {
  function_name = "s3-lifecycle-enforcer"
  role = aws_iam_role.lambda_role.arn
  handler = "main.lambda_handler"
  runtime = "python3.10"
  timeout = 900
  filename = "../lambda.zip"
  environment { variables = { DRY_RUN = "false" } }
}
