# -*- coding: utf-8 -*-
"""
飞书消息监听服务 - 改进版
参考 monitor_service.py 实现，支持日志监控、图片缓存、触发词识别
"""
import json
import re
import subprocess
import sys
import threading
import time
from collections import deque
from datetime import datetime, timedelta
from pathlib import Path
from threading import Lock

# 禁用输出缓冲，确保日志实时显示
sys.path.insert(0, str(Path(__file__).parent))

# 导入后设置无缓冲输出
import builtins
_original_print = builtins.print

def _flush_print(*args, **kwargs):
    """强制刷新的 print"""
    kwargs['flush'] = True
    return _original_print(*args, **kwargs)

builtins.print = _flush_print
from utils.logger import get_logger
from utils.feishu import send_text, send_image


def now():
    """获取当前时间字符串"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(level: str, message: str):
    """统一日志输出格式 - 使用ASCII字符避免乱码"""
    # 替换常见中文字符为英文
    replacements = {
        '✓': '[OK]',
        '✗': '[ERR]',
        '：': ': ',
        '，': ', ',
        '。': '.',
    }
    for cn, en in replacements.items():
        message = message.replace(cn, en)
    print(f"[{now()}] [{level}] {message}", flush=True)


class ImageCache:
    """图片缓存管理器 - 参考 monitor_service.py 的 ImageCache"""
    
    def __init__(self, cache_file: str = "temp/image_cache.json", expire_minutes: int = 10):
        self.cache_file = Path(cache_file)
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        self.expire_minutes = expire_minutes
        self.cache = {}  # user_id -> {image_path, timestamp}
        self.timers = {}  # user_id -> timer
        self.lock = Lock()
        self._load_cache()
    
    def _load_cache(self):
        """从文件加载缓存"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    now = datetime.now()
                    valid_count = 0
                    expired_count = 0
                    
                    for k, v in data.items():
                        try:
                            timestamp = datetime.fromisoformat(v['timestamp'])
                            if timestamp + timedelta(minutes=self.expire_minutes) > now:
                                self.cache[k] = v
                                valid_count += 1
                            else:
                                expired_count += 1
                        except Exception:
                            pass
                    
                    if expired_count > 0:
                        log("Cache", f"加载缓存: {valid_count}个有效, {expired_count}个已过期")
                    else:
                        log("Cache", f"加载缓存: {valid_count}个有效")
            except Exception as e:
                log("Error", f"加载缓存文件失败: {e}")
                self.cache = {}
    
    def _save_cache(self):
        """保存缓存到文件"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            log("Error", f"保存缓存失败: {e}")
    
    def set(self, user_id: str, image_path: str):
        """设置缓存，启动计时器（参考 monitor_service.py）"""
        with self.lock:
            # 取消旧计时器
            if user_id in self.timers:
                self.timers[user_id].cancel()
            
            # 设置新缓存
            self.cache[user_id] = {
                'image_path': image_path,
                'timestamp': datetime.now().isoformat()
            }
            self._save_cache()
            
            # 启动新计时器
            timer = threading.Timer(self.expire_minutes * 60, self._expire, args=[user_id])
            self.timers[user_id] = timer
            timer.start()
            
            log("Cache", f"✓ 缓存图片: user={user_id} -> {image_path}")
    
    def get(self, user_id: str) -> str:
        """获取缓存的图片路径"""
        with self.lock:
            if user_id not in self.cache:
                return None
            
            data = self.cache[user_id]
            try:
                timestamp = datetime.fromisoformat(data['timestamp'])
                if datetime.now() - timestamp > timedelta(minutes=self.expire_minutes):
                    self._expire(user_id)
                    return None
                return data['image_path']
            except Exception:
                return None
    
    def _expire(self, user_id: str):
        """缓存过期处理"""
        with self.lock:
            if user_id in self.cache:
                log("Cache", f"✗ 缓存过期: user={user_id}")
                del self.cache[user_id]
                self._save_cache()
            if user_id in self.timers:
                del self.timers[user_id]
    
    def delete(self, user_id: str):
        """手动删除缓存"""
        with self.lock:
            if user_id in self.timers:
                self.timers[user_id].cancel()
                del self.timers[user_id]
            if user_id in self.cache:
                log("Cache", f"✗ 清除缓存: user={user_id}")
                del self.cache[user_id]
                self._save_cache()
    
    def list_active(self) -> list:
        """列出所有活跃缓存"""
        with self.lock:
            return list(self.cache.keys())


class TestModeCache:
    """测试模式缓存 - 10分钟内收到'测试'口令则处理，否则过期"""
    
    def __init__(self, expire_minutes: int = 10):
        self.cache = {}  # user_id -> {image_path, timestamp, timer}
        self.lock = Lock()
        self.expire_minutes = expire_minutes
    
    def set(self, user_id: str, image_path: str):
        """设置测试模式缓存，启动计时器"""
        with self.lock:
            # 取消旧计时器
            if user_id in self.cache and 'timer' in self.cache[user_id]:
                self.cache[user_id]['timer'].cancel()
            
            # 设置新缓存
            self.cache[user_id] = {
                'image_path': image_path,
                'timestamp': datetime.now().isoformat()
            }
            
            # 启动新计时器
            timer = threading.Timer(self.expire_minutes * 60, self._expire, args=[user_id])
            self.cache[user_id]['timer'] = timer
            timer.start()
            
            log("TestMode", f"✓ 测试模式缓存: user={user_id}, path={image_path}, 10分钟后过期")
    
    def get(self, user_id: str) -> str:
        """获取测试模式缓存的图片路径"""
        with self.lock:
            if user_id not in self.cache:
                return None
            return self.cache[user_id].get('image_path')
    
    def _expire(self, user_id: str):
        """测试模式缓存过期处理"""
        with self.lock:
            if user_id in self.cache:
                log("TestMode", f"✗ 测试模式缓存过期: user={user_id}")
                if 'timer' in self.cache[user_id]:
                    self.cache[user_id]['timer'].cancel()
                del self.cache[user_id]
    
    def delete(self, user_id: str):
        """手动删除测试模式缓存"""
        with self.lock:
            if user_id in self.cache:
                log("TestMode", f"✗ 测试模式缓存已删除: user={user_id}")
                if 'timer' in self.cache[user_id]:
                    self.cache[user_id]['timer'].cancel()
                del self.cache[user_id]
    
    def list_active(self) -> list:
        """列出所有活跃缓存"""
        with self.lock:
            return list(self.cache.keys())


class TriggerConfig:
    """触发词配置管理"""
    
    def __init__(self, config_path: str = "config/triggers.json"):
        # 从 src 目录向上找到项目根目录
        project_root = Path(__file__).parent.parent
        self.config_file = project_root / config_path
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        if not self.config_file.exists():
            log("Config", "使用默认触发词配置")
            return self._default_config()
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                trigger_count = sum(len(t.get('keywords', [])) for t in config.get('triggers', {}).values())
                log("Config", f"加载配置: {len(config.get('triggers', {}))}个触发器, {trigger_count}个关键词")
                return config
        except Exception as e:
            log("Error", f"加载触发词配置失败: {e}")
            return self._default_config()
    
    def _default_config(self) -> dict:
        return {
            "triggers": {
                "image": {"script": "generate_images.py", "keywords": ["作图", "生图", "生9图", "9图"]},
                "video": {"script": "generate_video.py", "keywords": ["生视频", "做视频", "视频"]},
                "test": {"script": "test_mode.py", "keywords": ["测试"]}
            },
            "settings": {"cache_expire_minutes": 10, "case_sensitive": False}
        }
    
    def check_trigger(self, content: str) -> tuple:
        """检查触发词，返回 (trigger_id, trigger_info)"""
        content = content.strip()
        settings = self.config.get('settings', {})
        case_sensitive = settings.get('case_sensitive', False)
        
        check_content = content if case_sensitive else content.lower()
        
        for trigger_id, trigger_info in self.config.get('triggers', {}).items():
            for keyword in trigger_info.get('keywords', []):
                check_keyword = keyword if case_sensitive else keyword.lower()
                if check_keyword in check_content:
                    return (trigger_id, trigger_info)
        return (None, None)
    
    def get_cache_expire(self) -> int:
        return self.config.get('settings', {}).get('cache_expire_minutes', 10)


class FeishuMonitor:
    """飞书消息监听器 - 参考 monitor_service.py 实现"""
    
    def __init__(self, log_file: str = "logs/gateway.log"):
        # 项目根目录
        self.project_root = Path(__file__).parent.parent
        self.log_file = self.project_root / log_file
        self.triggers = TriggerConfig()
        self.cache = ImageCache(
            cache_file=str(self.project_root / "temp" / "image_cache.json"),
            expire_minutes=self.triggers.get_cache_expire()
        )
        self.logger = get_logger()
        self.running = False
        
        # 日志缓冲区（最近50行）
        self.buffer = deque(maxlen=50)
        
        # 防重复触发机制（参考 monitor_service.py）
        self.processing_users = set()
        self.processing_lock = Lock()
        
        # 正则表达式模式
        # 1. 检测 session 文件路径
        self.session_pattern = re.compile(r'sessionFile=([\w\-\\\.:\/]+\.jsonl?)')
        # 2. 检测图片下载
        self.image_pattern = re.compile(r'downloaded image media, saved to (.+\.(jpg|jpeg|png|webp))', re.IGNORECASE)
        # 3. 检测用户ID
        self.user_pattern = re.compile(r'received message from (ou_[a-f0-9]+)')
        
        # 确保日志文件存在
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_file.exists():
            self.log_file.touch()
        
        log("Init", f"项目根目录: {self.project_root}")
        log("Init", f"日志文件: {self.log_file}")
        log("Init", f"缓存过期时间: {self.triggers.get_cache_expire()}分钟")
    
    def _clean_line(self, line: str) -> str:
        """去除 ANSI 颜色代码"""
        return re.sub(r'\x1b\[[0-9;]*m', '', line)
    
    def _find_recent_user_id(self) -> str:
        """从缓冲区找最近的用户ID"""
        for line in reversed(self.buffer):
            match = self.user_pattern.search(line)
            if match:
                return match.group(1)
        return None
    
    def parse_line(self, line: str):
        """解析单行日志 - 参考 monitor_service.py"""
        start_time = time.time()
        log("Debug", f"[Parse] 开始解析日志行...")
        clean_line = self._clean_line(line)
        self.buffer.append(clean_line)
        
        # 调试输出
        safe_line = ''.join(c if c.isprintable() or c.isspace() else '?' for c in clean_line[:100])
        log("Debug", f"读取行: {safe_line}...")
        
        # 1. 检测 session 文件路径
        session_match = self.session_pattern.search(clean_line)
        if session_match:
            session_file = session_match.group(1)
            # 提取日志行中的时间戳
            time_match = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})', clean_line)
            log_timestamp = time_match.group(1) if time_match else None
            log("Debug", f"[Session] 检测到 session 文件: {session_file}, time={log_timestamp}")
            self._check_session_file(session_file, log_timestamp)
            return
        
        # 2. 检测图片下载
        img_match = self.image_pattern.search(clean_line)
        if img_match:
            image_path = img_match.group(1)
            user_id = self._find_recent_user_id()
            if user_id:
                self.cache.set(user_id, image_path)
                log("Debug", f"[Image] 缓存图片成功: user={user_id}, path={image_path}")
            else:
                log("Warn", f"检测到图片但未找到用户ID: {image_path}")
            return
        
        # 3. 检测用户消息（记录用户ID到缓冲区）
        msg_match = self.user_pattern.search(clean_line)
        if msg_match:
            user_id = msg_match.group(1)
            log("Debug", f"检测到用户消息: {user_id}")
            return
        
        # 耗时统计
        elapsed = time.time() - start_time
        if elapsed > 0.1:  # 超过100ms才记录
            log("Debug", f"[Perf] parse_line 耗时: {elapsed*1000:.1f}ms")
        else:
            log("Debug", f"[Perf] parse_line 耗时: {elapsed*1000:.1f}ms (正常)")
    
    def _check_session_file(self, session_file: str, log_timestamp: str = None):
        """检查 session 文件，提取最新消息 - 参考 monitor_service.py
        
        Args:
            session_file: session 文件路径
            log_timestamp: 日志中的时间戳（精确到秒），只查找该时间之后的消息
        """
        start_time = time.time()
        log("Debug", f"[Session] 开始检查 session 文件: {session_file}")
        try:
            # 检查是否有缓存的图片
            if not self.cache.cache:
                log("Debug", "[Session] 无缓存图片，跳过 session 检查")
                return
            
            session_path = Path(session_file)
            if not session_path.exists():
                log("Warn", f"Session 文件不存在: {session_file}")
                return
            
            log("Session", f"检查 session 文件: {session_file}")
            log("Session", f"日志时间戳: {log_timestamp}")
            
            # 读取文件最后 50KB
            file_size = session_path.stat().st_size
            read_size = min(51200, file_size)
            
            read_start = time.time()
            with open(session_path, 'r', encoding='utf-8', errors='replace') as f:
                f.seek(file_size - read_size)
                content = f.read()
            
            read_elapsed = time.time() - read_start
            log("Debug", f"[Session] 读取文件耗时: {read_elapsed*1000:.1f}ms, size={read_size}bytes")
            
            # 按行分割
            lines = content.strip().split('\n')
            
            # 从后向前查找，找到匹配 log_timestamp 的消息
            for line in reversed(lines):
                if not line.strip():
                    continue
                try:
                    msg = json.loads(line)
                    
                    # 检查消息时间是否匹配（精确到秒）
                    msg_timestamp = msg.get('timestamp', '')
                    if log_timestamp and not msg_timestamp.startswith(log_timestamp):
                        continue
                    
                    # 只处理用户消息
                    if msg.get('type') == 'message' and msg.get('message', {}).get('role') == 'user':
                        # 提取消息内容
                        message_data = msg.get('message', {})
                        content_blocks = message_data.get('content', [])
                        
                        text_content = ""
                        for block in content_blocks:
                            if block.get('type') == 'text':
                                text_content += block.get('text', '')
                        
                        log("Session", f"找到消息: {text_content[:100]}...")
                        
                        # 处理消息格式
                        user_id = None
                        message_text = None
                        
                        # 从 JSON metadata 中提取 sender_id（适用于所有消息类型）
                        sender_match = re.search(
                            r'"sender_id":\s*"(ou_[a-f0-9]+)"',
                            text_content
                        )
                        if sender_match:
                            user_id = sender_match.group(1)
                        
                        # 尝试匹配普通格式（图片消息等）
                        dm_match = re.search(
                            r'Feishu\[default\] DM from (ou_\w+): ([^\n]+)',
                            text_content
                        )
                        if dm_match:
                            user_id = dm_match.group(1)
                            message_text = dm_match.group(2).strip()
                            # 去掉后面的 metadata 和 JSON
                            message_text = re.sub(r'Conversation info.*$', '', message_text, flags=re.DOTALL).strip()
                            log("Session", "解析到普通格式消息")
                        
                        # 尝试匹配队列消息格式
                        elif '[Queued messages' in text_content:
                            # 提取 Queued #N 后面的实际消息内容
                            queued_match = re.search(
                                r'Queued #\d+\s*\n.*?```\s*\n\s*\}\s*```\s*\n\n(.+?)(?:\n\n|$)',
                                text_content,
                                re.DOTALL
                            )
                            if queued_match:
                                message_text = queued_match.group(1).strip()
                                log("Session", "解析到队列消息格式")
                        
                        # 处理提取到的消息
                        if user_id and message_text:
                            elapsed = time.time() - start_time
                            log("Debug", f"[Session] 提取消息成功: user={user_id}, msg={message_text[:50]}..., 耗时={elapsed*1000:.1f}ms")
                            self._process_message(user_id, message_text)
                        return  # 只处理最新消息
                        
                except json.JSONDecodeError:
                    continue
                    
        except Exception as e:
            total_elapsed = time.time() - start_time
            log("Error", f"读取 session 文件错误: {e}, 总耗时={total_elapsed*1000:.1f}ms")
    
    def _process_message(self, user_id: str, message_text: str):
        """处理用户消息，检查触发词并执行对应操作"""
        start_time = time.time()
        log("Debug", f"[Process] 开始处理消息: user={user_id}, msg={message_text[:50]}...")
        
        # 检查该用户是否有缓存的图片
        if user_id not in self.cache.cache:
            log("Session", f"用户 {user_id} 无缓存图片，忽略")
            return
        
        # 防重复触发检查（参考 monitor_service.py）
        with self.processing_lock:
            if user_id in self.processing_users:
                log("Process", f"用户 {user_id} 正在处理中，跳过重复触发")
                return
        
        # 检查触发词
        trigger_start = time.time()
        trigger_id, trigger_info = self.triggers.check_trigger(message_text)
        
        if trigger_id:
            elapsed = time.time() - start_time
            log("Debug", f"[Trigger] 检测到触发词! user={user_id}, trigger={trigger_id}, msg='{message_text}', 耗时={elapsed*1000:.1f}ms")
            log("Trigger", f"✓ 检测到触发词! user={user_id}, trigger={trigger_id}, msg='{message_text}'")
            log("Trigger", f"当前缓存用户: {self.cache.list_active()}")
            
            # 标记为处理中
            with self.processing_lock:
                self.processing_users.add(user_id)
            
            try:
                # 重置计时器（给用户更多时间等待生成）
                image_path = self.cache.get(user_id)
                if image_path:
                    cache_elapsed = time.time() - start_time
                    log("Debug", f"[Trigger] 重置缓存耗时: {cache_elapsed*1000:.1f}ms")
                    self.cache.set(user_id, image_path)
                
                # 执行对应脚本
                script = trigger_info.get('script')
                if script:
                    script_elapsed = time.time() - start_time
                    log("Debug", f"[Trigger] 准备执行脚本: {script}, 耗时={script_elapsed*1000:.1f}ms")
                    self._call_script(script, user_id, image_path)
                else:
                    log("Error", f"触发器 {trigger_id} 未配置脚本")
            finally:
                # 执行后清除缓存和标记
                self.cache.delete(user_id)
                with self.processing_lock:
                    self.processing_users.discard(user_id)
        else:
            log("Debug", f"未检测到触发词: {message_text}")
        
        total_elapsed = time.time() - start_time
        log("Debug", f"[Process] 消息处理完成: user={user_id}, 总耗时={total_elapsed*1000:.1f}ms")
    
    def _call_script(self, script: str, user_id: str, image_path: str) -> bool:
        """调用生成脚本 - 参考 monitor_service.py"""
        start_time = time.time()
        if not image_path:
            log("Error", f"无缓存图片: {user_id}")
            return False
        
        script_path = self.project_root / "src" / script
        if not script_path.exists():
            log("Error", f"脚本不存在: {script_path}")
            return False
        
        elapsed = time.time() - start_time
        log("Debug", f"[Script] 脚本准备完成: {script}, 耗时={elapsed*1000:.1f}ms")
        
        try:
            # 使用明确的 Python 路径，确保依赖可用
            python_exe = sys.executable
            cmd = [
                python_exe,
                str(script_path),
                "--image", image_path,
                "--user_id", user_id
            ]
            
            # 根据脚本类型添加参数
            if script == "generate_images.py":
                # generate_images.py 只需要 --image 和 --user_id，不需要额外参数
                pass
            elif script == "generate_video_v2.py":
                # V2版本：3图3视频合成
                cmd = [
                    sys.executable,
                    str(script_path),
                    "--image", image_path,
                    "--user_id", user_id,
                    "--duration", "5",
                    "--resolution", "480p"
                ]
            
            # 记录命令行
            log("Debug", f"[Script] 执行命令: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                cwd=str(self.project_root),
                timeout=1800 if "generate_video" in script else 600
            )
            
            elapsed = time.time() - start_time
            log("Debug", f"[Script] 脚本执行完成: {script}, 耗时={elapsed*1000:.1f}ms, returncode={result.returncode}")
            
            # 安全解码输出（处理 Windows 编码问题）
            def safe_decode(data: bytes) -> str:
                """尝试多种编码解码字节数据"""
                for encoding in ['utf-8', 'gbk', 'gb2312', 'utf-16', 'latin-1']:
                    try:
                        return data.decode(encoding, errors='replace')
                    except (UnicodeDecodeError, LookupError):
                        continue
                return data.decode('utf-8', errors='replace')  # 最后尝试
            
            stdout_str = safe_decode(result.stdout)
            stderr_str = safe_decode(result.stderr)
            
            log("Script", f"脚本输出:\n{stdout_str}")
            
            if result.returncode == 0:
                log("Script", f"✓ 脚本执行成功: {script}")
                # 解析结果并发送消息
                parse_start = time.time()
                self._parse_result(user_id, stdout_str, script)
                parse_elapsed = time.time() - parse_start
                log("Debug", f"[Script] 解析结果耗时: {parse_elapsed*1000:.1f}ms")
                return True
            else:
                log("Error", f"脚本执行失败: {stderr_str}")
                send_text(user_id, "生成失败，请稍后重试~")
                return False
                
        except subprocess.TimeoutExpired:
            log("Error", f"脚本执行超时: {script}")
            send_text(user_id, "生成超时，请稍后重试~")
            return False
        except Exception as e:
            log("Error", f"调用脚本错误: {e}")
            send_text(user_id, f"生成出错: {str(e)}")
            return False
    
    def _parse_result(self, user_id: str, stdout: str, script: str):
        """解析生成结果并发送给用户 - 参考 monitor_service.py"""
        start_time = time.time()
        # 确定结果标记
        if "generate_images.py" in script:
            marker = "[GENERATION_RESULT]"
        elif "generate_video" in script:
            # 支持 generate_video.py 和 generate_video_v2.py
            marker = "[VIDEO_RESULT]"
        elif "test_mode.py" in script:
            marker = "[TEST_MODE_RESULT]"
        else:
            return
        
        log("Parse", f"Looking for marker: {marker}")
        found = False
        
        for line in stdout.split('\n'):
            if marker in line:
                elapsed = time.time() - start_time
                log("Debug", f"[Parse] 找到结果标记: {line[:100]}..., 耗时={elapsed*1000:.1f}ms")
                found = True
                log("Parse", f"Found marker in line: {line[:100]}...")
                try:
                    json_str = line.split(marker)[1].strip()
                    log("Parse", f"JSON string: {json_str[:200]}...")
                    result = json.loads(json_str)
                    
                    status = result.get('status')
                    log("Parse", f"Parsed status: {status}")
                    
                    if status == 'success':
                        log("Result", f"Success: {user_id}")
                        self._send_results_to_user(user_id, result, script)
                    else:
                        log("Error", f"Failed: {user_id}, status={status}")
                        error_msg = result.get('error', {}).get('message', '生成失败')
                        send_text(user_id, f"生成失败: {error_msg}")
                    
                    return
                except Exception as e:
                    log("Error", f"Parse error: {e}, line: {line[:200]}")
                    send_text(user_id, "处理结果时出错，请稍后重试~")
        
        if not found:
            log("Error", f"Marker not found in output")
    
    def _send_results_to_user(self, user_id: str, result: dict, script: str):
        """发送生成的文件给用户 - 参考 monitor_service.py
        
        注意：generate_images.py 已经逐张发送，这里只处理视频和汇总
        """
        if "test_mode.py" in script:
            # 测试模式：已保存图片并发送回飞书
            output_path = result.get('output_path')
            status = result.get('status')
            
            if status == 'success' and output_path:
                log("Result", f"测试模式成功: user={user_id}, output={output_path}")
                send_text(user_id, f"测试模式成功！图片已保存到: {output_path}")
            else:
                error_msg = result.get('error', {}).get('message', '测试失败')
                log("Error", f"测试模式失败: {error_msg}")
                send_text(user_id, f"测试失败: {error_msg}")
            return
            
        if "generate_video" in script:
            # 视频生成结果 - 支持 generate_video.py 和 generate_video_v2.py
            # V2版本: merged_video, videos, scenes
            # V1版本: video_path, scene_path
            file_path = result.get('merged_video') or result.get('video_path')
            scene_path = result.get('scene_path')
            output_dir = result.get('output_dir', 'N/A')
            
            caption = "视频生成完成！🎬"
            
            # 转换为绝对路径（相对于项目根目录）
            if file_path:
                file_path = str(self.project_root / file_path)
            if scene_path:
                scene_path = str(self.project_root / scene_path)
            
            if file_path and Path(file_path).exists():
                file_size = Path(file_path).stat().st_size / (1024 * 1024)  # MB
                log("Send", f"发送视频文件: {file_path} ({file_size:.1f} MB)")
                
                # 检查文件大小（飞书限制 10MB）
                if file_size > 9.5:
                    log("Error", f"视频文件过大: {file_size:.1f} MB > 9.5 MB")
                    send_text(user_id, f"视频生成完成，但文件过大 ({file_size:.1f} MB)，无法发送。请使用低分辨率或短时间参数重新生成。")
                    return
                
                # 先发送场景图预览
                if scene_path and Path(scene_path).exists():
                    scene_size = Path(scene_path).stat().st_size / (1024 * 1024)
                    if scene_size > 9.5:
                        log("Warn", f"场景图过大，跳过发送: {scene_size:.1f} MB")
                    else:
                        send_image(user_id, scene_path, "Scene Preview")
                
                # 再发送视频
                log("Send", f"Sending video to user...")
                send_start = time.time()
                send_success = send_image(user_id, file_path, caption)
                send_elapsed = time.time() - send_start
                log("Debug", f"[Send] 发送视频耗时: {send_elapsed*1000:.1f}ms, success={send_success}")
                if not send_success:
                    log("Error", f"Failed to send video via Feishu")
                    # 如果发送失败，提供文件路径给用户
                    abs_path = Path(file_path).absolute()
                    send_text(user_id, f"Video generated but failed to send via Feishu. Please check the file manually: {abs_path}")
            else:
                log("Error", f"Video file not found: {file_path}")
                send_text(user_id, "Video generation completed but file not found")
        else:
            # 图片生成结果 - generate_images.py 已经逐张发送，这里只记录日志
            success_count = result.get('success_count', 0)
            total = result.get('total', 0)
            log("Send", f"图片生成完成: {success_count}/{total}，已由脚本逐张发送")
    
    def _check_log(self):
        """检查日志文件更新 - 参考 monitor_service.py"""
        try:
            current_size = self.log_file.stat().st_size
            if current_size <= self.last_size:
                return
            
            # 尝试不同编码，使用共享模式打开文件（允许其他进程写入）
            new_lines = []
            for encoding in ['utf-8', 'utf-16', 'gbk']:
                try:
                    # Windows: 使用 FILE_SHARE_READ | FILE_SHARE_WRITE 模式
                    import msvcrt
                    import os
                    
                    # 以共享读写模式打开文件
                    fh = os.open(str(self.log_file), os.O_RDONLY | os.O_BINARY)
                    try:
                        os.lseek(fh, self.last_size, os.SEEK_SET)
                        data = os.read(fh, current_size - self.last_size)
                        if data:
                            try:
                                text = data.decode(encoding, errors='replace')
                                new_lines = text.splitlines()
                                break
                            except:
                                continue
                    finally:
                        os.close(fh)
                except Exception:
                    continue
            
            if not new_lines:
                # 回退到普通模式（可能被占用）
                for encoding in ['utf-8', 'utf-16', 'gbk']:
                    try:
                        with open(self.log_file, 'r', encoding=encoding, errors='replace') as f:
                            f.seek(self.last_size)
                            new_lines = f.readlines()
                            new_lines = [l.rstrip('\n\r') for l in new_lines]
                        break
                    except PermissionError:
                        # 文件被占用，跳过本次检查
                        return
                    except:
                        continue
            
            self.last_size = current_size
            
            for line in new_lines:
                line = line.strip()
                if line:
                    self.parse_line(line)
                    
        except Exception as e:
            log("Error", f"读取日志错误: {e}")
    
    def start(self):
        """开始监控 - 参考 monitor_service.py"""
        print("=" * 60)
        print("  EcomAgent 飞书消息监听服务")
        print("=" * 60)
        print("")
        
        log("Start", "监听服务启动")
        log("Start", f"日志文件: {self.log_file}")
        log("Start", f"当前缓存用户: {self.cache.list_active()}")
        log("Start", "等待 Gateway 日志...")
        print("")
        
        self.running = True
        self.last_size = self.log_file.stat().st_size
        
        try:
            while self.running:
                start_time = time.time()
                self._check_log()
                elapsed = time.time() - start_time
                if elapsed > 0.6:  # 超过600ms才记录
                    log("Debug", f"[Perf] _check_log 耗时: {elapsed*1000:.1f}ms")
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("")
            log("Stop", "监听服务停止")
    
    def stop(self):
        """停止监控"""
        self.running = False


def main():
    """主函数"""
    monitor = FeishuMonitor()
    monitor.start()


if __name__ == '__main__':
    main()