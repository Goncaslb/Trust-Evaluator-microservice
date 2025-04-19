import numpy as np
from scipy.stats import beta

class SingleFeatureTrustModel:
    def __init__(self, name ,base_lambda=0.1, growth_rate=0.8, uncertainty_penalty=0.8):
        self.name = name
        self.base_lambda = base_lambda
        self.growth_rate = growth_rate  # how quickly n_eff increases
        self.uncertainty_penalty = uncertainty_penalty 
        self.n_eff = 2.0       # start with very low effective sample size
        self.alpha = 1.0
        self.beta = 1.0
        self.measurements = []

    def observe(self, observation):
        self.measurements.append(observation)
        if len(self.measurements) > 5:
            self.measurements.pop(0)

        volatility = self.estimate_volatility()
        adaptive_lambda = self.compute_lambda(volatility)

        # Increase effective n
        self.alpha *= 1/self.n_eff
        self.beta *= 1/self.n_eff
        self.n_eff += self.growth_rate/(volatility+1)

        # update depending on the new observation. Eg: if observation is the best possible it will be 1 so beta will not be increased
        
        self.alpha = ((1 - adaptive_lambda) * self.alpha + adaptive_lambda * observation) * self.n_eff
        #print(observation)
        #print('1-adaptive_lambda', (1-adaptive_lambda), '* self.beta', self.beta, '+adaptive_lambda',adaptive_lambda, '*1- observation', (1 - observation), '* self.n_eff', self.n_eff)
        self.beta = ((1 - adaptive_lambda) * self.beta + adaptive_lambda * (1 - observation)) * self.n_eff
        #print(self.beta)
        #print('lambda down')
        #print(adaptive_lambda)
        # above we multiply by n_eff to increase certainty with experience

        

    def estimate_volatility(self):
        if len(self.measurements) < 2:
            return 0.0
        return np.std(self.measurements)

    def compute_lambda(self, volatility):
        # Invert the relationship: higher volatility -> higher lambda
        # You might need to adjust the scaling factor and offset to fine-tune the behavior
        return max(0,min(1,self.base_lambda * (1 + 2.5*volatility)))

    @property
    def trust_score(self): # expected value of beta distribution
        return self.alpha / (self.alpha + self.beta)

    @property
    def variance(self):
        alpha = self.alpha
        beta_val = self.beta
        denom = (alpha + beta_val)**2 * (alpha + beta_val + 1)
        return (alpha * beta_val) / denom if denom > 0 else 0.0

    @property
    def stddev(self):
        return np.sqrt(self.variance)

    @property
    def adjusted_trust_score(self):
        """Trust penalized by uncertainty (standard deviation)."""
        if self.n_eff >= 4: 
            penalty = self.uncertainty_penalty * self.stddev
            adjusted = self.trust_score * (1 - penalty)
            return max(0.0, min(1.0, adjusted))  # Clamp between 0 and 1
        else: 
            return self.trust_score

    def confidence_interval(self, confidence=0.95):
        return beta.interval(confidence, self.alpha, self.beta)

    def __repr__(self):
        return (f"SingleFeatureTrustModel(trust={self.trust_score:.4f}, "
                f"adjusted={self.adjusted_trust_score:.4f}, "
                f"n_eff={self.n_eff:.1f}, "
                f"std={self.stddev:.4f}, "
                f"CI95={self.confidence_interval()})")
