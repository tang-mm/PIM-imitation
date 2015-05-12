# CHANGE THIS TO YOUR DIRECTORY
#directory_org$ = "/home/tangmm/telecom/Cours-3A/PIM-imitation/PreCorpusImitateurs/test/wav"
directory_org$ = "/media/winE/[TelecomParisTech]/Cours-3A/PIM-imitation/test/wav"
dir_mfcc$ = "/media/winE/[TelecomParisTech]/Cours-3A/PIM-imitation/test/mfcc"
dir_pitch$ = "/media/winE/[TelecomParisTech]/Cours-3A/PIM-imitation/test/pitch"

# FIND ALL WAV FILES IN THE DIRECTORY
Create Strings as file list... list 'directory_org$'/*.wav
numberOfFiles = Get number of strings

# LOOP THROUGH ALL THE WAV FILES
for ifile to numberOfFiles

    # OPEN ----------------------
    select Strings list
    filename$ = Get string... ifile
    baseFile$ = filename$ - ".wav"
    Read from file... 'directory_org$'/'baseFile$'.wav
    
    # GET MFCC ----------------------
    select Sound 'baseFile$'

#    To MelFilter... 0.020 0.010 100 100 0
    To MFCC... 12 0.050 0.010 100 100 0
    To Matrix
    Write to matrix text file... 'dir_mfcc$'/'baseFile$'.txt

    # GET PITCH----------------------
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

    # f0 = Get quantile: 0, 0, 0.50, "Hertz"
	# appendFileLine: 'dir_pitch$'/'baseFile$'.txt, " : F0 = ", f0


    # GET FORMANT----------------------

	#To Formant (burg)... time_step maximum_number_of_formants maximum_formant window_length preemphasis_from
    

    # CLEAN UP ----------------------
#    select MelFilter 'baseFile$'    plus 
   select MFCC 'baseFile$'
    plus Matrix 'baseFile$'
    plus Sound 'baseFile$'
    Remove

endfor

