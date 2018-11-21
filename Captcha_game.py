from abc import ABCMeta
from abc import abstractmethod


# captcha game base class
class Captcha_game(object):
    game_content = None
    game_answer = None
    game_mode = None
    __metaclass__ = ABCMeta

    def __init__(self, argvs=[]):
        self.game_mode = "bot"

    def __call__(self):
        self._start_game()
        self._classify(self.game_mode)

    def captcha_api(self):
        print("wow")
        return None

    @abstractmethod
    def _start_game(self):
        raise NotImplementedError

    @abstractmethod
    def _classify(self, mode):
        raise NotImplementedError
