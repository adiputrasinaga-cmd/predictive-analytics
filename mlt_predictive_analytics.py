# -*- coding: utf-8 -*-
"""MLT-Predictive_Analytics.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Nm9FJirIHJXgNwJ1nOvsB5YrMFYK4Wnb

# Proyek Machine Learning : Predictive Analytics

* Domain : Ekonomi dan Pendidikan
* Tujuan : Melakukan Prediksi pendapatan(**salary**) Lulusan Jurusan Teknik di India
* Dataset yang digunakan : https://www.kaggle.com/manishkc06/engineering-graduate-salary-prediction

## Melakukan Import terhadap Library yang diperlukan
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# %matplotlib inline
import seaborn as sns

from sklearn.preprocessing import OneHotEncoder
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.metrics import mean_squared_error
from pandas import read_csv

"""## DATA UNDERSTANDING

### Memuat Dataset ***Engineering_graduate_salary.csv*** pada variabel **"df"**
"""

df = read_csv('drive/MyDrive/csv/Engineering_graduate_salary.csv')

"""### Menampilkan tipe data setiap kolom pada dataset "df""""

df.info()

"""### Menghapus(**drop**) kolom/fitur yang tidak diperlukan"""

df.drop(
    ['ID', 'DOB', '10board', '12board', 'CollegeID', 'CollegeTier', 
     '10percentage','12graduation', '12percentage', 'CollegeCityID', 
     'CollegeCityTier','Degree','GraduationYear'], 
    axis='columns', 
    inplace=True
)

"""### Menampilkan tipe data setiap kolom pada dataset "df" setelah proses ***drop***"""

df.info()

"""###  Deskripsi Variabel Numerik"""

df.describe()

"""### Mendapatkan ukuran(***shape***) dari dataset"""

df.shape

"""### Melakukan pemeriksaan terhadap nilai yang hilang(***missing value***) pada dataset"""

df.isnull().sum()

"""### Memvisualisasikan data menggunakan ***boxplot*** untuk fitur numerik:
<ul>
  <li>[collegeGPA]</li>
  <li>[English]</li>
  <li>[Logical]</li>
  <li>[Quant]</li>
  <li>[Domain]</li>
  <li>[ComputerProgramming]</li>
  <li>[ElectronicsAndSemicon]</li>
</ul>
"""

sns.boxplot(x=df['collegeGPA'])

sns.boxplot(x=df['English'])

sns.boxplot(x=df['Logical'])

sns.boxplot(x=df['Quant'])

sns.boxplot(x=df['Domain'])

sns.boxplot(x=df['ComputerProgramming'])

sns.boxplot(x=df['ElectronicsAndSemicon'])

"""### Mengatasi masalah ***outlier*** dengan Metode IQR"""

Q1 = df.quantile(0.25)
Q3 = df.quantile(0.75)
IQR = Q3-Q1
df=df[~((df<(Q1-1.5*IQR))|(df>(Q3+1.5*IQR))).any(axis=1)]

"""### Menampilkan ukuran dataset setelah ***outliers*** diatasi"""

df.shape

"""### Menampilkan tipe data setiap kolom pada dataset "df" setelah proses ***outliers*** diatasi"""

df.info()

"""### Menganalisa data menggunakan Univariate Analysis

#### Membagi fitur numerik dan kategorik yang terdapat pada dataset ####
"""

numeric_feature = ['collegeGPA', 'English', 'Logical', 'Quant',  'Domain',
                 'ComputerProgramming',   'ElectronicsAndSemicon',  'ComputerScience',
                 'MechanicalEngg', 'ElectricalEngg', 'TelecomEngg', 'CivilEngg',
                 'conscientiousness', 'agreeableness', 'extraversion', 'nueroticism',
                 'openess_to_experience', 'Salary']
category_feature = ['Gender', 'Specialization', 'CollegeState']

"""#### Menganalisa fitur kategori ###"""

feature = category_feature[0]
count = df[feature].value_counts()
percent = 100*df[feature].value_counts(normalize=True)
dataFrame = pd.DataFrame({'Jumlah sampel':count, 'persentase':percent.round(1)})
print(dataFrame)
count.plot(kind='bar', title=feature)

"""#### Menganalisa fitur specialization"""

feature = category_feature[1]
count = df[feature].value_counts()
percent = 100*df[feature].value_counts(normalize=True)
dataFrame = pd.DataFrame({'Jumlah sampel':count, 'persentase':percent.round(1)})
print(dataFrame)
count.plot(kind='bar', title=feature)

"""#### Menganalisa fitur CollegeState"""

feature = category_feature[2]
count = df[feature].value_counts()
percent = 100*df[feature].value_counts(normalize=True)
dataFrame = pd.DataFrame({'Jumlah sampel':count, 'persentase':percent.round(1)})
print(dataFrame)
count.plot(kind='bar', title=feature)

