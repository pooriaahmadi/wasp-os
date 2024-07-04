import wasp


class Field:
    def __init__(self, name: str, default, setting_name: str) -> None:
        self.name = name
        self.__value = None
        self.default = default
        self.setting_name = setting_name

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value
        self.__save()

    @value.getter
    def value(self):
        return self.__value

    def get(self):
        value = wasp.system.get_from_settings(self.setting_name, self.name)
        if value == None:
            self.value = self.default
        else:
            self.__value = value

    def __save(self):
        wasp.system.save_to_settings(self.setting_name, self.name, self.value)
