import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

from XBase.MConstant import PROJECT_BASE_DIR
log_dir = os.path.join(PROJECT_BASE_DIR,'logs')
print(log_dir,'sss')
def setup_global_logger(
        log_dir=log_dir,
        level=logging.INFO,
        max_bytes=10 * 1024 * 1024,  # 单个日志文件最大10MB
        backup_count=5  # 保留5个备份文件
):
    """配置全局全局日志设置，只需在项目入口调用一次"""
    # 创建日志目录
    os.makedirs(log_dir, exist_ok=True)

    # 日志文件名（包含日期）
    log_file = os.path.join(log_dir, f"app_{datetime.now().strftime('%Y%m%d')}.log")
    # 获取根日志器
    logger = logging.getLogger()
    logger.setLevel(level)

    # 避免重复配置
    if logger.handlers:
        return

    # 日志格式（包含时间、级别、模块、行号和消息）
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 文件处理器（带轮转功能）
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # 控制台处理器台处理器（输出到控制台）
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
