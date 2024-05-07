import requests # type: ignore

import config as c


def http_post(path, body):

  url = f"http://{c.SERVER}:{c.PORT}{path}"
  print(f"http request: {url}\n{str(body)}")
  res = requests.request("POST", url, json=body)
  print(f"http response: {res.status_code}")
  # micropython requests doesn't support `raise_for_status()`
  # res.raise_for_status()
  if res.status_code >= 200 and res.status_code < 300:
    pass
  elif res.status_code >= 300 and res.status_code < 400:
    raise HTTPError("redirect response", res)
  elif res.status_code >= 400 and res.statuscode < 500:
    raise ClientError("4xx client error", res)
  elif res.status_code >= 500 and res.status_code < 600:
    raise ServerError("5xx server error", res)
  else:
    raise HTTPError("unknown response", res)


class HTTPError(Exception):
  pass
class ClientError(HTTPError):
  pass
class ServerError(HTTPError):
  pass


def remote_log(level, value):
  body = {"deviceId": c.DEVICE_ID, "level": level, "value": value}
  http_post("/logger", body)
