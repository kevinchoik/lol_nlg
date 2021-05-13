for r in all bandlecity bilgewater demacia demon ionia ixtal nomad noxus piltover shadowisles shurima targon freljord void zaun
do
	for m in 0 1 2
	do
		python3 model.py -r $r -m $m  > ./Results/$r$m.txt
	done
done
