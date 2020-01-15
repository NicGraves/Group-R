import Band_Filters as bf
import Notch_Filters as nf
import Mean_Filters as mf
import Order_Statistic_Filters as osf

class filters:

    def Identify_Filter_Type(self, filter_type, image, cutoff, width, order, notchx, notchy, window_size):

        Band_Filter_obj = bf.Band_Filters
        Notch_Filter_obj = nf.Notch_Filters
        Mean_Filter_obj = mf.Mean_Filters
        Order_Statistic_Filters_obj = osf.Order_Statistic_Filters

        if filter_type == 'Ideal Band Reject':                                          # Band Filters
            return Band_Filter_obj.Ideal_Band_Reject(self, image, cutoff, width)
        elif filter_type == 'Ideal Band Pass':
            return Band_Filter_obj.Ideal_Band_Pass(self, image, cutoff, width)
        elif filter_type == 'Gaussian Band Reject':
            return Band_Filter_obj.Gaussian_Band_Reject(self, image, cutoff, width)
        elif filter_type == 'Gaussian Band Pass':
            return Band_Filter_obj.Gaussian_Band_Pass(self, image, cutoff, width)
        elif filter_type == 'Butterworth Band Reject':
            return Band_Filter_obj.Butterworth_Band_Reject(self, image, cutoff, width, order)
        elif filter_type == 'Butterworth Band Pass':
            return Band_Filter_obj.Butterworth_Band_Pass(self, image, cutoff, width, order)
        elif filter_type == 'Ideal Notch Reject':                                           # Notch Filters
            return Notch_Filter_obj.Ideal_Notch_Reject(self, image, notchy, notchx, cutoff)
        elif filter_type == 'Ideal Notch Pass':
            return Notch_Filter_obj.Ideal_Notch_Pass(self, image, notchy, notchx, cutoff)   # yes notchx and notchy are
        elif filter_type == 'Gaussian Notch Reject':                                        # switched. I messed up
            return Notch_Filter_obj.Gaussian_Notch_Reject(self, image, notchy, notchx, cutoff)  # writting the functions
        elif filter_type == 'Gaussian Notch Pass':
            return Notch_Filter_obj.Gaussian_Notch_Pass(self, image, notchy, notchx, cutoff)
        elif filter_type == 'Butterworth Notch Reject':
            return Notch_Filter_obj.Butterworth_Notch_Reject(self, image, notchy, notchx, cutoff, order)
        elif filter_type == 'Butterworth Notch Pass':
            return Notch_Filter_obj.Butterworth_Notch_Pass(self, image, notchy, notchx, cutoff, order)
        elif filter_type == 'Arithmetic Mean Filter':                                       # Mean Filters
            return Mean_Filter_obj.Arithmetic_Mean_Filter(self, image, cutoff)
        elif filter_type == 'Geometric Mean Filter':
            return Mean_Filter_obj.Geometric_Mean_Filter(self, image, cutoff)
        elif filter_type == 'Harmonic Mean Filter':
            return Mean_Filter_obj.Harmonic_Mean_Filter(self, image, cutoff)
        elif filter_type == 'Max Filter':                                                   # Order Statistic Filters
            return Order_Statistic_Filters_obj.Max_Filter(self, image, window_size)
        elif filter_type == 'Min Filter':
            return Order_Statistic_Filters_obj.Min_Filter(self, image, window_size)
        elif filter_type == 'Median Filter':
            return Order_Statistic_Filters_obj.Median_Filter(self, image, window_size)
        elif filter_type == 'Midpoint Filter':
            return Order_Statistic_Filters_obj.Midpoint_Filter(self, image, window_size)
        elif filter_type == 'Alpha Trimmed Mean Filter':
            return Order_Statistic_Filters_obj.Alpha_Trimmed_Mean_Filter(self, image, window_size)
        elif filter_type == "Adaptive Filter":
            return Order_Statistic_Filters_obj.Adaptive_Filter(self, image, window_size)
