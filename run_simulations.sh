#!/bin/bash
python simulator/main.py -l >> simulation_list.txt
while IFS= read -r line
do
  python $line
done < "simulation_list.txt"
rm simulation_list.txt
mv *.csv raw_data
