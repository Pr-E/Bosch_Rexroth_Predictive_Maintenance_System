import io
import json
import sys

import boto3
import pandas as pd

from config.constants import AWS_REGION

from src.logger import configure_logger
from src.exception import MyException




logging = configure_logger()


# ==========================================================
# AWS S3 STORAGE
# ==========================================================

class S3Storage:

    def __init__(self, bucket_name: str):

        self.bucket_name = bucket_name

        self.s3 = boto3.client(
            "s3",
            region_name=AWS_REGION.strip()
        )
    

    # ======================================================
    # UPLOAD STRING / BYTES
    # ======================================================

    def upload_bytes(

        self,

        data,

        s3_key: str,

        content_type: str

    ):

        try:

            self.s3.put_object(

                Bucket=self.bucket_name,

                Key=s3_key,

                Body=data,

                ContentType=content_type
            )

            logging.info(

                f"Uploaded to S3: "

                f"s3://{self.bucket_name}/{s3_key}"
            )

        except Exception as e:

            logging.error(

                f"S3 upload failed: {e}"
            )

            raise MyException(
                e,
                sys
            )

    # ======================================================
    # LOAD CSV
    # ======================================================

    def load_csv(

        self,

        csv_key: str
    ):

        try:

            obj = self.s3.get_object(

                Bucket=self.bucket_name,

                Key=csv_key
            )

            data = pd.read_csv(

                io.BytesIO(

                    obj["Body"].read()
                ),

                parse_dates=[
                    "timestamp"
                ]
            )

            logging.info(

                f"Loaded CSV from S3: "

                f"{csv_key} | "

                f"Rows: {len(data):,}"
            )

            return data

        except Exception as e:

            logging.error(

                f"Error loading CSV "

                f"from S3: {e}"
            )

            raise MyException(
                e,
                sys
            )

    # ======================================================
    # LOAD JSON
    # ======================================================

    def load_json(

        self,

        json_key: str
    ):

        try:

            obj = self.s3.get_object(

                Bucket=self.bucket_name,

                Key=json_key
            )

            metadata = json.loads(

                obj["Body"]

                .read()

                .decode("utf-8")
            )

            logging.info(

                f"Loaded JSON from S3: "

                f"{json_key}"
            )

            return metadata

        except Exception as e:

            logging.error(

                f"Error loading JSON "

                f"from S3: {e}"
            )

            raise MyException(
                e,
                sys
            )

    # ======================================================
    # GET LATEST FILE
    # ======================================================

    def get_latest_file(

        self,

        prefix: str,

        keyword: str = None

    ):

        try:

            response = (

                self.s3.list_objects_v2(

                    Bucket=self.bucket_name,

                    Prefix=prefix
                )
            )

            if "Contents" not in response:

                raise ValueError(

                    f"No files found "

                    f"under prefix: {prefix}"
                )

            files = response["Contents"]

            if keyword:

                files = [

                    obj

                    for obj in files

                    if keyword in obj["Key"]
                ]

            if not files:

                raise ValueError(

                    f"No matching files "

                    f"found for keyword: "
                    f"{keyword}"
                )

            latest_file = max(

                files,

                key=lambda x:

                x["LastModified"]
            )

            logging.info(

                f"Latest file selected: "

                f"{latest_file['Key']}"
            )

            return latest_file["Key"]

        except Exception as e:

            logging.error(

                f"Failed finding latest file: "

                f"{e}"
            )

            raise MyException(
                e,
                sys
            )

    # ======================================================
    # UPLOAD MODEL ARTIFACT
    # ======================================================

    def upload_model(

        self,

        local_path: str,

        model_name: str,

        run_id: str
    ) -> str:

        try:

            s3_key = (

                f"mlflow-artifacts/"

                f"{run_id}/"

                f"{model_name}.joblib"
            )

            self.s3.upload_file(

                local_path,

                self.bucket_name,

                s3_key
            )

            s3_uri = (

                f"s3://"

                f"{self.bucket_name}/"

                f"{s3_key}"
            )

            logging.info(

                f"Model uploaded: "

                f"{s3_uri}"
            )

            return s3_uri

        except Exception as e:

            logging.error(

                f"Model upload failed: "

                f"{e}"
            )

            raise MyException(
                e,
                sys
            )

    # ======================================================
    # FILE EXISTS
    # ======================================================

    def file_exists(

        self,

        s3_key: str
    ) -> bool:

        try:

            self.s3.head_object(

                Bucket=self.bucket_name,

                Key=s3_key
            )

            return True

        except Exception:

            return False
        