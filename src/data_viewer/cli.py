"""
EcomAgent CLI 工具
"""

import click
import sys
from pathlib import Path

# 添加父目录到路径
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from data_viewer.main import run_server


@click.group()
@click.version_option(version="0.1.0", prog_name="ecomagent")
def cli():
    """EcomAgent - 电商数据抓取与分析平台"""
    pass


@cli.command()
@click.option("--host", default="0.0.0.0", help="服务监听地址")
@click.option("--port", default=8000, help="服务监听端口")
@click.option("--reload", is_flag=True, help="启用热重载（开发模式）")
def serve(host, port, reload):
    """启动 Web UI 服务"""
    run_server(host, port)


@cli.command()
def status():
    """查看系统状态"""
    from data_viewer.main import get_stats
    
    stats = get_stats()
    
    print("\n" + "="*60)
    print("EcomAgent 系统状态")
    print("="*60)
    
    print("\nAmazon:")
    print(f"  产品数：{stats['amazon']['products']}")
    print(f"  销售记录：{stats['amazon']['sales']}")
    print(f"  最后更新：{stats['amazon']['last_updated']}")
    
    print("\nTikTok:")
    print(f"  产品数：{stats['tiktok']['products']}")
    print(f"  销售记录：{stats['tiktok']['sales']}")
    print(f"  最后更新：{stats['tiktok']['last_updated']}")
    
    print("="*60 + "\n")


if __name__ == "__main__":
    cli()
