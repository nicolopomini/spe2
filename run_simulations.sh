#!/bin/bash
export PYTHONPATH=$PYTHONPATH:./simulator/
export PYTHONPATH=$PYTHONPATH:./analysis/
python simulator/main.py -l >> simulation_list.txt
if [ ! -d "raw_data" ]; then
  mkdir raw_data
fi
if [ ! -d "results" ]; then
  mkdir results
fi

echo "Aloha disk"
protocol=" -p aloha"
if [ ! -d "raw_data/aloha_disk" ]; then
  mkdir raw_data/aloha_disk
fi
while IFS= read -r line
do
  python $line $protocol
done < "simulation_list.txt"
mv *.csv raw_data/aloha_disk

echo "Aloha prob"
protocol=" -p aloha"
if [ ! -d "raw_data/aloha_prob" ]; then
  mkdir raw_data/aloha_prob
fi
while IFS= read -r line
do
  python $line $protocol
done < "simulation_list.txt"
mv *.csv raw_data/aloha_prob

echo "Trivial carrier sensing disk"
protocol=" -p trivial"
if [ ! -d "raw_data/trivial_disk" ]; then
  mkdir raw_data/trivial_disk
fi
while IFS= read -r line
do
  python $line $protocol
done < "simulation_list.txt"
mv *.csv raw_data/trivial_disk

echo "Trivial carrier sensing prob"
protocol=" -p trivial"
if [ ! -d "raw_data/trivial_prob" ]; then
  mkdir raw_data/trivial_prob
fi
while IFS= read -r line
do
  python $line $protocol
done < "simulation_list.txt"
mv *.csv raw_data/trivial_prob

rm simulation_list.txt

echo "Analysing results and plotting data"
python analysis/main.py
echo "Plots can be found in 'results' folder"
