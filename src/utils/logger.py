"""日志工具"""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


class OperationLogger:
    """操作日志记录器"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # 按日期创建日志文件
        self.log_file = self.log_dir / f"{datetime.now().strftime('%Y%m%d')}.log"
        
        # 配置 logging
        self.logger = logging.getLogger("ecomagent")
        self.logger.setLevel(logging.DEBUG)
        
        if not self.logger.handlers:
            handler = logging.FileHandler(self.log_file, encoding='utf-8')
            handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            ))
            self.logger.addHandler(handler)
    
    def log_operation(
        self,
        module: str,
        action: str,
        params: Dict[str, Any],
        result: Dict[str, Any],
        level: str = "INFO"
    ):
        """记录操作日志"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "module": module,
            "action": action,
            "params": params,
            "result": result
        }
        
        # 写入 JSON 格式日志
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        
        # 同时写入标准日志
        msg = f"[{module}] {action}: params={params}, result={result}"
        if level == "ERROR":
            self.logger.error(msg)
        elif level == "DEBUG":
            self.logger.debug(msg)
        else:
            self.logger.info(msg)
    
    def log_error(self, module: str, action: str, error: Exception, params: Dict = None):
        """记录错误日志"""
        self.log_operation(
            module=module,
            action=action,
            params=params or {},
            result={"status": "error", "message": str(error)},
            level="ERROR"
        )


# 全局实例
_logger = None

def get_logger() -> OperationLogger:
    """获取全局日志实例"""
    global _logger
    if _logger is None:
        _logger = OperationLogger()
    return _logger
