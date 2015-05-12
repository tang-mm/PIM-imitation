Draw: 0,0,0,0,"yes","Curve"
Draw: 1.0, 3.2, -1, 1, "no", "Poles"
writeInfoLine: "hello world"
appendInfoLine: "hahahahah"
Text top: "yes", "hello world"

selectObject: 7
To Spectrum: "yes"
Draw: 0, 5000, 20, 80, "yes"

selectObject: 7
name$ = selected$ ("Sound")
fullName$ = selected$ ()
writeInfoLine: name$
appendInfoLine: fullName$

#----------
writeInfoLine: ""
selectObject: 7
plusObject: 8

n = numberOfSelected ("Sound")
for i to n
	sound[i] = selected ("Sound", i)
endfor
# Median pitches of all selected sounds:
for i to n
	selectObject: sound[i]
	To Pitch: 0.0, 75, 600
	f0 = Get quantile: 0, 0, 0.50, "Hertz"
	appendInfoLine: selected$ (), " : F0 = ", f0
	Remove
endfor
# restore selection: 
selectObject()	;deselect all
for i from 1 to n
	plusObject: sound[i]
endfor