import numpy as np

#testing purposes, sample values to filter
#cases checked, values close together within given tolernace range, values not withn tolerance range
#duplicates, values within tolerance range at different points in the data (one at beginning/end)
FreqData = [54,10,10,10,13,40,37,50]

tolerance = 5 #bounds in which other values can not be within
FilteredFreqData = []
for Freq in FreqData: #scans through all values taken and filters any extra peaks within some tolerance range
    if len(FilteredFreqData) == 0: #stores first and highest peak value
        FilteredFreqData.append(Freq)
        continue
    
    print(Freq, ' = Freq') #testing purposes, see current iteration
    
    #if the current iteration is within the bounds of any of the values then move to the next iteration
    if any((Freq2-tolerance)<=Freq<=(Freq2+tolerance) for Freq2 in FilteredFreqData): 
        continue
    
    #1500 was selected as the first initial test value ; from observation of the plots of the audio, it appeared that most clear and distinct peaks that
    #was consistent among samples tend to be between 1-3kHz and anything above varied greatly.
    if Freq > 1500: #filters out any frequencies above the given value
        continue
        
    if Freq in FilteredFreqData: #avoid duplicate values
        continue
    FilteredFreqData.append(Freq)
    
#testing purposes, see final output
print(FilteredFreqData)
print(len(FreqData))
