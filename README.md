# (2022 Fall) Theory of Computation Project
2022-29307 김대현, 2022-23583 최유진

## Instruction

### Preliminaries

- `matplotlib` and `numpy` library is needed. Install these packages using command below:
```
pip install matplotlib
pip install numpy
```

- Input file is also needed. Our DenForest processes 2 dimesional spatial data and it should be in csv format.
```
126.655185 , 37.57862
126.87673 , 35.130691
...
126.84179 , 37.161333
127.462785 , 36.62359
```

### How to Run
You can run the program using command below.
```
python3.8 ./main.py <input_file_path> <tau_value> <eps_value> <window_size> <stride_size>
```
`ex)python3.8 ./main.py ../dataset/input.csv 5 0.1 1000 20`

### Result
Result is generated using matplotlib's pyplot modules. You can check the clustering result from figure named `result.png` in your working directory.


## Implemenation Details
- *ncoreTable* stores nostalgic cores
- *nodeTable* stores datapoints in the window
- *edgeTable* stores all the edges in the DenTree
