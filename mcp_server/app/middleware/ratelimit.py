def check_rate_limit(self):
    rate = self.client.get_rate_limit()
    remaining = rate.core.remaining

    if remaining < 10:
        raise Exception("GitHub rate limit almost exhausted")

    return remaining
