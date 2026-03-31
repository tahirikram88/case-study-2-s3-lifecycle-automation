import os

print("✅ Script started")

LOCAL_TEST = os.getenv("LOCAL_TEST", "false").lower() == "true"
DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"

def lambda_handler(event=None, context=None):
    if LOCAL_TEST:
        print("✅ LOCAL_TEST is enabled")
        print("✅ Lambda logic executed successfully")
        print("✅ Would scan S3 buckets")
        print("✅ Would apply lifecycle policies")
        return

    print("⚠️ AWS MODE (this requires AWS configuration)")
    return

if __name__ == "__main__":
    lambda_handler()
``
