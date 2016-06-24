"""models.py - This file contains the class definitions for the Datastore
entities used by the Game. Because these classes are also regular Python
classes they can include methods (such as 'to_form' and 'new_game')."""

import random
from datetime import date
from protorpc import messages
from google.appengine.ext import ndb

WORD_LIST = ['animal', 'obnoxious', 'word', 'bathroom', 'room', 'house', 'excursion']
MAX_ATTEMPTS = 10

class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    email =ndb.StringProperty()


class Game(ndb.Model):
    """Game object"""
    #target = ndb.IntegerProperty(required=True)
    target_word = ndb.StringProperty(required=True)
    partial_word_guessed = ndb.StringProperty(required=True)
    attempts_allowed = ndb.IntegerProperty(required=True, default=MAX_ATTEMPTS)
    attempts_remaining = ndb.IntegerProperty(required=True, default=MAX_ATTEMPTS)
    letters_guessed = ndb.StringProperty(required=True, default="")
    guess_results = ndb.StringProperty(required=True, default="")
    game_over = ndb.BooleanProperty(required=True, default=False)
    user = ndb.KeyProperty(required=True, kind='User')
    is_cancelled = ndb.BooleanProperty(required=True, default=False)

    @classmethod
    def new_game(cls, user, maxAttempts):
        """Creates and returns a new game"""
        if (maxAttempts <10):
            raise ValueError('Maximum must be greater than 10')
        i = random.choice(range(0, len(WORD_LIST)-1))
        game = Game(user=user,
                    target_word=WORD_LIST[i],
                    partial_word_guessed = "." * len(WORD_LIST[i]),
                    letters_guessed = "",
                    attempts_allowed = maxAttempts,
                    attempts_remaining = maxAttempts,
                    game_over=False)
        game.put()
        return game

    def to_form(self, message):
        """Returns a GameForm representation of the Game"""
        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.user_name = self.user.get().name
        form.attempts_remaining = self.attempts_remaining
        form.game_over = self.game_over
        form.letters_guessed = self.letters_guessed
        form.partial_word_guessed = self.partial_word_guessed
        form.message = message
        return form

    def end_game(self, won=False):
        """Ends the game - if won is True, the player won. - if won is False,
        the player lost."""
        self.game_over = True
        self.put()
        # Add the game to the score 'board'
        score = Score(user=self.user, date=date.today(), won=won,
                      attempts_remaining = self.attempts_remaining)
        score.put()


class Score(ndb.Model):

    """Score object"""
    user = ndb.KeyProperty(required=True, kind='User')
    date = ndb.DateProperty(required=True)
    won = ndb.BooleanProperty(required=True)
    attempts_remaining = ndb.IntegerProperty(required=True)

    def to_form(self):
        return ScoreForm(user_name=self.user.get().name, won=self.won,
                         date=str(self.date),
                         attempts_remaining = self.attempts_remaining)


class GameForm(messages.Message):
    """GameForm for outbound game state information"""
    urlsafe_key = messages.StringField(1, required=True)
    attempts_remaining = messages.IntegerField(2, required=True)
    game_over = messages.BooleanField(3, required=True)
    message = messages.StringField(4, required=True)
    user_name = messages.StringField(5, required=True)
    partial_word_guessed = messages.StringField(6, required=True)
    letters_guessed = messages.StringField(7, required=True)
    is_cancelled = messages.BooleanField(8,required=False)

class GameForms(messages.Message):
    """Return Multiple Game Forms"""
    items = messages.MessageField(GameForm, 1, repeated=True)

class NewGameForm(messages.Message):
    """Used to create a new game"""
    user_name = messages.StringField(1, required=True)
    max_attempts = messages.IntegerField(2, default=10)

#Message sent by form that picks a letter, guess is a single letter
class MakeMoveForm(messages.Message):
    """Used to make a move in an existing game"""
    guess = messages.StringField(1, required=True)


class ScoreForm(messages.Message):
    """ScoreForm for outbound Score information"""
    user_name = messages.StringField(1, required=True)
    date = messages.StringField(2, required=True)
    won = messages.BooleanField(3, required=True)
    attempts_remaining = messages.IntegerField(4, required=True)


class ScoreForms(messages.Message):
    """Return multiple ScoreForms"""
    items = messages.MessageField(ScoreForm, 1, repeated=True)


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)

class RankingForm(messages.Message):
    user_name = messages.StringField(1, required=True)
    performance_index = messages.FloatField(2, required=True)
    avg_score = messages.FloatField(3, required=True)

class RankingForms(messages.Message):
    items = messages.MessageField(RankingForm, 1, repeated=True)

class GameHistoryForm(messages.Message):
    """Outbound game history information"""
    urlsafe_key = messages.StringField(1, required=True)
    letter_guessed = messages.StringField(2, required=True)
    is_present = messages.BooleanField(3, required=True)

class GameHistoryForms(messages.Message):
    items = messages.MessageField(GameHistoryForm, 1, repeated=True)