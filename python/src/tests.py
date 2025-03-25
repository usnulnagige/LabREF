import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

from main import app
from utils.system import (
    get_size, get_system_info, get_cpu_info, get_memory_info, get_disk_usage
)
from schemas.system import System, CPU, Memory, Disk

client = TestClient(app)

def test_get_size():
    assert get_size(1024) == "1.00KB"
    assert get_size(1048576) == "1.00MB"
    assert get_size(1073741824) == "1.00GB"
    assert get_size(500) == "500.00B"

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
    assert "MB" in memory_info.total or "GB" in memory_info.total
    assert "MB" in memory_info.used or "GB" in memory_info.used

def test_get_disk_usage():
    disk_info = get_disk_usage()
    assert isinstance(disk_info, Disk)
    assert "B" in disk_info.total_read
    assert "B" in disk_info.total_write

def test_system_info_endpoint():
    response = client.post("/info", json=[])
    assert response.status_code == 200
    json_data = response.json()
    assert "system" in json_data
    assert "cpu" in json_data
    assert "memory" in json_data
    assert "disk" in json_data