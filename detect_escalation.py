import json
import os

log_folder = "logs"

for file in os.listdir(log_folder):
    if file.endswith(".json"):
        try:
            with open(os.path.join(log_folder, file)) as f:
                data = json.load(f)

                for record in data.get("Records", []):
                    event = record.get("eventName")

                    if event == "AssumeRole":
                        role = record.get("requestParameters", {}).get("roleArn", "Unknown")
                        user_info = record.get("userIdentity", {})
                        user = user_info.get("arn") or user_info.get("principalId", "Unknown")

                        print("⚠️ Privilege Escalation Detected")
                        print(f"User: {user}")
                        print(f"Assumed Role: {role}")
                        print("-" * 40)

        except Exception as e:
            print(f"Error reading {file}: {e}")
