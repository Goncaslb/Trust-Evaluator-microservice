# work in progress...


def bayesian_trust_update(current_trust, positive_feedback, negative_feedback, prior=0.5):
    alpha = prior * 10 + positive_feedback  # Prior belief in trustworthiness
    beta = (1 - prior) * 10 + negative_feedback  # Prior disbelief
    return alpha / (alpha + beta)  # Bayesian update formula

# time_decay 