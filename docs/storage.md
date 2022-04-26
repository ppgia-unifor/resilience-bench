## Storage configuration

It supports two strategies to save the results dataset: remote and local. The remote strategy use Amazon S3. Open `docker-compose.yaml` file and find the definition of `scheduler` container, in the `environment`

#### Remote (Amazon S3) configuration

1. Configure the AWS credentials file on host machine by follow the steps available [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).
2. Set the bucket name to `AWS_BUCKET_NAME` variable.
3. Set the path inside the bucket to `AWS_OUTPUT_PATH` variable.
4. Make sure the variable `DISK_PATH` do not exist.

#### Local configuration

1. Make sure `AWS_BUCKET_NAME` and `AWS_OUTPUT_PATH` do not exist;
2. Set `DISK_PATH` to a path inside the container;
3. Mount a volume binding `DISK_PATH` and a path in the host;