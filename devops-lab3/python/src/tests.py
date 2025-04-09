import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
import re

from main import app
from utils.system import (
    get_size, get_system_info, get_cpu_info, get_memory_info, get_disk_usage
)
from schemas.system import System, CPU, Memory, Disk

client = TestClient(app)

@pytest.mark.parametrize("input_bytes, expected_output", [
    (1024, "1.00KB"),
    (1048576, "1.00MB"),
    (1073741824, "1.00GB"),
    (500, "500.00B"),
])
def test_get_size(input_bytes, expected_output):
    assert get_size(input_bytes) == expected_output

def test_get_system_info():
    system_info = get_system_info()
    assert isinstance(system_info, System)
    assert system_info.system is not None

def test_get_cpu_info():
    cpu_info = get_cpu_info()
    assert isinstance(cpu_info, CPU)
    assert cpu_info.physical_cores > 0
    assert cpu_info.total_cores > 0
    assert "Mhz" in cpu_info.max_freq

def test_get_memory_info():
    memory_info = get_memory_info()
    assert isinstance(memory_info, Memory)

    size_pattern = r"^\d+\.\d{2}(B|KB|MB|GB|TB|PB)$"
    percentage_pattern = r"^\d{1,3}(\.\d{1,2})?%$"

    assert re.match(size_pattern, memory_info.total)
    assert re.match(size_pattern, memory_info.used)
    assert re.match(percentage_pattern, memory_info.percentage)
    assert re.match(size_pattern, memory_info.swap.total)
    assert re.match(size_pattern, memory_info.swap.used)
    assert re.match(percentage_pattern, memory_info.swap.percentage)


def test_get_disk_usage():
    disk_info = get_disk_usage()
    assert isinstance(disk_info, Disk)

    size_pattern = r"^\d+\.\d{2}(B|KB|MB|GB|TB|PB)$"

    assert re.match(size_pattern, disk_info.total_read)
    assert re.match(size_pattern, disk_info.total_write)


def test_system_info_endpoint():
    response = client.post("/info", json=[])
    assert response.status_code == 200
    json_data = response.json()
    assert "system" in json_data
    assert "cpu" in json_data
    assert "memory" in json_data
    assert "disk" in json_data