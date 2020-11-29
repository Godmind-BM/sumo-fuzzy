import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as skf


class GreenExtend(object):
    """Provides data and methods to extend green."""

    def __init__(self):
        pass

    def compute_extended_time(self, flow1, flow2):
        """
        Provide green phase extension to add to min duration.

        >>> compute_extended_time(flow1, flow2)
            parameters:
            ----------
            flow1 : queue-length of green-phase first flow
            flow2 : queue-length of green-phase second flow

            results:
            -------
            current-green phase extension.
        """
        # Ligustic variables.
        first_queue = np.arange(0, 31, 1)
        second_queue = np.arange(0, 31, 1)
        extension_time = np.arange(0, 11, 1)

        # Fuzzy subsets

        # Inputs : Queue-lengths
        first_queue_low = skf.trapmf(first_queue, [0, 0, 6, 12, ])
        first_queue_med = skf.trapmf(first_queue, [6, 12, 18, 24, ])
        first_queue_hig = skf.trapmf(first_queue, [18, 24, 30, 30, ])

        second_queue_low = skf.trapmf(second_queue, [0, 0, 6, 12, ])
        second_queue_med = skf.trapmf(second_queue, [6, 12, 18, 24, ])
        second_queue_hig = skf.trapmf(second_queue, [18, 24, 30, 30, ])

        # Output: Green-extension
        ext_low = skf.trapmf(extension_time, [0, 0, 2, 4])
        ext_med = skf.trapmf(extension_time, [2, 4, 6, 8])
        ext_hig = skf.trapmf(extension_time, [6, 8, 10, 10])

        # Fuzzy membership functions activation
        first_queue_low_level = skf.interp_membership(first_queue, first_queue_low, flow1)
        first_queue_med_level = skf.interp_membership(first_queue, first_queue_med, flow1)
        first_queue_hig_level = skf.interp_membership(first_queue, first_queue_hig, flow1)

        second_queue_low_level = skf.interp_membership(second_queue, second_queue_low, flow2)
        second_queue_med_level = skf.interp_membership(second_queue, second_queue_med, flow2)
        second_queue_hig_level = skf.interp_membership(second_queue, second_queue_hig, flow2)

        # Rules

        # (f_queue is low) AND (s_queue is low) ---> (ext is low)
        premise_rule1 = np.fmin(first_queue_low_level, second_queue_low_level)
        rule1 = np.fmin(premise_rule1, ext_low)
        # (f_queue is low) AND (s_queue is medium) ---> (ext is medium)
        premise_rule2 = np.fmin(first_queue_low_level, second_queue_med_level)
        rule2 = np.fmin(premise_rule2, ext_med)
        # (f_queue is low) AND (s_queue is high) ---> (ext is high)
        premise_rule3 = np.fmin(first_queue_low_level, second_queue_hig_level)
        rule3 = np.fmin(premise_rule3, ext_hig)
        # (f_queue is medium) AND (s_queue is low) ---> (ext is medium)
        premise_rule4 = np.fmin(first_queue_med_level, second_queue_low_level)
        rule4 = np.fmin(premise_rule4, ext_med)
        # (f_queue is medium) AND (s_queue is medium) ---> (ext is medium)
        premise_rule5 = np.fmin(first_queue_med_level, second_queue_med_level)
        rule5 = np.fmin(premise_rule5, ext_med)
        # (f_queue is medium) AND (s_queue is high) ---> (ext is high)
        premise_rule6 = np.fmin(first_queue_med_level, second_queue_hig_level)
        rule6 = np.fmin(premise_rule6, ext_hig)
        # (f_queue is high) AND (s_queue is low) ---> (ext is high)
        premise_rule7 = np.fmin(first_queue_hig_level, second_queue_low_level)
        rule7 = np.fmin(premise_rule7, ext_hig)
        # (f_queue is high) AND (s_queue is medium) ---> (ext is high)
        premise_rule8 = np.fmin(first_queue_hig_level, second_queue_med_level)
        rule8 = np.fmin(premise_rule8, ext_hig)
        # (f_queue is high) AND (s_queue is high) ---> (ext is high)
        premise_rule9 = np.fmin(first_queue_hig_level, second_queue_hig_level)
        rule9 = np.fmin(premise_rule9, ext_hig)

        # Aggregates all the outputs
        # aggreagation : max is used for
        decision_matrix = [
            rule1, rule2, rule3,
            rule4, rule5, rule6,
            rule7, rule8, rule9,
        ]

        aggregated = 0
        for x in decision_matrix:
            aggregated = np.fmax(aggregated, x)

        # deffuzification
        extension = skf.defuzz(extension_time, aggregated, 'centroid')

        return np.round(extension)

    def __repr__(self):
        return f'{self.__class__.__name__}'



