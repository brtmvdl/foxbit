import http.client
import hmac
import hashlib
import config
import utils
import json

class Request():
  def __init__(self, method: str = "GET", path: str = "/", body: dict[str, str] = None):
    self.method = method
    self.path = path
    self.body = body

  def getMethod(self) -> str:
    return self.method

  def getPath(self) -> str:
    return self.path

  def getFullPath(self) -> str:
    return config.path_prefix + self.getPath()

  def getSignature(self, timestamp: str, path: str, query: str) -> str:
    secret = f"{timestamp}GET{path}{query}"
    sig = config.secret
    return hmac.new(bytes(secret, encoding = 'ascii'), bytes(sig, encoding = 'ascii'), hashlib.sha256).hexdigest()

  def getHeaders(self, timestamp: str = str(utils.getTimestamp())) -> dict[str, str]:
    return {
      "Host": self.getHost(),
      "Content-Type": "application/json",
      "X-FB-ACCESS-KEY": config.key,
      "X-FB-ACCESS-TIMESTAMP": timestamp,
      "X-FB-ACCESS-SIGNATURE": self.getSignature(timestamp, self.getFullPath(), query = ""),
    }

  def getHeadersList(self) -> list[str]:
    headers = self.getHeaders()
    return [f"{key}: {value}" for key, value in headers.items()]

  def getBody(self) -> dict[str, str]:
    return self.body

  def getBodyString(self) -> str:
    body = self.getBody()
    if (body is None):
      return ""
    return str(body)

  def getHost(self) -> str:
    return config.host

  def getVersion(self) -> str:
    return "1.1"

  def __str__(self) -> str:
    lines = []
    lines.append(f"{self.getMethod()} {self.getFullPath()} HTTP/{self.getVersion()}")
    lines.extend(self.getHeadersList())
    lines.append(self.getBodyString())
    return "\r\n".join(lines)

class Response():
  def __init__(self, req: Request, res: http.client.HTTPResponse):
    self.req = req
    self.res = res

  def getData(self):
    return json.loads(self.res.read())
  
  def __str__(self) -> str:
    lines = []
    lines.append(f"HTTP/{self.res.version} {self.res.status} {self.res.reason}")
    lines.append(str(self.res.headers))
    lines.append(str(self.res.read()))
    return "\r\n".join(lines)

def run(req: Request) -> Response:
  host, method, path, body, headers = req.getHost(), req.getMethod(), req.getFullPath(), req.getBodyString(), req.getHeaders()
  print("request", host, method, path, body, headers)
  conn = http.client.HTTPSConnection(host)
  conn.request(method, path, body, headers)
  return Response(req, conn.getresponse())
