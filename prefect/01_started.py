from prefect import flow, task
from prefect.context import get_run_context
import random
import time
from prefect.types import DateTime
from prefect_shell import ShellOperation



@task
def get_elastic_data(target_date: DateTime) -> str:

    date_str = target_date.strftime("%Y-%m-%dT%H:%M:00Z")

    result = ShellOperation(
        commands=[
            "./scripts/elastic-dump.sh ${START_DATE}",
        ],
        env={"START_DATE": date_str},
    ).run()

    return "Done"


@task
def gzip_data(target_date: DateTime) -> str:

    date_str = target_date.strftime("%Y%m%d-%H")

    result = ShellOperation(
        commands=[
            "./scripts/elastic-gzip.sh ${START_DATE}",        
        ],
        env={"START_DATE": date_str},
    ).run()

    return "Done"


@flow
def main(offset=0) -> list[str]:

    flow_run_context = get_run_context()
    flow_run = flow_run_context.flow_run
    expected_start = flow_run.expected_start_time

    target_date = expected_start.add(hours=offset)
    print(f"Flow run ID: {flow_run.id} will start at {expected_start}, target date is {target_date}")

    elaslic_result = get_elastic_data(target_date)
    print(f"Elastic data result: {elaslic_result}")

    gzip_result = gzip_data(target_date)
    
    results = "Done"
    return results


if __name__ == "__main__":
    main()