class Config:
    role_del_reason = None
    channel_del_reason = None
    members_punish_reason = None

    def set(variable: str):
        try:
            Config.__getattribute__(Config, variable)
        except AttributeError:
            print("Choose: role_del_reason, channel_del_reason, members_punish_reason")

Config.set(variable="fffdg")