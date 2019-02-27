import os

def get_image_emotion(photo_link, image, instance, zone):
    docker_cmd = "'docker run -e photo_link={photo_link} -e detection_type=face {image}'"
    docker_cmd_formatted = docker_cmd.format(photo_link=photo_link, image=image)
    gcloud_cmd = """gcloud compute ssh {instance} --zone {zone} -- """
    cli = gcloud_cmd.format(instance=instance, zone=zone) + docker_cmd_formatted
    return str(os.popen(cli).read().strip())
