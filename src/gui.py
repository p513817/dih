import rich
from rich import box
from rich.align import Align
from rich.text import Text
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import (
    Progress, 
    TextColumn, 
    BarColumn, 
    TaskProgressColumn, 
    TimeRemainingColumn, 
    TimeElapsedColumn, 
    FileSizeColumn,
    SpinnerColumn
)

LOGO = \
r'''
██████╗ ██╗██╗  ██╗
██╔══██╗██║██║  ██║
██║  ██║██║███████║
██║  ██║██║██╔══██║
██████╔╝██║██║  ██║
╚═════╝ ╚═╝╚═╝  ╚═╝
'''

def rich_logo(ver:str=""):
    console = Console()
    logo = LOGO if ver=="" else f"{LOGO}v{ver}"
    panel = Panel(Text(logo, justify="left"), box=box.SIMPLE_HEAD)
    console.print(panel)

class RichTable:
    """A wrapper for Rich Table, more easy to use"""
    
    def __init__(self):
        self.console = Console()
        self.table = Table()
        self.headers = []

    def define(self, headers: list):
        """Define the table"""
        self.headers = headers
        for header in headers:
            self.table.add_column(header)
    
    def update(self, values: tuple[str], style=""):
        """Update content into table

        Args:
            values (tuple[str]): the value to insert
            style (str, optional): setup color. Defaults to "".
        """
        ss, es = style, style
        if style:
            ss, es = f'[{style}]', f'[/{style}]'
        self.table.add_row(*[ f"{ss}{value}{es}" for value in values ])

    def print_out(self):
        """Show the table"""
        # self.console.clear()
        # self.console.print(Align(self.table, align='center'))
        self.console.print(self.table)

def get_rich_progress():
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn() )
        
if __name__ == "__main__":
    rt = RichTable()
    rt.define(['Name', 'Age'])
    rt.update(('Max', '27'))
    rt.print_out()