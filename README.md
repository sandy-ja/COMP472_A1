# :beers: COMP 472 – Assignment 1 :tiger:

---

Axel Bogos - 40077502 <br>
Luan Meiyi - 40047658 <br>
Xavier Morin - 40077865

---

## Preliminary Information

---
#### Libraries Used:
* pandas
* seaborn
* matplotlib
* numpy
* sklearn 
---

## How To Run 

---

Execute the main() function of ```main.py```. This will execute the following functions and model calls, in that order: 
```python
    plot_data(df_train)
    GNB(df_train,df_val)
    Base_DT(df_train,df_val)
    Best_DT(df_train,df_val)
    PER(df_train, df_val)
    Base_MLP(df_train, df_val)
    Best_MLP(df_train, df_val)
```
where the plot function and each model call generate their output files in the directory 'results' with the following structure
```
.
│ main.py
│ __init__.py    
│ README.md
│
└───results
│   │
│   │ dataset1-plot.png
│   │ dataset2-plot.png
│   │
│   └───GNB-DS1
|   |   | GNB-DS1.csv
|   |   | GNB-DS1-Confusion_Matrix.png
|   |
│   └───GNB-DS2.csv
|   |   | GNB-DS2.csv
|   |   | GNB-DS2-Confusion_Matrix.png
|   |   
│   └───Base-DT-DS1
|   |   | Base-DT-DS1.csv
|   |   | Base-DT-DS1-Confusion_Matrix.png
|   |   
│   └───Base-DT-DS2
|   |   | Base-DT-DS2.csv
|   |   | Base-DT-DS2-Confusion_Matrix.png
|   |   
│   └───Best-DT-DS1
|   |   | Best-DT-DS1.csv
|   |   | Best-DT-DS1-Confusion_Matrix.png
|   |   
│   └───Best-DT-DS2
|   |   | Best-DT-DS2.csv
|   |   | Best-DT-DS2-Confusion_Matrix.png
|   |   
│   └───PER-DS1
|   |   | PER-DS1.csv
|   |   | PER-DS1-Confusion_Matrix.png
|   |   
│   └───PER-DS2
|   |   | PER-DS1.csv
|   |   | PER-DS1-Confusion_Matrix.png
|   |   
│   └───Base-MLP-DS1
|   |   | Base-MLP-DS1.csv
|   |   | Base-MLP-DS1-Confusion_Matrix.png
|   |   
│   └───Base-MLP-DS2
|   |   | Base-MLP-DS2.csv
|   |   | Base-MLP-DS2-Confusion_Matrix.png
|   |   
│   └───Best-MLP-DS1
|   |   | Best-MLP-DS1.csv
|   |   | Best-MLP-DS1-Confusion_Matrix.png
|   |   
│   └───Best-MLP-DS2
|       | Best-MLP-DS2.csv
|       | Best-MLP-DS2-Confusion_Matrix.png
|   
└───data
    │   ...
```
---
