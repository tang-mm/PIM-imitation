# CHANGE THIS TO YOUR DIRECTORY

base_dir$ = "/media/winE/[TelecomParisTech]/Cours-3A/PIM-imitation/test/to_Alliot/"
directory_org$ = base_dir$ + "wav/"
dir_mfcc$ = base_dir$ + "mfcc/"
dir_pitch$ = base_dir$ + "pitch/"
dir_formant_1$ = base_dir$ + "formant_1/"
dir_formant_2$ = base_dir$ + "formant_2/"

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
    # time_step, minimum_pitch,  maximum_pitch
    To Matrix
    Write to matrix text file... 'dir_pitch$'/'baseFile$'.txt

    # f0 = Get quantile: 0, 0, 0.50, "Hertz"
	# appendFileLine: 'dir_pitch$'/'baseFile$'.txt, " : F0 = ", f0


    # GET FORMANT----------------------
    # Default max =5500 Hz (adult female); for a male, use 5000 Hz; young child, beyond 5500Hz.
    select Sound 'baseFile$'
	#To Formant (burg)... time_step maximum_number_of_formants maximum_formant window_length preemphasis_from
   To Formant (burg)... 0.010 5 5000 0.025 50
    # F1
    To Matrix... 1      
    Write to matrix text file... 'dir_formant_1$'/'baseFile$'.txt
    # F2
    select Formant 'baseFile$'
    To Matrix... 2    
    Write to matrix text file... 'dir_formant_2$'/'baseFile$'.txt

    # CLEAN UP ----------------------
    select MFCC 'baseFile$'
    plus  Pitch 'baseFile$'
    plus Formant 'baseFile$'
    plus Matrix 'baseFile$'
    plus Sound 'baseFile$'
    Remove

endfor

