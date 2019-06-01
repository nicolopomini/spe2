#!/bin/bash
export PYTHONPATH=$PYTHONPATH:./analysis/
python simulator/main.py -l >> simulation_list.txt
if [ ! -d "raw_data" ]; then
  mkdir raw_data
fi
if [ ! -d "results" ]; then
  mkdir results
fi

echo "Aloha disk"
if [ ! -d "raw_data/aloha_disk" ]; then
  mkdir raw_data/aloha_disk
fi
while IFS= read -r line
do
  python $line
done < "simulation_list.txt"
mv *.csv raw_data/aloha_disk

echo "Aloha prob"
if [ ! -d "raw_data/aloha_prob" ]; then
  mkdir raw_data/aloha_prob
fi
while IFS= read -r line
do
  python $line
done < "simulation_list.txt"
mv *.csv raw_data/aloha_prob

echo "Trivial carrier sensing disk"
if [ ! -d "raw_data/trivial_disk" ]; then
  mkdir raw_data/trivial_disk
fi
while IFS= read -r line
do
  python $line
done < "simulation_list.txt"
mv *.csv raw_data/trivial_disk

echo "Trivial carrier sensing prob"
if [ ! -d "raw_data/trivial_prob" ]; then
  mkdir raw_data/trivial_prob
fi
while IFS= read -r line
do
  python $line
done < "simulation_list.txt"
mv *.csv raw_data/trivial_prob

rm simulation_list.txt

echo "Analysing results and plotting data"
python analysis/main.py
echo "Plots can be found in 'results' folder"
