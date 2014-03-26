# Zypper update check/notify.
Rudimentary script to check any updates available on remote zypper instances, and sends available updates in a formatted ASCII table to a Amazon SNS topic.

## Setup
As indicated by the boto documentation, users need to set the following environment variables:

```bash
export AWS_ACCESS_KEY_ID="<Insert your AWS Access Key>"
export AWS_SECRET_ACCESS_KEY="<Insert your AWS Secret Key>"
```

## Use/Switches
- -t : Destination SNS topic ARN

## Dependencies :
+   boto
+   PrettyTable > 0.6
+   xml
