"""
Rate limiting middleware for API protection
"""

import logging
from fastapi import Request, HTTPException
from app.core.config import settings

logger = logging.getLogger(__name__)

# Try to import slowapi
try:
    from slowapi import Limiter
    from slowapi.util import get_remote_address
    from slowapi.errors import RateLimitExceeded
    
    # Initialize rate limiter
    # Note: app.state.limiter will be set in main.py
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=[f"{settings.RATE_LIMIT_PER_MINUTE}/minute"] if settings.RATE_LIMIT_ENABLED else []
    )
    
    
    def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
        """Custom handler for rate limit exceeded"""
        logger.warning(f"Rate limit exceeded for {get_remote_address(request)}")
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Rate limit exceeded",
                "message": "Too many requests. Please try again later.",
                "retry_after": exc.retry_after
            }
        )
except ImportError:
    # Rate limiting not available
    limiter = None
    RateLimitExceeded = None
    
    def rate_limit_exceeded_handler(request: Request, exc):
        """Dummy handler when slowapi is not installed"""
        pass

