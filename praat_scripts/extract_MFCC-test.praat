# CHANGE THIS TO YOUR DIRECTORY
directory_org$ = "/home/tangmm/telecom/Cours-3A/PIM-imitation/PreCorpusImitateurs/test"
dir_mfcc$ = "/home/tangmm/telecom/Cours-3A/PIM-imitation/PreCorpusImitateurs/test/mfcc"
dir_pitch$ = "/home/tangmm/telecom/Cours-3A/PIM-imitation/PreCorpusImitateurs/test/pitch"

#directory_org$ = "C:\where_my_files_are"

# FIND ALL WAV FILES IN THE DIRECTORY
Create Strings as file list... list 'directory_org$'/*.wav
numberOfFiles = Get number of strings

# LOOP THROUGH ALL THE WAV FILES
for ifile to numberOfFiles

    #OPEN THEM
    select Strings list
    filename$ = Get string... ifile
    baseFile$ = filename$ - ".wav"
    Read from file... 'directory_org$'/'baseFile$'.wav
    
    #CONVERT THEM AND SAVE THEM
    select Sound 'baseFile$'

    To MelFilter... 0.020 0.010 100 100 0
    To MFCC... 12
    To Matrix
    Write to matrix text file... 'dir_mfcc$'/'baseFile$'.txt

    #GET PITCH
    time_step = 0.010
    minimum_pitch = 70
    maximum_pitch = 600
 
    pitch_silence_threshold = 0.03
    pitch_voicing_threshold = 0.45
    pitch_octave_cost = 0.01
    pitch_octave_jump_cost = 0.35
    pitch_voiced_unvoiced_cost = 0.14
 
    select Sound 'baseFile$'
   To Pitch: 0.010, 70, 600
    #To Pitch: time_step, minimum_pitch,  maximum_pitch
    Write to text file... 'dir_pitch$'/'baseFile$'.txt


    #CLEAN UP
    select MelFilter 'baseFile$'
    plus MFCC 'baseFile$'
    plus Matrix 'baseFile$'
    plus Sound 'baseFile$'
    Remove

endfor
