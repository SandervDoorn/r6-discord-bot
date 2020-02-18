from discord.ext.commands import CommandError

class TeamAlreadyExistsError(Exception):
    pass


class TeamAlreadyCaptainizedError(Exception):
    pass


class NotAllowedError(CommandError):
    pass