"""### Menganalisa data menggunakan Multivariate Analysis"""

# fitur kategori dan numerik
category = df.select_dtypes(include='object').columns.to_list()

for col in category:
  sns.catplot(x=col, y="Salary", kind="bar", dodge=False, height = 4,
              aspect = 5, data=df, palette="Set3")

"""### Menampilkan Plot Pair fitur numerik"""

sns.pairplot(df, diag_kind='kde')

"""### Melakukan pengamatan terhadap tingkat korelasi dengan menggunakan matrik korelasi pada tiap fitur"""

plt.figure(figsize=(10, 8))
correlation_matrix = df.corr().round(2)

sns.heatmap(data=correlation_matrix, annot=True, cmap='coolwarm', linewidth=0.5)
plt.title("Matrik Korelasi fitur numerik", size=20)

"""### Menghapus fitur yang nilai tingkat korelasinya lemah 

<ul type="none">
  <li>Semakin dekat nilainya ke 0, korelasinya semakin lemah</li>
</ul>
"""

df.drop(['ComputerScience', 'MechanicalEngg', 'ElectricalEngg', 'CivilEngg', 'TelecomEngg'], inplace=True, axis=1)

"""### Menampilkan dataset "df" setelah proses drop"""

df

"""### Menampilkan kembali matrik korelasi fitur numerik"""

plt.figure(figsize=(10, 8))
correlation_matrix = df.corr().round(2)

sns.heatmap(data=correlation_matrix, annot=True, cmap='coolwarm', linewidth=0.5)
plt.title("Matrik Korelasi fitur numerik", size=20)

"""## DATA PREPARATION

### Encoding Fitur Kategorik ###
"""

df = pd.concat(
    [df, pd.get_dummies(df['Gender'], 
    prefix='Gender',
    drop_first=True)], 
    axis=1
)

df = pd.concat(
    [df, pd.get_dummies(df['Specialization'], 
    prefix='Specialization',
    drop_first=True)], 
    axis=1
)

df = pd.concat([df, pd.get_dummies(
    df['CollegeState'], 
    prefix='CollegeState',
    drop_first=True)], 
    axis=1
)

df.drop(['Gender', 'Specialization', 'CollegeState'], axis=1, inplace=True)

"""### Menampilkan dataset ***df*** setelah proses ***Encoding***"""

df

"""### Membuat plot berpasangan pada fitur numerik"""

sns.pairplot(
    df[['English',	'Logical',	'Quant',	'Domain',	'ComputerProgramming',
        'ElectronicsAndSemicon',	'conscientiousness',	'agreeableness',
        'extraversion',	'nueroticism',	'openess_to_experience']], 
    plot_kws = {"s":5}
)

"""### Menerapkan PCA pada fitur numerik"""

pca = PCA(n_components=11, random_state=123)
pca.fit(
    df[['English',	'Logical',	'Quant',	'Domain',	'ComputerProgramming',
        'ElectronicsAndSemicon',	'conscientiousness',	'agreeableness',
        'extraversion',	'nueroticism',	'openess_to_experience']])

"""### Melihat informasi proporsi ratio PC pada 11 fitur numerik"""

pca.explained_variance_ratio_.round(2)

"""### Mereduksi dimensi dengan menggunakan fitur baru"""

pca = PCA(n_components=1, random_state=123)

pca.fit(
    df[['English',	'Logical',	'Quant',	'Domain',	'ComputerProgramming',
        'ElectronicsAndSemicon',	'conscientiousness',	'agreeableness',
        'extraversion',	'nueroticism',	'openess_to_experience']]
)

df['AMCATscore'] = pca.transform(
    df.loc[:, ('English',	'Logical',	'Quant',	'Domain',	'ComputerProgramming',
              'ElectronicsAndSemicon',	'conscientiousness',	'agreeableness',
              'extraversion',	'nueroticism',	'openess_to_experience')]
).flatten()

df.drop(
    ['English',	'Logical',	'Quant',	'Domain',	'ComputerProgramming',
      'ElectronicsAndSemicon',	'conscientiousness',	'agreeableness',
      'extraversion',	'nueroticism',	'openess_to_experience'],
      axis=1, inplace=True
)

"""### Menampilkan dataset ***df*** setelah proses reduksi dimensi"""

df

"""### Membagi dataset menjadi train dan test"""

X = df.drop(["Salary"], axis=1)
y = df["Salary"]
X_train, X_test, y_train, y_test = train_test_split (X, y, test_size = 0.2, random_state=123)

print(f'Total of sample in whole dataset: {len(X)}')
print(f'Total of sample in train dataset: {len(X_train)}')
print(f'Total of sample in test dataset: {len(X_test)}')

