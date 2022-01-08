def refresh_step_dict(func):
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        self.create_step_dict(self)
    return wrapper

