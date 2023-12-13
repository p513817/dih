import pytest
import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)

from src.dih.gui import RichTable

@pytest.fixture
def rich_table():
    return RichTable()

def test_define_header(rich_table):
    headers = ["Name", "Age", "City"]
    rich_table.define(headers)
    assert rich_table.headers == headers

def test_update_and_print_out(rich_table, capsys):
    headers = ["Name", "Age", "City"]
    rich_table.define(headers)

    # 添加数据并打印输出
    rich_table.update(("Alice", "30", "New York"))
    rich_table.update(("Bob", "25", "Los Angeles"))
    rich_table.print_out()

    # 检查输出是否包含表格标题和数据行
    captured = capsys.readouterr()
    assert "Alice" in captured.out
    assert "Bob" in captured.out
    assert "30" in captured.out
    assert "25" in captured.out
    assert "New York" in captured.out
    assert "Los Angeles" in captured.out