from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

import elastic
import parse

# Initialize FastMCP server
mcp = FastMCP("MPN (Mobile Private Network) Agent")



@mcp.tool()
async def get_customers() -> str:
    """Get Customer List with status """

    data = elastic.get_es_customer_list()
    customer_list = parse.get_customer_list(data)
    return customer_list

@mcp.tool()
async def get_status(customer_name: str) -> str:
    """Get Customer Details status

    Args:
        customer_name: customer name
    """
    data = elastic.get_es_customer_list()
    state = parse.custumer_details(data, customer_name)


    return state


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')


