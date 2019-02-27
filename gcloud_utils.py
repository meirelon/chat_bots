from google.cloud import storage

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)


def deploy_image(obj, project_id, bucket, filename):
    client = storage.Client(project=project_id)
    with NamedTemporaryFile(mode='wb') as temp:
        pickle.dump(obj, temp)
        temp.seek(0)
        # gcs_path = os.path.join(destination_path, datetime.today().strftime("%Y%m%d"), '{filename}.pkl'.format(filename=filename))
        gcs_path=filename
        client.bucket(bucket).blob(gcs_path).upload_from_filename(temp.name)
