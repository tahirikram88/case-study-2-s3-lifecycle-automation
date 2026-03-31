import os
import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# ----------------------------
# Local / Demo Configuration
# ----------------------------
DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"
LOCAL_TEST = os.getenv("LOCAL_TEST", "false").lower() == "true"
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

SIZE_THRESHOLD_BYTES = 100 * 1024 ** 3  # 100 GB
EXEMPT_TAG_KEY = "lifecycle-exempt"

logging.basicConfig(level=logging.INFO)

# ----------------------------
# Local Test Mode (NO AWS)
# ----------------------------
if LOCAL_TEST:
    def lambda_handler(event=None, context=None):
        print("✅ LOCAL TEST MODE")
        print("✅ Lambda executed successfully")
        print("✅ Would scan S3 buckets")
        print("✅ Would apply lifecycle policies")
        return

    # Allow local execution
    if __name__ == "__main__":
        lambda_handler()

# ----------------------------
# AWS Mode (Production)
# ----------------------------
else:
    import boto3
    from botocore.exceptions import ClientError

    s3 = boto3.client("s3", region_name=AWS_REGION)
    cw = boto3.client("cloudwatch", region_name=AWS_REGION)

    def lambda_handler(event=None, context=None):
        tz = ZoneInfo("US/Eastern")
        logging.info(f"Run started at {datetime.now(tz)}")

        for bucket in s3.list_buckets()["Buckets"]:
            name = bucket["Name"]

            if is_exempt(name) or has_lifecycle(name):
                continue

            size = get_bucket_size(name)
            if size and size >= SIZE_THRESHOLD_BYTES:
                if DRY_RUN:
                    logging.info(f"DRY_RUN: Would apply lifecycle to {name}")
                else:
                    apply_lifecycle(name)

    def is_exempt(bucket):
        try:
            tags = s3.get_bucket_tagging(Bucket=bucket)["TagSet"]
            return any(
                t["Key"] == EXEMPT_TAG_KEY and t["Value"].lower() == "true"
                for t in tags
            )
        except ClientError:
            return False

    def has_lifecycle(bucket):
        try:
            s3.get_bucket_lifecycle_configuration(Bucket=bucket)
            return True
        except ClientError:
            return False

    def get_bucket_size(bucket):
        end = datetime.utcnow()
        start = end - timedelta(days=2)

        r = cw.get_metric_statistics(
            Namespace="AWS/S3",
            MetricName="BucketSizeBytes",
            Dimensions=[
                {"Name": "BucketName", "Value": bucket},
                {"Name": "StorageType", "Value": "StandardStorage"},
            ],
            StartTime=start,
            EndTime=end,
            Period=86400,
            Statistics=["Average"],
        )
        return r["Datapoints"][0]["Average"] if r["Datapoints"] else None

    def apply_lifecycle(bucket):
        s3.put_bucket_lifecycle_configuration(
            Bucket=bucket,
            LifecycleConfiguration={
                "Rules": [
                    {
                        "ID": "auto-tier",
                        "Status": "Enabled",
                        "Transitions": [
                            {"Days": 30, "StorageClass": "STANDARD_IA"},
                            {"Days": 180, "StorageClass": "GLACIER"},
                        ],
                    }
                ]
            },
        )

    if __name__ == "__main__":
        lambda_handler()
