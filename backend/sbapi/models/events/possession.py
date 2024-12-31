# sbapi/models/events/possession.py
from django.db import models
from .base import Event


class PossessionEvent(Event):
    """Possession-related event details"""
    # Set pieces
    corner_awarded = models.BooleanField(
        default=False)  # recorded as h/a for conceded/won

    # Ball control
    dispossessed = models.BooleanField(default=False)
    turnover = models.BooleanField(default=False)
    overrun = models.BooleanField(default=False)

    # Dribbling
    dribble_lastman = models.BooleanField(default=False)
    dribble_lost = models.BooleanField(default=False)
    dribble_won = models.BooleanField(default=False)

    class Meta:
        db_table = 'sbapi_event_possession'  # Specific table name
        verbose_name = 'Events - Possession'
        verbose_name_plural = 'Events - Possession'
        indexes = [
            *Event.Meta.indexes,
            models.Index(fields=['dribble_won']),
            models.Index(fields=['dispossessed']),
            models.Index(fields=['touches']),
        ]


# 
# Location of each pass
# End location of each pass
# Pass accuracy so all passes, (for this we need to use pass accurate and pass innac)then use accuract erand innacruate

# Type of pass, so this too:

# was it an assist
# was it a corner?
# was it a cross? most times when its a corner its a cross but not always lol
# what about:
# Assist freekick
# Assist other
# Assist throughball
# Assist throwin
# was it Intentional assist

# then for a # Passkey key pass was it a ?

# Key pass corner

# Key pass cross

# Key pass freekick

# Key pass long

# Key pass other

# Key pass short

# Key pass throughball

# Key pass throwin

# then chances created too (this mean key passes + assists), so for alter when trying to find the cahcne created find ti from events
# Note theres also BCC BUT THIS ALREADY CO MES TWITH THE DAT SO WE ODNT NEED TO FIND




# doing  it this way will help me aggregate it for a season, so aggreagte for amcth foir a player i wil show u this too

# then use this too i want to kmow every detaila but my passes
# Pass corner

# Pass corner accurate

# Pass corner inaccurate

# Pass cross accurate

# Pass cross blocked defensive

# Pass cross inaccurate

# Pass freekick

# Pass freekick accurate

# Pass freekick inaccurate

# Pass back

# Pass back zone inaccurate

# Pass forward

# Pass forward zone accurate

# Pass left

# Pass right

# Pass chipped

# Pass head

# Pass left foot

# Pass right foot

# Pass long ball accurate

# Pass long ball inaccurate

# Short pass accurate

# Short pass inaccurate

# Pass through ball accurate

# Pass through ball inaccurate

# Big chance created

# Successful final third passes

# Throw in

# i wanna be clear what im trying to do so you know,
# basically i havce api routes fior diffrent stats i ie match events, im staring with passing that needs upgradingf and pottnetially changing idk yuoull help
# the route return all passing events from a amtchn adn com, eptiotn good, firstly i want to be able to from ym front end (so perhaps i need an api rotue backend oidk0, see
# passinmg events for a speicifc player form trhat macth you get me
# alsoo,i currently have a playere macth stats rotue showingg stats from a specifi cmathc thats no problem but then, i feel liek its goo ig ic a=could get mor edtail fo the stuff 
# i aggregate, for example asists in match a playe rmay have 3, but then i want to see what was true, ie was he asis tyf rom a corner or fk or sdomehting
# or even a regualr passes a paleyr had 90 passes, i want to get the detail of each pass as well or know i mean we have all the dat in one palc eits kind of jus tfil;t
# fi;lteroig it in the righ wya or somethign , liek a players passes all them then the type and then aggregated (and then knowing what those aggregate stuff are clealryl)
# liek i dont jsu wnan aknow he had 3 chances cretaed or 5 bgi chnces created wold be ncie to know if it was a coner ans stuff idk if i m vlear o hwo this woulkd work
# caus e i ahevb an matches/1282309/events/passing and matches/stats/players/1282309 showing detail too 

#  i wil lalso calculate further stats based on ther attribuyte s latesr, the reason i want match level agrgegation and with detial is so that my
# player season is easy to sdo ie cna use match possibley but for all amcthes idk, liek perhaps isot sjust getting the ful row of passing event btu perhas theres abter way, hope ive been clear and lmk
# if u have any qs, i am goonn share my code


# on my endx and start x coroidnates, like i want to do stuff liek finding out progressive passes, later tho