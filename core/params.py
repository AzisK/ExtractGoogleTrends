class Params:
    _params_default = {
        "geo": "US",
        "q": "vpn,antivirus,ad blocker,password manager",
    }
    passed_params = {'geo': None, 'q': None}

    @property
    def params(self):
        truthy_params = {k: self.passed_params[k] for k in self.passed_params if self.passed_params[k]}
        return {**self._params_default, **truthy_params}

    def pass_params(self, geo, q):
        self.passed_params = {'geo': geo, 'q': q}
        return self
