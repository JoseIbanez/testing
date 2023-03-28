#!/usr/bin/env python3

import logging
import os
import docker
import time

#from acelink_server.common import getLogger

logger = logging.getLogger(__name__)


def get_container(port:int):
    client = docker.from_env()
    docker_name = f"acelink.{port}"

    container_id = None
    ace_id = None
    description = None

    try:
        container = client.containers.get(docker_name)
        container_id = container.id

    except docker.errors.NotFound as e:
        pass

    client.close()

    try:
        with open(f"/mnt/d1/hls/{port}/description","r") as f:
            description = f.readline().rstrip()

        with open(f"/mnt/d1/hls/{port}/id","r") as f:
            ace_id = f.readline().rstrip()

    except OSError as e:
        logger.info(e)
        pass

    result = {
        'port': port,
        'ace_id': ace_id,
        'container_id': container_id,
        'description': description
    }

    return result


def del_container(port:int):
    client = docker.from_env()
    docker_name = f"acelink.{port}"
    container_id = None

    try:
        container = client.containers.get(docker_name)
        container_id = container.id
        logger.info("Found a container:%s,removing it, wait a second...",container_id)
        container.kill()

    except docker.errors.NotFound as e:
        container_id = "0"
        pass

    client.close()
    return container_id


def run_acelink(ace_id:str,port:int,description=""):


    logger.info("Preparing folders")
    try: 

        path_list = [f"/mnt/d1/hls/{port}", f"/mnt/d1/hls-log/{port}" ]

        for path in path_list:

            if not os.path.exists(path):
                os.makedirs(path)

    except OSError as e: 
        logger.error(e)
        return

    with open(f"/mnt/d1/hls/{port}/description","w") as f:
        f.write(description)


    client = docker.from_env()
    docker_name = f"acelink.{port}"

    ## Remove old container
    try:
        container = client.containers.get(docker_name)
        logger.info("Found old container, removing it, wait a second...")
        container.kill()
        time.sleep(5)

    except docker.errors.NotFound as e:
        pass


    if not ace_id:
        logger.info("Not ace id provided, no container created")
        client.close()
        return


    ## Create acelink container

    container = client.containers.run("acelink-ffmpeg",
                        detach=True,
                        auto_remove=True,
                        cap_add=['NET_ADMIN'],
                        environment={"ID": ace_id},
                        ports={ "6878/tcp" : str(port)},
                        name=docker_name,
                        volumes={f"/mnt/d1/hls/{port}" : {'bind': '/mnt/hls', 'mode': 'rw'}}                       
                        )

    logger.info("Acelink container created: %s %s", container.name, container.id)
    client.close()

    return container.id


def main():
    run_acelink("c9ee7c95e7a2e9cd0e848b1f70848453652bebc2",3231)

if __name__ == "__main__":
    main()
