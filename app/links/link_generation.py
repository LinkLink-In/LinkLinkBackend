import random
import string


def generateCompletelyRandomShortID(length: int) -> str:
    """
    Generates a random n-character long short id for a link
    :return: link short id
    """
    return ''.join(random.choice(string.ascii_letters) for char in range(length))
