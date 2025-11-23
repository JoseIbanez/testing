from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone
import time


from prefect import get_client
from prefect.client.schemas.filters import DeploymentFilter, FlowRunFilter
from prefect.client.schemas.objects import FlowRun
from prefect.client.schemas.sorting import FlowRunSort
from prefect.states import Scheduled


async def schedule_deployment() -> None:

    async with get_client() as client:


        # get deployment list
        deployments = await client.read_deployments()

        deployment_id = None
        for deployment in deployments:
            print(f"Deployment: {deployment.id} - {deployment.name} - {deployment.flow_id}")
            print(deployment)
            deployment_id = deployment.id

        # get deployment by name
        #deployment = await client.read_deployment_by_name("main/demo2")
        #print(f"Deployment: {deployment.id} - {deployment.name}")


        for day in [1, 10, 13, 14, 15, 17, 19, 20, 21, 23,24, 28, 29, 31]:

            scheduled_time = datetime(2025, 6, day, 0, 0 , 0, tzinfo=timezone.utc)

            run_flow = await client.create_flow_run_from_deployment(
                tags=[f"{scheduled_time.strftime('%Y-%m-%d')}"],
                deployment_id=deployment_id,
                state=Scheduled(scheduled_time=scheduled_time),
                #parameters={"target_date": "2025-06-01T00:00:00Z"},
            )
            print(f"Flow run scheduled: {run_flow} for deployment {deployment_id}")

            time.sleep(10)


if __name__ == "__main__":

    asyncio.run(schedule_deployment())
    print("Deployment scheduled successfully.")

