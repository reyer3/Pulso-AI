#!/usr/bin/env python3
"""Health check script for Docker container."""

import sys
import asyncio
import aiohttp
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def check_health():
    """Check if the application is healthy."""
    try:
        # Check main health endpoint
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            async with session.get("http://localhost:8000/health") as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info(f"✅ Health check passed: {result}")
                    return 0
                else:
                    logger.error(f"❌ Health check failed: HTTP {response.status}")
                    return 1
                    
    except aiohttp.ClientConnectorError:
        logger.error("❌ Health check failed: Cannot connect to application")
        return 1
    except asyncio.TimeoutError:
        logger.error("❌ Health check failed: Timeout")
        return 1
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(check_health()))
