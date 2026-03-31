
resource "aws_cloudwatch_event_rule" "nightly" {
  name = "s3-lifecycle-nightly"
  schedule_expression = "cron(0 2 * * ? *)"
  schedule_time_zone = "US/Eastern"
}

resource "aws_cloudwatch_event_target" "lambda" {
  rule = aws_cloudwatch_event_rule.nightly.name
  arn  = aws_lambda_function.lifecycle.arn
}

resource "aws_lambda_permission" "allow" {
  statement_id  = "AllowEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lifecycle.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.nightly.arn
}
