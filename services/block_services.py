import requests

base_url_blocks_by_time = "https://blockchain.info/blocks"
base_url_block_details = "https://blockchain.info/rawblock"


def get_blocks(millisecond_time) -> list:
    """
    This function sends a request to get all blockchain config
    """
    url = f"{base_url_blocks_by_time}/{millisecond_time}?format=json"

    response = requests.get(url)

    return response.json()


def get_block(block_hash: str) -> dict:
    """
    This function sends a request to get block by hash
    """
    url = f"{base_url_block_details}/{block_hash}"

    response = requests.get(url)

    return response.json()
