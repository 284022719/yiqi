import time
from typing import Callable, Dict, Any
from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
import secrets
import hashlib
import hmac
from src.utils.logger import get_logger

logger = get_logger("security")


class SecurityMiddleware(BaseHTTPMiddleware):
    """安全中间件"""
    
    def __init__(
        self,
        app,
        rate_limit_requests: int = 100,
        rate_limit_window: int = 60,
        enable_cors: bool = True,
        enable_rate_limit: bool = True,
        enable_security_headers: bool = True
    ):
        super().__init__(app)
        self.rate_limit_requests = rate_limit_requests
        self.rate_limit_window = rate_limit_window
        self.enable_cors = enable_cors
        self.enable_rate_limit = enable_rate_limit
        self.enable_security_headers = enable_security_headers
        
        # 速率限制存储
        self.rate_limit_store: Dict[str, Dict[str, Any]] = {}
        
        # 清理过期记录的定时器
        self.last_cleanup = time.time()
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """处理请求"""
        start_time = time.time()
        
        try:
            # 获取客户端IP
            client_ip = self._get_client_ip(request)
            
            # 速率限制检查
            if self.enable_rate_limit:
                if not self._check_rate_limit(client_ip):
                    logger.warning(f"速率限制触发: {client_ip}")
                    return JSONResponse(
                        status_code=429,
                        content={"detail": "请求过于频繁，请稍后再试"}
                    )
            
            # 安全检查
            if not self._security_check(request):
                logger.warning(f"安全检查失败: {client_ip} - {request.url}")
                return JSONResponse(
                    status_code=403,
                    content={"detail": "请求被拒绝"}
                )
            
            # 处理请求
            response = await call_next(request)
            
            # 添加安全头
            if self.enable_security_headers:
                self._add_security_headers(response)
            
            # 记录请求日志
            process_time = time.time() - start_time
            logger.info(
                f"{request.method} {request.url.path} - "
                f"{response.status_code} - {process_time:.3f}s - {client_ip}"
            )
            
            return response
            
        except Exception as e:
            logger.error(f"请求处理错误: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={"detail": "内部服务器错误"}
            )
    
    def _get_client_ip(self, request: Request) -> str:
        """获取客户端真实IP"""
        # 检查代理头
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        return request.client.host if request.client else "unknown"
    
    def _check_rate_limit(self, client_ip: str) -> bool:
        """检查速率限制"""
        current_time = time.time()
        
        # 清理过期记录
        if current_time - self.last_cleanup > 60:
            self._cleanup_rate_limit_store(current_time)
            self.last_cleanup = current_time
        
        # 获取客户端记录
        if client_ip not in self.rate_limit_store:
            self.rate_limit_store[client_ip] = {
                "requests": [],
                "blocked_until": 0
            }
        
        client_record = self.rate_limit_store[client_ip]
        
        # 检查是否被阻止
        if current_time < client_record["blocked_until"]:
            return False
        
        # 清理过期的请求记录
        window_start = current_time - self.rate_limit_window
        client_record["requests"] = [
            req_time for req_time in client_record["requests"]
            if req_time > window_start
        ]
        
        # 检查请求数量
        if len(client_record["requests"]) >= self.rate_limit_requests:
            # 阻止客户端
            client_record["blocked_until"] = current_time + 300  # 阻止5分钟
            return False
        
        # 添加当前请求
        client_record["requests"].append(current_time)
        return True
    
    def _cleanup_rate_limit_store(self, current_time: float):
        """清理速率限制存储"""
        window_start = current_time - self.rate_limit_window
        expired_ips = []
        
        for ip, record in self.rate_limit_store.items():
            # 清理过期的请求记录
            record["requests"] = [
                req_time for req_time in record["requests"]
                if req_time > window_start
            ]
            
            # 如果记录为空且不在阻止状态，删除记录
            if not record["requests"] and current_time >= record["blocked_until"]:
                expired_ips.append(ip)
        
        for ip in expired_ips:
            del self.rate_limit_store[ip]
    
    def _security_check(self, request: Request) -> bool:
        """安全检查"""
        # 检查User-Agent
        user_agent = request.headers.get("User-Agent", "")
        if not user_agent or len(user_agent) < 10:
            return False
        
        # 检查请求大小
        content_length = request.headers.get("Content-Length")
        if content_length and int(content_length) > 10 * 1024 * 1024:  # 10MB
            return False
        
        # 检查路径注入
        path = str(request.url.path)
        suspicious_patterns = [
            "..", "//", "\\", "script", "javascript", "vbscript",
            "onload", "onerror", "onclick", "eval(", "document.cookie"
        ]
        
        for pattern in suspicious_patterns:
            if pattern.lower() in path.lower():
                return False
        
        return True
    
    def _add_security_headers(self, response: Response):
        """添加安全头"""
        # 防止点击劫持
        response.headers["X-Frame-Options"] = "DENY"
        
        # XSS保护
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # 内容类型嗅探保护
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # 引用策略
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # 内容安全策略
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
        response.headers["Content-Security-Policy"] = csp
        
        # 权限策略
        response.headers["Permissions-Policy"] = (
            "geolocation=(), microphone=(), camera=()"
        )


class CORSMiddleware(BaseHTTPMiddleware):
    """CORS中间件"""
    
    def __init__(self, app, allow_origins: list = None):
        super().__init__(app)
        self.allow_origins = allow_origins or ["*"]
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """处理CORS"""
        response = await call_next(request)
        
        # 添加CORS头
        origin = request.headers.get("Origin")
        if origin in self.allow_origins or "*" in self.allow_origins:
            response.headers["Access-Control-Allow-Origin"] = origin or "*"
        
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        
        return response


def generate_csrf_token() -> str:
    """生成CSRF令牌"""
    return secrets.token_urlsafe(32)


def verify_csrf_token(token: str, expected_token: str) -> bool:
    """验证CSRF令牌"""
    if not token or not expected_token:
        return False
    
    # 使用时间安全的比较
    return hmac.compare_digest(token, expected_token)


def hash_password(password: str, salt: str = None) -> tuple[str, str]:
    """哈希密码"""
    if salt is None:
        salt = secrets.token_hex(16)
    
    # 使用PBKDF2进行密码哈希
    hash_obj = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000  # 迭代次数
    )
    
    return hash_obj.hex(), salt


def verify_password(password: str, hashed_password: str, salt: str) -> bool:
    """验证密码"""
    new_hash, _ = hash_password(password, salt)
    return hmac.compare_digest(new_hash, hashed_password) 