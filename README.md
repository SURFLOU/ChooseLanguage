# ChooseLanguage

It's app which calculates given your preferences which foreign language should you learn next. 

How to initialize an app:

```python
connection = connect_to_db("localhost", "root", "", "language")
create_tables(connection)
df = normalize_df(language_list, connection)
df = set_wages(df, wages_list)

```

Output of dataframe given language_list for instance as Polish and wages_list as [1,2,3,4,5]:

```python
      Language  Lexical_similarity  Phoneme_similarity  Family_of_language  \
0   Portuguese                 0.0            1.625000                 0.0   
1      English                 0.0            1.437500                 0.0   
2      Russian                 1.0            0.000000                 2.0   
3      Spanish                 0.0            1.393939                 0.0   
4    Norwegian                 0.0            1.437500                 0.0   
5       German                 0.0            1.437500                 0.0   
6        Dutch                 0.0            0.821429                 0.0   
7      Italian                 0.0            1.121951                 0.0   
8       French                 0.0            1.150000                 0.0   
9      Swedish                 0.0            1.437500                 0.0   
10      Danish                 0.0            1.437500                 0.0   

    Number_of_hours  Total_speakers  Amount_of_job_offers  Total_sum  
0               3.0        0.812263              0.000000   5.437263  
1               3.0        4.000000              5.000000  13.437500  
2               0.0        0.897650              0.115596   4.013246  
3               3.0        1.877567              0.255561   6.527067  
4               3.0        0.000000              0.241190   4.678690  
5               2.1        0.450289              2.418145   6.405935  
6               3.0        0.063065              0.269308   4.153801  
7               3.0        0.222152              0.270557   4.614660  
8               3.0        0.974288              0.521120   5.645408  
9               3.0        0.026635              0.083729   4.547864  
10              3.0        0.002484              0.254936   4.694921  

```


It calculates such things as:
<ul>
<li> Number of job offers: (based on website pracuj.pl) <img src="https://i.imgur.com/hYnmSOi.png" alt="Number of job offers"> </li>
<li> Total number of native speakers: <img src="https://i.imgur.com/gPtMi4n.png" alt="Number of native speakers"> </li>
<li> Rate of phonemes that are the same in every language:</li>
<br>
Each language has it own phonemes in International Phonetical Alphabet. Each of this phonemes can be written as hexadecimal code, for instance:

```python
german_phonemes = [
    "\u0061", "\u0062", "\u0063", "\u0064", "\u0065", "\u0066", "\u0067", "\u0068", "\u0069", "\u006a", "\u006b", "\u006c",
    "\u006d", "\u006e", "\u006f", "\u0070", "\u0071", "\u0072", "\u0073", "\u0074", "\u0075", "\u0076", "\u0077", "\u0078",
    "\u0079", "\u007a", "\u00e4", "\u00c4", "\u00f6", "\u00d6", "\u00fc", "\u00dc"
]
```
I calculate the ratio how many phonemes differ from one language with another, the less the amount is the higher score is. 
<li> Lexical similarity (based on this study: <a href="http://ukc.disi.unitn.it/index.php/lexsim/"> Study </a> </li>

> Lexical similarity is a measure of the degree to which the word sets of two given languages are similar.
<img src="https://i.imgur.com/U6UjScy.png" alt="Lexical similarity">
<li> Number of hours needed to learn a language (based on FSI) <img src="https://i.imgur.com/8dphukO.png" alt="Number of hours needed"> </li>
<li> Type of family </li>
</ul>
