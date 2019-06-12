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

echo
echo "Aloha prob"
protocol=" -p aloha"
if [ ! -d "raw_data/aloha_prob" ]; then
  mkdir raw_data/aloha_prob
fi
while IFS= read -r line
do
  python $line $protocol -R
done < "simulation_list.txt"
mv *.csv raw_data/aloha_prob

echo
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

echo
echo "Trivial carrier sensing prob"
protocol=" -p trivial"
if [ ! -d "raw_data/trivial_prob" ]; then
  mkdir raw_data/trivial_prob
fi
while IFS= read -r line
do
  python $line $protocol -R
done < "simulation_list.txt"
mv *.csv raw_data/trivial_prob

echo
echo "Simple carrier sensing disk with p = 0.75"
protocol=" -p simple"
if [ ! -d "raw_data/simple_disk_75" ]; then
  mkdir raw_data/simple_disk_75
fi
while IFS= read -r line
do
  python $line $protocol -P 0.75
done < "simulation_list.txt"
mv *.csv raw_data/simple_disk_75

echo
echo "Simple carrier sensing disk with p = 0.5"
protocol=" -p simple"
if [ ! -d "raw_data/simple_disk_50" ]; then
  mkdir raw_data/simple_disk_50
fi
while IFS= read -r line
do
  python $line $protocol -P 0.5
done < "simulation_list.txt"
mv *.csv raw_data/simple_disk_50

echo
echo "Simple carrier sensing disk with p = 0.25"
protocol=" -p simple"
if [ ! -d "raw_data/simple_disk_25" ]; then
  mkdir raw_data/simple_disk_25
fi
while IFS= read -r line
do
  python $line $protocol -P 0.25
done < "simulation_list.txt"
mv *.csv raw_data/simple_disk_25

echo
echo "Simple carrier sensing disk with p = 0"
protocol=" -p simple"
if [ ! -d "raw_data/simple_disk_00" ]; then
  mkdir raw_data/simple_disk_00
fi
while IFS= read -r line
do
  python $line $protocol -P 0
done < "simulation_list.txt"
mv *.csv raw_data/simple_disk_00

echo
echo "Simple carrier sensing prob with p = 0.75"
protocol=" -p simple"
if [ ! -d "raw_data/simple_prob_75" ]; then
  mkdir raw_data/simple_prob_75
fi
while IFS= read -r line
do
  python $line $protocol -P 0.75 -R
done < "simulation_list.txt"
mv *.csv raw_data/simple_prob_75

echo
echo "Simple carrier sensing prob with p = 0.5"
protocol=" -p simple"
if [ ! -d "raw_data/simple_prob_50" ]; then
  mkdir raw_data/simple_prob_50
fi
while IFS= read -r line
do
  python $line $protocol -P 0.5 -R
done < "simulation_list.txt"
mv *.csv raw_data/simple_prob_50

echo
echo "Simple carrier sensing prob with p = 0.25"
protocol=" -p simple"
if [ ! -d "raw_data/simple_prob_25" ]; then
  mkdir raw_data/simple_prob_25
fi
while IFS= read -r line
do
  python $line $protocol -P 0.25 -R
done < "simulation_list.txt"
mv *.csv raw_data/simple_prob_25

echo
echo "Simple carrier sensing prob with p = 0"
protocol=" -p simple"
if [ ! -d "raw_data/simple_prob_00" ]; then
  mkdir raw_data/simple_prob_00
fi
while IFS= read -r line
do
  python $line $protocol -P 0 -R
done < "simulation_list.txt"
mv *.csv raw_data/simple_prob_00

rm simulation_list.txt

echo "Analysing results and plotting data"
python analysis/main.py
echo "Plots can be found in 'results' folder"
