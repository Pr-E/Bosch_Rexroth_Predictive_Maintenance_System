import io
import json
import sys
import os
import shutil
from pathlib import Path

import boto3
import pandas as pd
from botocore.exceptions import NoCredentialsError

from config.constants import AWS_REGION
from src.logger import configure_logger
from src.exception import MyException

logging = configure_logger()


class S3Storage:

    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name

        # Try to create S3 client; fall back to local storage if no credentials
        try:
            self.s3 = boto3.client("s3", region_name=AWS_REGION.strip())
            self.use_local = False
            logging.info("S3Storage: Using AWS S3")
        except NoCredentialsError:
            self.use_local = True
            self.local_base = Path("local_storage")
            self.local_base.mkdir(exist_ok=True)
            logging.warning("No AWS credentials found – using LOCAL storage instead")

    def _local_path(self, s3_key: str) -> Path:
        """Convert an S3 key to a local file path."""
        return self.local_base / s3_key

    def upload_bytes(self, data, s3_key: str, content_type: str):
        if self.use_local:
            path = self._local_path(s3_key)
            path.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(data, str):
                data = data.encode("utf-8")
            path.write_bytes(data)
            logging.info(f"Written locally: {path}")
        else:
            try:
                self.s3.put_object(
                    Bucket=self.bucket_name,
                    Key=s3_key,
                    Body=data,
                    ContentType=content_type
                )
                logging.info(f"Uploaded to S3: s3://{self.bucket_name}/{s3_key}")
            except Exception as e:
                logging.error(f"S3 upload failed: {e}")
                raise MyException(e, sys)

    def load_csv(self, csv_key: str):
        if self.use_local:
            path = self._local_path(csv_key)
            if not path.exists():
                raise FileNotFoundError(f"Local CSV not found: {path}")
            data = pd.read_csv(path, parse_dates=["timestamp"])
            logging.info(f"Loaded CSV locally: {path} | Rows: {len(data):,}")
            return data
        else:
            try:
                obj = self.s3.get_object(Bucket=self.bucket_name, Key=csv_key)
                data = pd.read_csv(
                    io.BytesIO(obj["Body"].read()), parse_dates=["timestamp"]
                )
                logging.info(f"Loaded CSV from S3: {csv_key} | Rows: {len(data):,}")
                return data
            except Exception as e:
                logging.error(f"Error loading CSV from S3: {e}")
                raise MyException(e, sys)

    def load_json(self, json_key: str):
        if self.use_local:
            path = self._local_path(json_key)
            if not path.exists():
                raise FileNotFoundError(f"Local JSON not found: {path}")
            with open(path, "r", encoding="utf-8") as f:
                metadata = json.load(f)
            logging.info(f"Loaded JSON locally: {path}")
            return metadata
        else:
            try:
                obj = self.s3.get_object(Bucket=self.bucket_name, Key=json_key)
                metadata = json.loads(obj["Body"].read().decode("utf-8"))
                logging.info(f"Loaded JSON from S3: {json_key}")
                return metadata
            except Exception as e:
                logging.error(f"Error loading JSON from S3: {e}")
                raise MyException(e, sys)

    def get_latest_file(self, prefix: str, keyword: str = None):
        if self.use_local:
            base = self.local_base / prefix
            if not base.exists():
                raise FileNotFoundError(f"Local prefix not found: {base}")
            files = list(base.rglob("*"))
            if keyword:
                files = [f for f in files if keyword in f.name]
            if not files:
                raise FileNotFoundError(
                    f"No local files matching prefix='{prefix}', keyword='{keyword}'"
                )
            latest = max(files, key=lambda p: p.stat().st_mtime)
            local_key = str(latest.relative_to(self.local_base)).replace("\\", "/")
            logging.info(f"Latest local file: {local_key}")
            return local_key
        else:
            try:
                response = self.s3.list_objects_v2(
                    Bucket=self.bucket_name, Prefix=prefix
                )
                if "Contents" not in response:
                    raise ValueError(f"No files found under prefix: {prefix}")
                files = response["Contents"]
                if keyword:
                    files = [obj for obj in files if keyword in obj["Key"]]
                if not files:
                    raise ValueError(f"No matching files found for keyword: {keyword}")
                latest_file = max(files, key=lambda x: x["LastModified"])
                logging.info(f"Latest file selected: {latest_file['Key']}")
                return latest_file["Key"]
            except Exception as e:
                logging.error(f"Failed finding latest file: {e}")
                raise MyException(e, sys)

    def upload_json(self, data: dict, s3_key: str):
        """Serialize a dict as JSON and upload (local or S3)."""
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        self.upload_bytes(json_str, s3_key, content_type="application/json")

    def upload_model(self, local_path: str, model_name: str, run_id: str) -> str:
        if self.use_local:
            dest = self.local_base / "mlflow-artifacts" / run_id / f"{model_name}.joblib"
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(local_path, dest)
            logging.info(f"Model copied locally: {dest}")
            return str(dest)
        else:
            try:
                s3_key = f"mlflow-artifacts/{run_id}/{model_name}.joblib"
                self.s3.upload_file(local_path, self.bucket_name, s3_key)
                s3_uri = f"s3://{self.bucket_name}/{s3_key}"
                logging.info(f"Model uploaded: {s3_uri}")
                return s3_uri
            except Exception as e:
                logging.error(f"Model upload failed: {e}")
                raise MyException(e, sys)

    def file_exists(self, s3_key: str) -> bool:
        if self.use_local:
            return self._local_path(s3_key).exists()
        try:
            self.s3.head_object(Bucket=self.bucket_name, Key=s3_key)
            return True
        except Exception:
            return False