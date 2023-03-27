#!/usr/bin/env python3

import logging
import os
import docker
import time

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def del_container(port:int):
    client = docker.from_env()
    docker_name = f"acelink.{port}"

    try:
        container = client.containers.get(docker_name)
        logger.info("Found old container, removing it, wait a second...")
        container.kill()
        time.sleep(5)

    except docker.errors.NotFound as e:
        pass

    client.close()
    return


def run_acelink(ace_id:str,port:int):


    logger.info("Preparing folders")
    try: 

        path_list = [f"/mnt/d1/hls/{port}", f"/mnt/d1/hls-log/{port}" ]

        for path in path_list:

            if not os.path.exists(path):
                os.makedirs(path)

    except OSError as e: 
        logger.error(e)
        return



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

    return


def main():
    run_acelink("c9ee7c95e7a2e9cd0e848b1f70848453652bebc2",3231)

if __name__ == "__main__":
    main()
