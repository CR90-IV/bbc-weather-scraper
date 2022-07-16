from math import nan
import requests, json

def append_to_url(base_url,param):
    return "%s%s/" % (base_url,param)

def append_query_to_url(base_url, **kwargs):
    if kwargs:
        base_url += "?" + "&".join(f"{key}={value}" for key, value in kwargs.items())
    return base_url


class RestConsumer(object):

    def __init__(self,base_url, app_key="", append_json=False, append_slash=False):
        self.base_url = base_url if base_url[-1] == '/' else "%s%s" % (base_url,"/")
        self.append_json = append_json
        self.append_slash = append_slash
        self.app_key = app_key

    def __getattr__(self,key):
        new_base = append_to_url(self.base_url,key)
        return self.__class__(base_url=new_base,
                              app_key=self.app_key,
                              append_json=self.append_json,
                              append_slash=self.append_slash)
    
    def __getitem__(self,key):  # This is used for functionality in e.g .StopPoint['940GZZLUSKS'] to get whats contained in []; __getitem___ is called on []
        return self.__getattr__(key)

    def __call__(self, **kwargs):   # object() is shorthand for object.__call__()
        if not self.append_slash:
            self.base_url = self.base_url[:-1]
        if self.append_json:
            self.base_url = "%s%s" % (self.base_url,'.json')
        self.base_url = append_query_to_url(self.base_url, **kwargs)
        print("Calling %s" % self.base_url)
        return self.get(self.base_url,**kwargs)

    def get(self,url,**kwargs):
        if self.app_key == "":
            r = requests.get(url)
        else:
            r = requests.get(url, headers={'app_key': self.app_key})
        return json.loads(r.text)

    def post(self,**kwargs):
        r = requests.post(**kwargs)
        return json.loads(r.text)