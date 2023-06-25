locals {
  enabled = module.this.enabled

  policy_arn_prefix = format(
    "arn:%s:iam::%s:policy",
    join("", data.aws_partition.current.*.partition),
    join("", data.aws_caller_identity.current.*.account_id),
  )

}

module "label" {
  source     = "cloudposse/label/null"
  version    = "0.25.0"
  attributes = [var.function_name]

  context = module.this.context
}

data "aws_partition" "current" {
  count = local.enabled ? 1 : 0
}

data "aws_caller_identity" "current" {
  count = local.enabled ? 1 : 0
}

data "archive_file" "lambda_zip" {
  count       = local.enabled ? 1 : 0
  type        = "zip"
  source_file = "handler.py"
  output_path = "lambda_function.zip"
}

module "lambda" {
  source                 = "../"
  description            = "saves users details to dynamo db for personal site"
  filename               = join("", data.archive_file.lambda_zip.*.output_path)
  function_name          = module.label.id
  handler                = var.handler
  runtime                = var.runtime
  iam_policy_description = var.iam_policy_description
  role                   = "arn:aws:iam::606526534964:role/mel3kings-lambda-role"
  custom_iam_policy_arns = [
    "arn:aws:iam::aws:policy/job-function/ViewOnlyAccess",
    "arn:aws:iam::606526534964:policy/mel3kings-lambda-policy"
  ]
  context = module.this.context
}
