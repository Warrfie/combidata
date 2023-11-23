class CombinatoricsError(Exception):
    """Bad combinatorics."""

    def __init__(self, message="You can't combine that case"):
        self.message = message
        super().__init__(self.message)