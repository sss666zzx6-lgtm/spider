import asyncio
from curl_cffi import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from typing import Optional, Dict, Any


class BaseSpider:
  """通用异步爬虫基类"""

  def __init__(
      self,
      max_concurrent: int = 5,
      base_url: str = "",
      headers: Optional[Dict[str, str]] = None,
      proxies: Optional[Dict[str, str]] = None,
      timeout: int = 30
  ):
      self.session: Optional[requests.AsyncSession] = None
      self.semaphore = asyncio.Semaphore(max_concurrent)
      self.base_url = base_url.rstrip("/")
      self.headers = headers or {}
      self.proxies = proxies
      self.timeout = timeout

  async def _ensure_session(self):
      """懒加载 Session"""
      if self.session is None:
          self.session = requests.AsyncSession(
              impersonate="chrome",
              headers=self.headers,
              proxies=self.proxies
          )

  @retry(
      stop=stop_after_attempt(3),
      wait=wait_exponential(multiplier=1, min=1, max=10),
      retry=retry_if_exception_type(Exception),
      reraise=True
  )
  async def fetch(self, url: str, method: str = "GET", **kwargs) -> Optional[Any]:
      """通用 HTTP 请求"""
      async with self.semaphore:
          await self._ensure_session()
          full_url = f"{self.base_url}{url}" if url.startswith("/") else url

          if method.upper() == "GET":
              response = await self.session.get(full_url, timeout=self.timeout, **kwargs)
          elif method.upper() == "POST":
              response = await self.session.post(full_url, timeout=self.timeout, **kwargs)
          else:
              raise ValueError(f"不支持的 HTTP 方法：{method}")

          response.raise_for_status()
          return response

  async def close(self):
      """关闭 Session"""
      if self.session:
          await self.session.close()
          self.session = None

  async def __aenter__(self):
      """支持 async with 上下文管理器"""
      await self._ensure_session()
      return self

  async def __aexit__(self, exc_type, exc_val, exc_tb):
      await self.close()




class MySpider(BaseSpider):
  def __init__(self):
      super().__init__(
          max_concurrent=5,
          base_url="https://api.example.com",
          headers={"Authorization": "Bearer xxx"}
      )

  async def get_user_info(self, user_id: int):
      response = await self.fetch(f"/users/{user_id}")
      return response.json()


# 使用方式 1：手动管理
async def main():
  spider = MySpider()
  try:
      data = await spider.get_user_info(123)
  finally:
      await spider.close()

# 使用方式 2：async with（推荐）
async def main():
  async with MySpider() as spider:
      data = await spider.get_user_info(123)
