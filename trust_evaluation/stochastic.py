import numpy as np
from scipy.stats import beta

class SingleFeatureTrustModel:
    def __init__(self, base_lambda=0.05, volatility_scale=0.5, growth_rate=0.5, uncertainty_penalty=1.0):
        self.base_lambda = base_lambda
        self.volatility_scale = volatility_scale
        self.growth_rate = growth_rate  # how quickly n_eff increases
        self.uncertainty_penalty = uncertainty_penalty
        self.trust_mean = 0.5  # EWMA of trust scores
        self.n_eff = 2.0       # start with very low effective sample size
        self.measurements = []

    def observe(self, trust_score):
        self.measurements.append(trust_score)
        if len(self.measurements) > 30:
            self.measurements.pop(0)

        volatility = self.estimate_volatility()
        adaptive_lambda = self.compute_lambda(volatility)

        # Update smoothed trust estimate (p)
        self.trust_mean = (1 - adaptive_lambda) * self.trust_mean + adaptive_lambda * trust_score

        # Increase effective n
        self.n_eff += self.growth_rate

    def estimate_volatility(self):
        if len(self.measurements) < 2:
            return 0.0
        return np.std(self.measurements)

    def compute_lambda(self, volatility):
        return min(1.0, self.base_lambda + self.volatility_scale * volatility)

    @property
    def alpha(self):
        return self.trust_mean * self.n_eff

    @property
    def beta_param(self):
        return (1 - self.trust_mean) * self.n_eff

    @property
    def trust_score(self):
        return self.trust_mean

    @property
    def variance(self):
        alpha = self.alpha
        beta_val = self.beta_param
        denom = (alpha + beta_val)**2 * (alpha + beta_val + 1)
        return (alpha * beta_val) / denom if denom > 0 else 0.0

    @property
    def stddev(self):
        return np.sqrt(self.variance)

    @property
    def adjusted_trust_score(self):
        """Trust penalized by uncertainty (standard deviation)."""
        penalty = self.uncertainty_penalty * self.stddev
        adjusted = self.trust_mean * (1 - penalty)
        return max(0.0, min(1.0, adjusted))  # Clamp between 0 and 1

    def confidence_interval(self, confidence=0.95):
        return beta.interval(confidence, self.alpha, self.beta_param)

    def __repr__(self):
        return (f"SingleFeatureTrustModel(trust={self.trust_score:.4f}, "
                f"adjusted={self.adjusted_trust_score:.4f}, "
                f"n_eff={self.n_eff:.1f}, "
                f"std={self.stddev:.4f}, "
                f"CI95={self.confidence_interval()})")
