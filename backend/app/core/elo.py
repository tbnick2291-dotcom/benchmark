def expected_score(rating_self: float, rating_opponent: float) -> float:
    return 1.0 / (1.0 + 10 ** ((rating_opponent - rating_self) / 400))


def update_rating(rating_self: float, rating_opponent: float, result: float, k: float = 32.0) -> float:
    return rating_self + k * (result - expected_score(rating_self, rating_opponent))


def batch_update(winner_rating: float, loser_rating: float, k: float = 32.0) -> tuple[float, float]:
    new_winner = update_rating(winner_rating, loser_rating, result=1.0, k=k)
    new_loser = update_rating(loser_rating, winner_rating, result=0.0, k=k)
    return new_winner, new_loser
