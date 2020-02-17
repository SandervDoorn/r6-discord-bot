from discord import Member
from models.team import Team


def is_bot_admin(subject: Member):
    if 'R6 Bot Manager' in [r.name for r in subject.roles]:
        return True
    return False


def is_bot_admin_or_captain(subject: Member, team: Team):
    pass
