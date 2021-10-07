import math

class LikelihoodModel:
    """ Mixin class for maximum-likelihood estimation in one-parameter models """

    def __init__(self, x):
        """ Set up LikelihoodModel with data in iterable x """
        self.x = x

    def loglik(self, theta, xi):
        """ Function to be implemented by subclasses implementing a specific model
            Should return the contribution of observation xi to the loglikelihood
            for parameter theta """
        raise NotImplementedError

    def initialise_optimisation(self):
        """ Optional method which will be called before the loglikelihood is
            optimised. To be used to set theta_min and theta_max in a
            data-adaptive way """
        pass

    def full_loglik(self, theta):
        """ Compute full loglikelihood using method loglik """
        return sum([self.loglik(theta, xi) for xi in self.x])

    def mle(self):
        """ Compute the maximum likelihood estimate
            Requires that two attributes, self.theta_min and self.theta_max
            (smallest and largest possible value of the parameters) have been
            set """
        phi = (1 + math.sqrt(5)) / (3 + math.sqrt(5))
        self.initialise_optimisation()
        # The algorithm is based on maintaining a list of three values, so that
        # the value in the middle has the largest log-likelihood
        theta = [self.theta_min,
                 (1 - phi) * self.theta_min + phi * self.theta_max,
                 self.theta_max]
        # Evaluate loglikelihood for these three values
        loglik = list(map(lambda theta: self.full_loglik(theta), theta))
        # Add new values as long as the three values are too far apart ...
        while theta[2] - theta[0] > 1e-12:
            # We currently have three points [theta[0]. theta[1], theta [2]]
            # Where we add the new point depends on the distances between
            # the thetas
            if theta[1] - theta[0] > theta[2] - theta[1]:
                # theta[0]                   theta[1]     theta[2]
                #               ^^^^^^ new point will go here
                theta_new = (1 - phi) * theta[1] + phi * theta[0]
                loglik_new = self.full_loglik(theta_new)
                # We now have four values of theta, we want to keep only three
                # We keep the largest one and the closest one to the left and
                # right
                if loglik_new > loglik[1]:
                    theta = [theta[0], theta_new, theta[1]]
                    loglik = [loglik[0], loglik_new, loglik[1]]
                else:
                    theta = [theta_new, theta[1], theta[2]]
                    loglik = [loglik_new, loglik[1], loglik[2]]
            else:
                # theta[0]    theta[1]                theta[2]
                #                           ^^^^^^ new point will go here
                theta_new = (1 - phi) * theta[1] + phi * theta[2]
                loglik_new = self.full_loglik(theta_new)
                # We now have four values of theta, we want to keep only three
                # We keep the largest one and the closest one to the left and
                # right
                if loglik_new > loglik[1]:
                    theta = [theta[1], theta_new, theta[2]]
                    loglik = [loglik[1], loglik_new, loglik[2]]
                else:
                    theta = [theta[0], theta[1], theta_new]
                    loglik = [loglik[0], loglik[1], loglik_new]
        return theta[1]