"""### Menerapkan teknik Standarisasi 

<ul type="none" align="justify">
  <li>Algoritma machine learning memiliki performa lebih baik dan konvergen lebih cepat ketika dimodelkan pada data dengan skala relatif sama atau mendekati distribusi normal. Proses standarisasi dapat membantu untuk membuat fitur data menjadi bentuk yang lebih mudah diolah oleh algoritma. </li>
</ul>
"""

numeric_feature = ['collegeGPA', 'AMCATscore']
scaler = StandardScaler()
scaler.fit(X_train[numeric_feature])
X_train[numeric_feature]

"""### Menampilkan data numerik x_train setalah proses ***Standarisasi***"""

X_train[numeric_feature].describe().round(4)

"""### Melakukan Proses ***Scaling*** terhadap data uji

<ul type="none" align="justify">
  <li>
    Hal ini harus dilakukan agar skala antara data latih dan data uji sama dan kita bisa melakukan evaluasi.
  </li>
</ul>
"""

X_test.loc[:, numeric_feature] = scaler.transform(X_test[numeric_feature])

"""## MODEL DEVELOPMENT

### Menyiapkan dataframe untuk analisa model
"""

models = pd.DataFrame(
    index=['train_mse', 'test_mse'],
    columns=['KNN', 'RandomForest', 'Boosting']
)

"""#### Model prediksi dengan algoritma KNN"""

KNN = KNeighborsRegressor(n_neighbors=100)
KNN.fit(X_train, y_train)
y_pred_KNN = KNN.predict(X_train)

"""#### Model prediksi dengan algoritma Random Forest"""

RF = RandomForestRegressor(n_estimators=100, max_depth=1, random_state=123, n_jobs=-1)
RF.fit(X_train, y_train)

models.loc['train_mse','RandomForest'] = mean_squared_error(y_pred=RF.predict(X_train), y_true=y_train)

"""#### Model prediksi dengan algoritma Boosting Algorithm : Adaptive Boosting"""

boosting = AdaBoostRegressor(n_estimators=100, learning_rate=0.005, random_state=123)
boosting.fit(X_train, y_train)
models.loc['train_mse', 'Boosting'] = mean_squared_error(y_pred=boosting.predict(X_train),
                                                         y_true=y_train)

"""## EVALUASI MODEL

<ul type="none" align="justify">
  <li>
  Secara umum, jika nilai prediksi mendekati nilai sebenarnya, performanya baik. Sedangkan jika tidak, performanya buruk. Secara teknis, selisih antara nilai sebenarnya dan nilai prediksi disebut eror. Maka, semua metrik mengukur seberapa kecil nilai eror tersebut.  
  </li>
</ul>

### Mengevaluasi ketiga model prediksi dengan metrik MSE

<ul type="none" align="justify">
  <li>
Metrik yang gunakan pada prediksi ini adalah MSE(Mean Squared Error) yang menghitung jumlah selisih kuadrat rata-rata nilai sebenarnya dengan nilai prediksi.
  </li>
</ul>
"""

mse = pd.DataFrame(columns=['train', 'test'], index=['KNN', 'RF', 'Boosting'])
model_dict = {'KNN': KNN, 'RF': RF, 'Boosting':boosting}

for name, model in model_dict.items():
  mse.loc[name, 'train'] = mean_squared_error(y_true=y_train, y_pred=model.predict(X_train))/1e6
  mse.loc[name, 'test'] = mean_squared_error(y_true=y_test, y_pred=model.predict(X_test))/1e6

# Data metrik MSE 
mse

"""### Membuat Plot metrik MSE dengan bar chart"""

fig, ax = plt.subplots()
mse.sort_values(by='test', ascending=False).plot(kind='barh', ax=ax, zorder=3)
ax.grid(zorder=0)

"""### Pengujian model prediksi menggunakan nilai ***Salary*** dari dataset"""

prediksi = X_test.iloc[:1].copy()
pred_dict = {'Salary':y_test[:1]}

for name, model in model_dict.items():
  pred_dict['prediksi_'+name] = model.predict(prediksi).round(1)

pd.DataFrame(pred_dict)

"""## KESIMPULAN
<ul type="none" align="justify">
  <li>
Pengujian setiap model dengan algoritma yang berbeda menghasilkan nilai prediksi yang berbeda pula. Model dengan nilai yang mendekati nilai sebenarnya diperoleh pada prediksi dengan menggunakan algoritma Random Forest. Untuk 
prediksi menggunakan algoritma K-Nearest Neighbor dan Boosting, performanya masih dibawah prediksi model Random Forest. Sehingga dapat disimpulkan bahwa pada kasus ini, model dengan menggunakan Algoritma Random Forest lebih tepat untuk digunakan atau diterapkan.
  </li>
</ul>
"""