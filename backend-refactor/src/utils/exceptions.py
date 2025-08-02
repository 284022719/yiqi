"""
自定义异常类
"""

from fastapi import HTTPException, status
from typing import Any, Dict, Optional


class APIException(HTTPException):
    """API异常基类"""
    
    def __init__(
        self,
        status_code: int,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=message)
        self.error_code = error_code
        self.details = details or {}


class ValidationException(APIException):
    """数据验证异常"""
    
    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message=message,
            error_code="VALIDATION_ERROR",
            details={"field": field} if field else None
        )


class NotFoundException(APIException):
    """资源未找到异常"""
    
    def __init__(self, resource: str, resource_id: Optional[str] = None):
        message = f"{resource} not found"
        if resource_id:
            message += f" with id: {resource_id}"
        
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=message,
            error_code="NOT_FOUND",
            details={"resource": resource, "resource_id": resource_id}
        )


class DatabaseException(APIException):
    """数据库操作异常"""
    
    def __init__(self, message: str, operation: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            error_code="DATABASE_ERROR",
            details={"operation": operation} if operation else None
        )


class ExternalAPIException(APIException):
    """外部API调用异常"""
    
    def __init__(self, message: str, api_name: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            message=message,
            error_code="EXTERNAL_API_ERROR",
            details={"api_name": api_name} if api_name else None
        )


class AuthenticationException(APIException):
    """认证异常"""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message,
            error_code="AUTHENTICATION_ERROR"
        )


class AuthorizationException(APIException):
    """授权异常"""
    
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message=message,
            error_code="AUTHORIZATION_ERROR"
        )


class RateLimitException(APIException):
    """速率限制异常"""
    
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            message=message,
            error_code="RATE_LIMIT_ERROR"
        ) 