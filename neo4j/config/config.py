


class Config:

    def __init__(self):
        """
        Load configuration
        """
        self.config= {
            "netconf" : { "credentials": {"user":"user", "pass":"pass"} }

        }


    def get(self,param):
        """
        safeGet a config param
        """
        dct = self.config

        for key in param:
            if not dct:
                return None
            dct = dct[key]

        return dct

        