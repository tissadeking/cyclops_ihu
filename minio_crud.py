from minio import Minio
from minio.error import S3Error
import config

# MinIO credentials and endpoint
'''minio_url = "http://localhost:9100"  # API port
minio_endpoint = "localhost:9100"
access_key = "minioadmin"
secret_key = "minioadmin"
bucket_name = "long-term"
file_path = "policy_store.csv"
download_path = "policy_store_downloaded.csv"'''

minio_endpoint = config.minio_endpoint
access_key = config.access_key
secret_key = config.secret_key
bucket_name = config.bucket_name
print(minio_endpoint, access_key, secret_key, bucket_name)

# Initialize MinIO client
minio_client = Minio(
    minio_endpoint,  #MinIO server URL
    access_key=access_key,  #MinIO access key or username
    secret_key=secret_key,  #MinIO secret key or password
    secure=False  # Set to False if not using HTTPS
)

#create bucket
def create_bucket():
    minio_client.make_bucket(bucket_name)

# Ensure the bucket exists
def ensure_bucket():
    try:
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' created.")
        else:
            print(f"Bucket '{bucket_name}' already exists.")
    except S3Error as e:
        print(f"Error ensuring bucket: {e}")

# Create or upload an object
def create_object(object_name, file_path):
    try:
        minio_client.fput_object(bucket_name, object_name, file_path)
        print(f"Object '{object_name}' uploaded successfully.")
    except S3Error as e:
        print(f"Error uploading object: {e}")

# Retrieve an object
def retrieve_object(object_name, download_path):
    try:
        minio_client.fget_object(bucket_name, object_name, download_path)
        print(f"Object '{object_name}' downloaded to '{download_path}'.")
    except S3Error as e:
        print(f"Error retrieving object: {e}")

# Update an object (re-upload with the same name)
def update_object(object_name, new_file_path):
    try:
        minio_client.fput_object(bucket_name, object_name, new_file_path)
        print(f"Object '{object_name}' updated successfully.")
    except S3Error as e:
        print(f"Error updating object: {e}")

# Delete an object
def delete_object(object_name):
    try:
        minio_client.remove_object(bucket_name, object_name)
        print(f"Object '{object_name}' deleted successfully.")
    except S3Error as e:
        print(f"Error deleting object: {e}")

# List all objects in the bucket
def list_objects():
    try:
        objects = minio_client.list_objects(bucket_name)
        print("Objects in bucket:")
        for obj in objects:
            print(f" - {obj.object_name}")
    except S3Error as e:
        print(f"Error listing objects: {e}")

# Example usage
'''if __name__ == "__main__":
    ensure_bucket()  # Ensure the bucket exists

    # Example object details
    object_name = "policy"
    upload_path = "policy_store.csv"
    download_path = "policy_store_downloaded.csv"  #download path
    update_path = "policy_store.csv"  #updated file path

    # Perform CRUD operations
    create_object(object_name, upload_path)  # Create/Upload
    list_objects()  # List all objects
    retrieve_object(object_name, download_path)  # Retrieve
    update_object(object_name, update_path)  # Update
    delete_object(object_name)  # Delete
    list_objects()  # List all objects after deletion'''