class PhaseUrgency(object):
    """Phase urgency module."""

    def __init__(self):
        """Initialiser."""
        pass

    def compute_urgency(self, queue_length, waiting_time):
        """
             >>> compute_urgency(q, w).
            parameters:
                q : queue length
                w : waiting
            returns:
                The phase urgency.
        """

        # lingustics variables
        # queue : [0-30]
        # waiting-time : [0-150]
        # urgency : [0-10]
        # print("phase urgency :", "waiting :", waiting_time, "queue :", queue_length)
        queue = np.arange(0, 31, 1)
        waiting = np.arange(0, 220, 1)
        urgency = np.arange(0, 11, 1)

        # fuzzy subsets
        # queue-length
        queue_low = skf.trapmf(queue, [0, 0, 6, 12, ])
        queue_med = skf.trapmf(queue, [6, 12, 18, 24, ])
        queue_hig = skf.trapmf(queue, [18, 24, 30, 30, ])

        # waiting-time
        # wait_low = skf.trapmf(waiting, [0, 0, 30, 60, ])
        # wait_med = skf.trapmf(waiting, [30, 60, 90, 120, ])
        # wait_hig = skf.trapmf(waiting, [90, 120, 150, 150, ])

        wait_low = skf.trapmf(waiting, [0, 0, 44, 88, ])
        wait_med = skf.trapmf(waiting, [44, 88, 132, 176, ])
        wait_hig = skf.trapmf(waiting, [132, 176, 220, 220, ])

        # urgency
        urge_low = skf.trapmf(urgency, [0, 0, 2, 4])
        urge_med = skf.trapmf(urgency, [2, 4, 6, 8])
        urge_hig = skf.trapmf(urgency, [6, 8, 10, 10])

        # activate membership function
        queue_low_level = skf.interp_membership(queue, queue_low, queue_length)
        queue_med_level = skf.interp_membership(queue, queue_med, queue_length)
        queue_hig_level = skf.interp_membership(queue, queue_hig, queue_length)

        wait_low_level = skf.interp_membership(waiting, wait_low, waiting_time)
        wait_med_level = skf.interp_membership(waiting, wait_med, waiting_time)
        wait_hig_level = skf.interp_membership(waiting, wait_hig, waiting_time)

        # rules
        # (queue is low) AND (waiting is low) ---> (urge is low)
        premise_rule1 = np.fmin(queue_low_level, wait_low_level)
        rule1 = np.fmin(premise_rule1, urge_low)
        # (queue is medium) AND (waiting is low) ---> (urge is low)
        premise_rule2 = np.fmin(queue_med_level, wait_low_level)
        rule2 = np.fmin(premise_rule2, urge_low)
        # (queue is high) AND (waiting is low) ---> (urge is medium)
        premise_rule3 = np.fmin(queue_hig_level, wait_low_level)
        rule3 = np.fmin(premise_rule3, urge_med)
        # (queue is low) AND (waiting is med) ---> (urge is medium)
        premise_rule4 = np.fmin(queue_low_level, wait_med_level)
        rule4 = np.fmin(premise_rule4, urge_med)
        # (queue is medium) AND (waiting is med) ---> (urge is medium)
        premise_rule5 = np.fmin(queue_med_level, wait_med_level)
        rule5 = np.fmin(premise_rule5, urge_hig)
        # (queue is high) AND (waiting is med) ---> (urge is high)
        premise_rule6 = np.fmin(queue_hig_level, wait_med_level)
        rule6 = np.fmin(premise_rule6, urge_hig)
        # (queue is low) AND (waiting is high) ---> (urge is medium)
        premise_rule7 = np.fmin(queue_low_level, wait_hig_level)
        rule7 = np.fmin(premise_rule7, urge_hig)
        # (queue is med) AND (waiting is high) ---> (urge is high)
        premise_rule8 = np.fmin(queue_med_level, wait_hig_level)
        rule8 = np.fmin(premise_rule8, urge_hig)
        # (queue is high) AND (waiting is high) ---> (urge is high)
        premise_rule9 = np.fmin(queue_hig_level, wait_hig_level)
        rule9 = np.fmin(premise_rule9, urge_hig)

        # Aggregates all the outputs
        # aggreagation : max is used for
        decision_matrix = [
            rule1, rule2, rule3,
            rule4, rule5, rule6,
            rule7, rule8, rule9,
        ]

        aggregated = 0
        for x in decision_matrix:
            aggregated = np.fmax(aggregated, x)

        # deffuzification
        urge = skf.defuzz(urgency, aggregated, 'centroid')

        return urge

    def __repr__(self):
        return f'{self.__class__.__name__}'
