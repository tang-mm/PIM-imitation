#####################################
# Folder and Files info

form Set files to be analyzed
  sentence type real_speakers
  sentence inputfolder F:\MIMICRY\wav\real_speakers\
  sentence outputfolder F:\MIMICRY\praat_out\
endform

outputfile$ = outputfolder$ + type$ + "_Pitch_Int_Jitter_Shimmer_Syllables.txt" 

filedelete 'outputfile$'
fileappend "'outputfile$'" file'tab$'minPitch'tab$'maxPitch'tab$'pitch_range'tab$'medianPitch'tab$'meanPitch'tab$'sdPitch'tab$'
 ...jitter_loc'tab$'jitter_loc_abs'tab$'jitter_rap'tab$'jitter_ppq5'tab$'
 ...shimmer_loc'tab$'shimmer_loc_dB'tab$'shimmer_apq3'tab$'shimmer_apq5'tab$'shimmer_apq11
 ...'tab$'mean_nhr:4'tab$'min_int'tab$'max_int'tab$'mean_int'tab$'range_of_int'tab$'
 ...speechrate (nsyll/dur)'tab$'articulation rate (nsyll / phonationtime)'tab$'ASD (speakingtime/nsyll)'newline$'

# read files
Create Strings as file list... list 'inputfolder$'/*.wav
numberOfFiles = Get number of strings
for ifile to numberOfFiles
   select Strings list
   file$ = Get string... ifile

Read from file... 'inputfolder$''file$'

name$ = selected$("Sound",1)

#####################################
# Intensity
To Intensity... 100 0 
select Intensity 'name$'
start = 0
end = 10
min_int = Get minimum... start
... end Parabolic
max_int = Get maximum... start
... end parabolic
mean_int = Get mean... start end
... energy
range_of_int = max_int-min_int
select Intensity 'name$'
Remove

#####################################
# Pitch
select Sound 'name$'
minimum_pitch = 70
maximum_pitch = 600
 
pitch_silence_threshold = 0.03
pitch_voicing_threshold = 0.45
pitch_octave_cost = 0.01
pitch_octave_jump_cost = 0.35
pitch_voiced_unvoiced_cost = 0.14
 
To Pitch (cc)... 0 minimum_pitch 15 no pitch_silence_threshold pitch_voicing_threshold 0.01 0.35 0.14 maximum_pitch
plus Sound 'name$'
 
To PointProcess (cc)
points = Get number of points
 
select Sound 'name$'
plus Pitch 'name$'
plus PointProcess 'name$'_'name$'

# for the whole sound [0 0]
start = 0
end = 0
maximum_period_factor = 1.3
maximum_amplitude_factor = 1.6
report$ = Voice report... start end minimum_pitch maximum_pitch maximum_period_factor maximum_amplitude_factor 0.03 0.45

medianPitch = extractNumber (report$, "Median pitch: ")
meanPitch = extractNumber (report$, "Mean pitch: ")
sdPitch =extractNumber (report$, "Standard deviation: ")
minPitch = extractNumber (report$, "Minimum pitch: ")
maxPitch = extractNumber (report$, "Maximum pitch: ")
pitch_range = maxPitch-minPitch

#####################################
# Jitter and Shimmer
jitter_loc = extractNumber (report$, "Jitter (local): ") * 100
jitter_loc_abs = extractNumber (report$, "Jitter (local, absolute): ") * 1000000
jitter_rap = extractNumber (report$, "Jitter (rap): ") * 100
jitter_ppq5 = extractNumber (report$, "Jitter (ppq5): ") *100
shimmer_loc = extractNumber (report$, "Shimmer (local): ") *100
shimmer_loc_dB = extractNumber (report$, "Shimmer (local, dB): ")
shimmer_apq3 = extractNumber (report$, "Shimmer (apq3): ") * 100
shimmer_apq5 = extractNumber (report$, "Shimmer (apq5): ") * 100
shimmer_apq11 = extractNumber (report$, "Shimmer (apq11): ") * 100
mean_nhr = extractNumber (report$, "Mean noise-to-harmonics ratio: ")
 
#####################################


select Pitch 'name$'
plus PointProcess 'name$'_'name$'
Remove

silencedb = -25
mindip = 2 
showtext = 0
minpause = 0.3
#directory$ = "F:/MIMICRY/wav"
 
# print a single header line with column names and units
#printline soundname, nsyll, npause, dur (s), phonationtime (s), speechrate (nsyll/dur), articulation rate (nsyll / phonationtime), ASD (speakingtime/nsyll)

# read files
#Create Strings as file list... list 'directory$'/*.wav
#numberOfFiles = Get number of strings
#for ifile to numberOfFiles
#   select Strings list
#   fileName$ = Get string... ifile
#   Read from file... 'directory$'/'fileName$'

Read from file... 'inputfolder$''file$'

# use object ID
   soundname$ = selected$("Sound")
   soundid = selected("Sound")

#select Sound 'name$'

   originaldur = Get total duration
   # allow non-zero starting time
   bt = Get starting time

   # Use intensity to get threshold
   To Intensity... 50 0 yes
   intid = selected("Intensity")
   start = Get time from frame number... 1
   nframes = Get number of frames
   end = Get time from frame number... 'nframes'

   # estimate noise floor
   minint = Get minimum... 0 0 Parabolic
   # estimate noise max
   maxint = Get maximum... 0 0 Parabolic
   #get .99 quantile to get maximum (without influence of non-speech sound bursts)
   max99int = Get quantile... 0 0 0.99

   # estimate Intensity threshold
   threshold = max99int + silencedb
   threshold2 = maxint - max99int
   threshold3 = silencedb - threshold2
   if threshold < minint
       threshold = minint
   endif

  # get pauses (silences) and speakingtime
   To TextGrid (silences)... threshold3 minpause 0.1 silent sounding
   textgridid = selected("TextGrid")
   silencetierid = Extract tier... 1
   silencetableid = Down to TableOfReal... sounding
   nsounding = Get number of rows
   npauses = 'nsounding'
   speakingtot = 0
   for ipause from 1 to npauses
      beginsound = Get value... 'ipause' 1
      endsound = Get value... 'ipause' 2
      speakingdur = 'endsound' - 'beginsound'
      speakingtot = 'speakingdur' + 'speakingtot'
   endfor

   select 'intid'
   Down to Matrix
   matid = selected("Matrix")
   # Convert intensity to sound
   To Sound (slice)... 1
   sndintid = selected("Sound")

   # use total duration, not end time, to find out duration of intdur
   # in order to allow nonzero starting times.
   intdur = Get total duration
   intmax = Get maximum... 0 0 Parabolic

   # estimate peak positions (all peaks)
   To PointProcess (extrema)... Left yes no Sinc70
   ppid = selected("PointProcess")

   numpeaks = Get number of points

   # fill array with time points
   for i from 1 to numpeaks
       t'i' = Get time from index... 'i'
   endfor


   # fill array with intensity values
   select 'sndintid'
   peakcount = 0
   for i from 1 to numpeaks
       value = Get value at time... t'i' Cubic
       if value > threshold
             peakcount += 1
             int'peakcount' = value
             timepeaks'peakcount' = t'i'
       endif
   endfor


   # fill array with valid peaks: only intensity values if preceding
   # dip in intensity is greater than mindip
   select 'intid'
   validpeakcount = 0
   currenttime = timepeaks1
   currentint = int1

   for p to peakcount-1
      following = p + 1
      followingtime = timepeaks'following'
      dip = Get minimum... 'currenttime' 'followingtime' None
      diffint = abs(currentint - dip)

      if diffint > mindip
         validpeakcount += 1
         validtime'validpeakcount' = timepeaks'p'
      endif
         currenttime = timepeaks'following'
         currentint = Get value at time... timepeaks'following' Cubic
   endfor


   # Look for only voiced parts
   select 'soundid'
   #select Sound 'name$'
   To Pitch (ac)... 0.02 30 4 no 0.03 0.25 0.01 0.35 0.25 450
   # keep track of id of Pitch
   pitchid = selected("Pitch")

   voicedcount = 0
   for i from 1 to validpeakcount
      querytime = validtime'i'

      select 'textgridid'
      whichinterval = Get interval at time... 1 'querytime'
      whichlabel$ = Get label of interval... 1 'whichinterval'

      select 'pitchid'
      value = Get value at time... 'querytime' Hertz Linear

      if value <> undefined
         if whichlabel$ = "sounding"
             voicedcount = voicedcount + 1
             voicedpeak'voicedcount' = validtime'i'
         endif
      endif
   endfor

  
   # calculate time correction due to shift in time for Sound object versus
   # intensity object
   timecorrection = originaldur/intdur

   # Insert voiced peaks in TextGrid
   if showtext > 0
      select 'textgridid'
      Insert point tier... 1 syllables
     
      for i from 1 to voicedcount
          position = voicedpeak'i' * timecorrection
          Insert point... 1 position 'i'
      endfor
   endif

   # clean up before next sound file is opened
    select 'intid'
    plus 'matid'
    plus 'sndintid'
    plus 'ppid'
    plus 'pitchid'
    plus 'silencetierid'
    plus 'silencetableid'

    Remove
    if showtext < 1
       select 'soundid'
       #select Sound 'name$'
	   plus 'textgridid'
       Remove
    endif

# summarize results in Info window
   speakingrate = 'voicedcount'/'originaldur'
   articulationrate = 'voicedcount'/'speakingtot'
   npause = 'npauses'-1
   asd = 'speakingtot'/'voicedcount'
  
   # Write data in file
   fileappend "'outputfile$'" 
  ...'name$''tab$''minPitch:3''tab$''maxPitch:3''tab$''pitch_range:3''tab$''medianPitch:3''tab$''meanPitch:3''tab$''sdPitch:3''tab$'
  ...'jitter_loc:3''tab$''jitter_loc_abs:3''tab$''jitter_rap:3''tab$''jitter_ppq5:3''tab$'
  ...'shimmer_loc:3''tab$''shimmer_loc_dB:3''tab$''shimmer_apq3:3''tab$''shimmer_apq5:3''tab$''shimmer_apq11:3'
  ...'tab$''mean_nhr:4''tab$''min_int:3''tab$''max_int:3''tab$''mean_int:3''tab$''range_of_int:3''tab$'
  ...'speakingrate:2''tab$''articulationrate:2''tab$''asd:3''newline$'
 
endfor
