class Version:
    def __init__(self, major: int, minor: int, build: int, alpha=False, beta=False):
        self.major = major if isinstance(major, int) else int(major)
        self.minor = minor if isinstance(minor, int) else int(minor)
        self.build = build if isinstance(build, int) else int(build)
        self.alpha = alpha
        self.beta = beta

        if self.alpha and self.beta:
            raise ValueError('is_alpha and is_beta can\'t be true at the same time')

    # TODO: Beta | Alpha
    def __lt__(self, other):
        if self.major < other.major:
            return True
        elif self.minor < other.minor:
            return True
        elif self.build < other.build:
            return True
        else:
            return False

    # TODO: Beta | Alpha
    def __gt__(self, other):
        if self.major > other.major:
            return True
        elif self.minor > other.minor:
            return True
        elif self.build > other.build:
            return True
        else:
            return False

    # TODO: Beta | Alpha
    def __eq__(self, other):
        if self.major == other.major and self.minor == other.minor and self.build == other.build:
            return True
        else:
            return False

    @staticmethod
    def from_string(source: str):
        alpha = False
        beta = False

        source = source.split('-')
        if len(source) == 2:
            if source[1] == 'a':
                alpha = True
            elif source[1] == 'b':
                beta = True

        ma, mi, b = map(int, source[0].split('.'))

        return Version(ma, mi, b, alpha, beta)

    def __str__(self):
        addition = ''
        if self.alpha:
            addition = '-a'
        elif self.beta:
            addition = '-b'

        return f'{self.major}.{self.minor}.{self.build}' + addition
