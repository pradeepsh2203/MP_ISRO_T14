import numpy as np
from datetime import datetime
import math
import sys
import os
import pandas as pd
from matplotlib import pyplot as plt
from shutil import copyfile
import astropy
from scipy.optimize import curve_fit
import warnings
warnings.filterwarnings('ignore')
from astropy.convolution import convolve, Box1DKernel
import json


class flare : 

    def read_file(self,file) :
        if file.endswith('.lc'):
            with astropy.io.fits.open(file) as iit_bhu:
                iit_bhu.verify('fix')
                temp = iit_bhu[1].data
                data_ = pd.DataFrame(temp)

        if file.endswith('.csv'):
            data_ = pd.read_csv(file)




        init_data_time = datetime(2017, 1, 1,0,0,0)
        init_utc_timestamp = init_data_time.timestamp()
        if(type(data_['TIME'][0])== str):
            for i in range(len(data_['TIME'])):
                data_['TIME'][i] = self.utc_to_MET(data_['TIME'][i])
        # data_['TIME_IN_YEARS'] = data_['TIME'].apply(lambda x:datetime.utcfromtimestamp(x+init_utc_timestamp))

        #data_new = self.uniforming(data_)
        #data_new.sort_values(by='TIME')
        #data_new=data_new.reset_index()
        data_new2 = self.rebinning( data_ , 60)
        smoothed_signal = convolve(data_new2['RATE'], Box1DKernel(10))
        data_new2['RATE'] = smoothed_signal
        flare = self.flare_locations(data_new2)
        return flare
        #return flare
        #print(flare[5])
        # final_data = pd.DataFrame()
        # final_data['rise point time'] = np.array(flare[0])
        # final_data['rise point time']= final_data['rise point time'].apply(lambda x:datetime.utcfromtimestamp(x+init_utc_timestamp))
        # final_data['type of flare'] = np.array(flare[2])
        # final_data['rise start time'] = np.array(flare[3])
        # final_data['rise start time']= final_data['rise start time'].apply(lambda x:datetime.utcfromtimestamp(x+init_utc_timestamp))
        # final_data['peak time'] = np.array(flare[4])
        # final_data['peak time']= final_data['peak time'].apply(lambda x:datetime.utcfromtimestamp(x+init_utc_timestamp))
        # final_data['decay end time'] = np.array(flare[5])
        # final_data['decay end time']= final_data['decay end time'].apply(lambda x:datetime.utcfromtimestamp(x+init_utc_timestamp))
        # final_data['peak values'] = np.array(flare[6])
        # final_data['background'] = np.array(flare[7])
        #final_data['rise point rate'] = np.array(flare[8])

        # print(np.array(final_data['rise point time'])-np.array(final_data['rise start time']))
        # print(np.array(final_data['rise point time']),np.array(final_data['rise start time']))
        # print(final_data)

        #final_data['decay end time']= final_data['decay end time'].apply(lambda x:datetime.utcfromtimestamp(x+init_utc_timestamp))
        # print(final_data)
        # return final_data


    def utc_to_MET(self,date_time,utc_true = True):
        if 'datetime.datetime' in str(type(date_time)):
            pass

        if type(date_time) == str:
            try:
                form = "%d-%m-%Y %H:%M:%S.%f"
                date_time = datetime.strptime(date_time, form)

            except:
                try:
                    form = "%Y-%m-%d %H:%M:%S.%f"
                    date_time = datetime.strptime(date_time, form)

                except:
                    try:
                        form = "%m-%d-%Y %H:%M:%S.%f"
                        date_time = datetime.strptime(date_time, form)
                    except:
                        return np.float(date_time)


        if type(date_time) == np.float64:
            return date_time

        if utc_true == False:
            date_time = date_time.replace(tzinfo=datetime.timezone.utc)

        date_time_timestamp = date_time.timestamp()
        init_data_time = datetime(2017, 1, 1, 0, 0, 0)
        init_utc_timestamp = init_data_time.timestamp()
        final_timestamp = date_time_timestamp - init_utc_timestamp

        return final_timestamp

    def uniforming(self,df):
        input_ = df
        for i in range(len(input_['TIME']-1)):
            if input_['TIME'][i+1]-input_['TIME'][i] > 3:
                temp = input_['TIME'][i]
                while(temp < input_['TIME'][i+1]) :
                    temp = temp + 1
                    new_row = {'TIME':temp, 'RATE':input_['RATE'][i]}
                    #append row to the dataframe
                    input_ = input_.append(new_row, ignore_index=True)
        input_ = input_.sort_values(by='TIME')    
        return input_

    def rebinning(self, df_ ,bin_interval):
        data = []
        time = []
        for i in range (0,len(df_),bin_interval):
            time.append(df_['TIME'][i])
            if i+bin_interval<len(df_):
                sumi = sum([df_['RATE'][j] for j in range(i,i+bin_interval)])
            else:
                sumi = sum([df_['RATE'][j] for j in range(i,len(df_))])
            data.append(sumi/bin_interval)
        dicti = {'TIME':time,'RATE':data}
        df_ = pd.DataFrame(dicti)
        return df_

    def test_polynomial(self,x , a , b ,c ):
        return (((-1*b)/(2*a)) - (np.sqrt(((x-c)/a) + (b*b/4*a*a))))

    def test_linear(self, x , m , c):
        np.seterr(invalid='ignore')
        return (m*x + c)


    def test_decay_equation(self, x , A , alpha_inverse):
        np.seterr(invalid='ignore')
        return (x/abs(A))**(-alpha_inverse)

    def fit_curve_first_half_polynomial(self,rate , time , bg , t_peak ) :
        np.seterr(invalid='ignore')
        param_polynomial, param_cov_polynomial = curve_fit(self.test_polynomial, rate, np.array(time) - t_peak ,[-1,1,1] ,bounds = ([-np.inf,-np.inf,-np.inf],[-1,-0.1,np.inf]), maxfev=50000)
        time_start = -(param_polynomial[1]/2*param_polynomial[0]) -  np.sqrt(((bg-param_polynomial[2])/param_polynomial[0]) + (param_polynomial[1]*param_polynomial[1]/4*param_polynomial[0]*param_polynomial[0])) + t_peak
        #print(param_polynomial)
        return time_start

    def fit_curve_first_half_linear(self,rate , time , bg , t_peak ) :
        np.seterr(invalid='ignore')
        param_linear, param_cov_linear = curve_fit(self.test_linear, rate ,np.array(time) - t_peak ,[1,1,1] , maxfev=50000)
        time_start = param_linear[0]*bg + param_linear[1]
        return time_start

    def fit_curve_later_half(self,rate , time , bg , t_peak) :
        np.seterr(invalid='ignore') 
        param_decay, param_conv_decay = curve_fit( self.test_decay_equation, rate , (np.array(time) - t_peak) , [1,1] ,bounds = ([0.0001,-np.inf],np.inf) ,maxfev=50000)
        #print(param_decay)
        time_end =  ((bg + 0.47)/param_decay[0])**(-param_decay[1]) + t_peak
        #plt.plot(time_end, rate ,color='green', linestyle='solid',linewidth=1, markersize=12)
        return time_end

    def flare_locations(self,df):
        np.seterr(invalid='ignore')
        rise = []
        rise_rate = []
        rise_start = []
        decay_end = []
        decay = []
        peaks_time = []
        bg_for_this_peak = []
        type = []
        flare_end_point = []
        bg = df['RATE'][0]
        i = 0
        prev_i = [0,0]
        peak_values = []
        plt.title('SOLAR FLARES', fontdict={'fontweight':'bold', 'fontsize': 18})
        plt.xlabel('TIME')
        plt.ylabel('FLUX (X e-7) W/(m^2)')
        handles =  ['A class flare', 'B class flare' , 'C class flare' , 'M class flare' , 'X class flare']
        labels = ['green','r','orange','b','m']
        plt.legend(handles, labels, loc=3, framealpha=1, frameon=True)
        plt.plot(df['TIME'], df['RATE'],color='k', linestyle='dashed',linewidth=1, markersize=12)
        
        #f_bg = df['Rate'][0]
        while i < (len(df)-4):
            if df['RATE'][i]<df['RATE'][i+1]:
                if df['RATE'][i+1]<df['RATE'][i+2]:
                    if df['RATE'][i+2]<df['RATE'][i+3]:
                        if df['RATE'][i+3]<df['RATE'][i+4] and df['RATE'][i+4]/df['RATE'][i] > 1.03:
                            #rise.append([df['Rate'][i],df['Rate'][i+1],df['Rate'][i+2],df['Rate'][i+3]])
                            rise.append(df['TIME'][i])
                            rise_rate.append(df['RATE'][i])
                            temp = i+4
                            prev_i.append(i)
                            del prev_i[0]
                            #m=m+1
                            
                            for j in range(i+4, len(df)-3):
                                if df['RATE'][j]>df['RATE'][j+1]:
                                    if df['RATE'][j+1]>df['RATE'][j+2]:
                                        if df['RATE'][j+2]>df['RATE'][j+3]:
                                                #decay.append([df['Rate'][j],df['Rate'][j+1],df['Rate'][j+2],df['Rate'][j+3]])
                                                decay.append(j+3)
                                                temp = j+3
                                                try:
                                                    for kl in range(j+4,len(df)-3):
                                                        if df['RATE'][kl]>df['RATE'][kl+1]:
                                                            if df['RATE'][kl+1]>df['RATE'][kl+2]:
                                                                if df['RATE'][kl+2]<df['RATE'][kl+3]:
                                                                    flare_end_point.append(kl)
                                                                    break 
                                                except:
                                                    flare_end_point.append(len(df)-1)
                                                break
                            points_between = np.array(df['RATE'][i+4:j])
                            if len(points_between) == 0 :
                                points_between = np.array(df['RATE'][i+3:i+5])
                            while_stop = 1
                            nm = i + 2
                            while(while_stop == 1):
                                nm = nm -1
                                if(df['RATE'][i] - df['RATE'][nm] > 900 or nm == 0 ):
                                    while_stop = 0
                                    temp_average = np.array(df['RATE'][nm:i])
                                    if np.mean(temp_average)/bg > 1.5:
                                            pass
                                    elif np.mean(temp_average)/bg < 1.5 and np.max(points_between)/np.mean(temp_average) > 1.5 :
                                            bg = np.mean(temp_average)

                                    elif df['RATE'][i] < np.mean(temp_average) : 
                                        bg  = df['RATE'][i]

                            peak_value = max(list(points_between))    
                            peak_values.append(peak_value)
                            points_between_list = list(points_between)
                            index_max = points_between_list.index(peak_value) + i + 4
                            peaks_time.append(df['TIME'][index_max])
                            bg_for_this_peak.append(bg)
                            
                            fig_size = plt.rcParams["figure.figsize"]
                            fig_size[0] = 20
                            fig_size[1] = 8
                            
                            try:
                                curve = np.polyfit(np.array(df['RATE'][index_max-7:int(index_max)-4]), np.array(df['TIME'][index_max-7:int(index_max)-4]),1)
                                poly = np.poly1d(curve)   
                                rise_start.append(poly(bg))
                            except:
                                curve = np.polyfit(np.array(df['RATE'][index_max-4:index_max]), np.array(df['TIME'][index_max-4:index_max]),1)
                                poly = np.poly1d(curve)
                                rise_start.append(poly(bg))
                            try:
                                decay_end.append(self.fit_curve_later_half(np.array(df['RATE'][index_max : kl+2]) , np.array(df['TIME'][index_max : kl+2]), bg , df['TIME'][index_max] ))
                            except:
                                #rise_start.append(self.fit_curve_first_half_polynomial(np.array(df['RATE'][i:index_max]) , np.array(df['TIME'][i:index_max]) ,bg , df['TIME'][index_max]))
                                decay_end.append(self.fit_curve_later_half(np.array(df['RATE'][index_max : j+4]) , np.array(df['TIME'][index_max : j+4]), bg , df['TIME'][index_max] ))

                            if np.max(points_between) - bg <= 1 and np.max(points_between)>bg :
                                float = (peak_value - bg)*10
                                format_float = "{:.1f}".format(float)
                                type.append(str(format_float) + 'A')
                                plt.plot(df['TIME'][i:flare_end_point[-1]], df['RATE'][i:flare_end_point[-1]],color='green', linestyle='solid',linewidth=1, markersize=12)
                                plt.scatter(df['TIME'][i], df['RATE'][i],color='y')
                                plt.scatter(df['TIME'][flare_end_point[-1]], df['RATE'][flare_end_point[-1]],color='y')
                                print('hellow')

                            elif np.max(points_between) - bg < 1 and np.max(points_between)<=bg :
                                float = (peak_value - df['RATE'][i])*10
                                format_float = "{:.1f}".format(float)
                                type.append(str(format_float) + 'A')
                                plt.plot(df['TIME'][i:flare_end_point[-1]], df['RATE'][i:flare_end_point[-1]],color='green', linestyle='solid',linewidth=1, markersize=12)
                                plt.scatter(df['TIME'][i], df['RATE'][i], color='brown')
                                plt.scatter(df['TIME'][flare_end_point[-1]], df['RATE'][flare_end_point[-1]], color='brown')
                                print('hellow')

                            elif np.max(points_between)-bg >= 1 and np.max(points_between) - bg < 10:
                                float = (peak_value - bg)
                                format_float = "{:.1f}".format(float)
                                type.append(str(format_float) + 'B')
                                plt.plot(df['TIME'][i:flare_end_point[-1]], df['RATE'][i:flare_end_point[-1]],color='r', linestyle='solid',linewidth=1, markersize=12)
                                plt.scatter(df['TIME'][i], df['RATE'][i],color='green')
                                plt.scatter(df['TIME'][flare_end_point[-1]], df['RATE'][flare_end_point[-1]],color='green')

                            elif np.max(points_between)-bg >= 10 and np.max(points_between) - bg < 100:
                                float = (peak_value - bg)/10
                                format_float = "{:.1f}".format(float)
                                type.append(str(format_float) + 'C')
                                plt.plot(df['TIME'][i:flare_end_point[-1]], df['RATE'][i:flare_end_point[-1]],color='orange', linestyle='solid',linewidth=1, markersize=12)
                                plt.scatter(df['TIME'][i], df['RATE'][i],color='magenta')
                                plt.scatter(df['TIME'][flare_end_point[-1]], df['RATE'][flare_end_point[-1]], color='magenta')

                            elif np.max(points_between)-bg >= 100 and np.max(points_between) - bg < 1000:
                                float = (peak_value - bg)/100
                                format_float = "{:.1f}".format(float)
                                type.append(str(format_float) + 'M')
                                plt.plot(df['TIME'][i:flare_end_point[-1]], df['RATE'][i:flare_end_point[-1]],color='b', linestyle='solid',linewidth=1, markersize=12)
                                plt.scatter(df['TIME'][i], df['RATE'][i],color='orange')
                                plt.scatter(df['TIME'][flare_end_point[-1]], df['RATE'][flare_end_point[-1]],color='orange')

                            elif np.max(points_between)-bg >= 1000 and np.max(points_between) - bg < 100000:
                                float = (peak_value - bg)/1000
                                format_float = "{:.1f}".format(float)
                                type.append(str(format_float) + 'X')
                                plt.plot(df['TIME'][i:flare_end_point[-1]], df['RATE'][i:flare_end_point[-1]],color='m', linestyle='solid',linewidth=1, markersize=12)
                                plt.scatter(df['TIME'][i], df['RATE'][i],color='r')
                                plt.scatter(df['TIME'][flare_end_point[-1]], df['RATE'][flare_end_point[-1]],color='r')


                            i = temp + 1
                        else:
                            i+=1
                    else:
                        i+=1
                else:
                    i+=1
            else:
                i+=1
        plt.savefig('uploads\\file34.png', dpi=400)
        # plt.show()
        comb = [rise,  decay ,type , rise_start ,peaks_time, decay_end , peak_values , bg_for_this_peak , rise_rate]
        return comb





if __name__ == '__main__':
    flare_ = flare()
    fileName = input()
    # print(fileName)
    data = flare_.read_file(fileName)
    array_data = json.dumps(data, separators=(',',':'))
    print(array_data)
    #array_data = json.dumps(data, separators=(',',':'))
    #print(array_data)
    #print(array_data)
