from discord.ext.commands import CommandError


class TeamAlreadyExistsError(CommandError):
    pass


class TeamAlreadyCaptainizedError(CommandError):
    pass


class NotAllowedError(CommandError):
    pass


class PlayerAlreadyInTeamError(CommandError):
    pass


class UserNotRegisteredError(CommandError):
    pass


class NotCaptainOfTeamError(CommandError):
    pass


class TeamDoesNotExistError(CommandError):
    pass


class UserAlreadyExistsError(CommandError):
    pass


class UserNotInTeamError(CommandError):
    pass
