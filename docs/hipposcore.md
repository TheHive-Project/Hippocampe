# Hipposcore

## Introduction

Hippocampe allows analysts to configure a confidence level for each feed that can be changed over time. When queried, it will provide a score called Hipposcore that will aid the analyst decide whether the analyzed observables are innocuous or rather malicious.

For the record, the hipposcore is between [-100 ; +100].
If positive, the data scored is likely to be not malicious.
On the other hand, if negative, it is likely to be malicious.
In other words, the sign indicates the data's category (malicious / not malicious).

The score's value answers the confidence question.
Higher it tends towards ```-100```, higher the intel is trustworthy to be malicious.
The other way around, higher it tends to ```+100```, higher the intel is trustworthy to **not** be malicious.

![hipposcore_range](hipposcore_range.png)

The Hipposcore formula is:

![hipposcore](hipposcore.png)

The formula is derived from the capacitor's charge formula. It is a product with three parts. We are going to explain each in turn.

## The percentage

![hipposcore_percentage](hipposcore_percentage.png)

The easiest part is the third term: ``` * 100 ```. It is used to make the score a percentage.

## The main part

![hipposcore_main_part](hipposcore_main_part.png)

The main part is quite difficult to understand.

### The blind-full confidence

First it has ```1``` because each feed is believed to be trustworthy with the maximum value (1), **at the beginning**. 

Then a value is subtracted from this blind-full confidence, and to be precise ```exp(-k |P|)``` is subtracted.

> But why exp(-k |P|) ? Where does it come from?    

To answer this question, let's have a look at ```P```.

### P: source's confidence, time factor and occurrences

![p](p.png)

With:    

* ```n1```: the source's score
* ```n3```: a timeFactor function, depends on the feed data's age

> Why is a sum needed?

Hipposcore takes in consideration the confidence in the source of the data (*n1*) and the time factor: the longer the data is present in the source, the less relevant it is.     

If the data is present in several feeds (a.k.a. sources), this also has to be taken in count hence the sum.

Let's illustrate this with a fictitious example and calculate ```P``` for the ```evil.com```  domain.```evil.com``` is listed in two feeds:
 
   * ```superFeed```
   * ```hyperFeed```


```superFeed``` source score is ```-100``` and ```hyperFeed``` source score is ```-90```.```evil.com``` was last listed in:

   * ```superFeed``` 2 days ago
   * ```hyperFeed``` 3 days ago

From that P is:

```
    P = sum[n1 * n3]
    
<=> P = [n1 superFeed * n3 superFeed] + [n1 hyperFeed * n3 hyperFeed]
        
<=> P = [superFeed source's score * timeFactor(intel age in superFeed)] + [hyperFeed source's score * timeFactor(intel age in hyperFeed)]
 
```

> How does the timeFactor function works?

#### timeFactor Function

As described above, the longer the data is present in the source, the less relevant it is. If the data is too old, ```n3``` must be smaller and have less impact on the overall result. To do so ```n3``` is computed according to the following formula:

![n3](n3.png)

Where ```t``` is the data's age.

> Why is it a time factor formula?

Let's have a look at the function:

![graph1](graph1.png)

From the graph, the function tends to 0 as the data's age increases.

![graph2](graph2.png)

If the data is one year old (```t = 365```), ```n3``` wil be less than ```0.2``` but if it is super fresh and has been added today to the feed (```t = 0```) ```n3``` will be at the max value which is 1.

> But why 182.625 in the n3 formula?

Let's have a look at some interesting values of ```n3``` over time:

|  Example  |  1  |  2  |  3  |
|  -------  | --- | --- | --- |
|  t  |  0  |  182.625  |  365  |    
|  n3  |  1  |  0.37  |  0.13  |    

```182.625``` is the period. It means that when the data's age reaches this value (```t = 182.625```), ```n3``` will lose **63%** of its original value (which it has when ```t = 0```).   

And if you haven't noticed yet, ```182.625``` is equivalent to 6 months. So after 6 months ```n3``` loses **63%**, a physics/mathematics fact.

Given these explanations, lets' get back to ```P```:

```
    P = sum[n1 * n3]
    
<=> P = [n1 superFeed * n3 superFeed] + [n1 hyperFeed * n3 hyperFeed]
        
<=> P = [superFeed source's score * timeFactor(intel age in superFeed)] + [hyperFeed source's score * timeFactor(intel age in hyperFeed)


# Resuming the calculation with values previously given:

<=> P = [-100 * exp(-2 / 182.625)] + [-90 * exp(-3 / 182.625)]

<=> P = [-100 * 0.99] + [-90 * 0.98]

<=> P = -99 + -88.2

<=> P = -187.2
 
```

> I understand that P is a combination of the confidence in the feed/source, the time factor and the number of feeds where the data is present but I don't really see the point...

If you understand this far, that's excellent but some effort is still required to fully grasp the Hipposcore. Remember ```exp(-k |P|)```? Let's do some math:

First consider ```exp(-k P)```, P can be any value between ```[-infinite ; +infinite]``` but if P is between ```[-infinite ; 0]``` the result will be between ```[+infinite ; 1]```.

Since the *blind-full confidence* is set to ```1``` we cannot subtract more trust than ```1```. It does not make sense. Thankfully, if P is between ```[0 ; +infinite]```, the result will be between ```[1 ; 0]``` so **the bigger ```P``` is, the less 'trust' we'll need to subtract**. Moreover, it also means that **```[1 - exp( -k |P|)]``` is always positive**.

The variation table below sums up the behavior of ```exp(-k x)```. Please note that the descriptions are in French but this shouldn't prevent you from getting the idea. And to map the table to our use case, assume that ```x``` is equivalent to ```P```.

![variation_table](variation_table.png)

> But we can't force P to be positive. Can we?

That is right. We can't force ```P``` to be positive. However, thanks to the absolute value function, we can force ```P``` to be positive **in the exponential function only**. And that answers why ```exp(-k |P|)```.

> Wait... What about k? What is its purpose?

```k``` acts like an amplifier/attenuator. For a given value of ```P```, if ```k``` is negative, the smaller it is the more 'trust' will be subtracted. In the other hand, if ```k``` is positive, the bigger it is the less 'trust' will be subtracted:

|  Example  |  1  |  2  |  3  |  4  |  5  |  6  |
| --------  | --- | --- | --- | --- | --- | --- |
|  ```|P|```  |  1  |  1  |  1  |  1  |  1  |  1  |     
|  ```k```  |  1  |  2  |  4  | -1  |  -2  |  -4  |     
|  ```exp(-k |P|) (trust to be subtracted)```  |  0.37  |  0.14  |  0.02  |  2.7  |  7.4  |  54.6 |     

For your information, we set ```k``` with the value ```2```.

## Malicious or not?
Finally, let's move to the final part:
![hipposcore_sign](hipposcore_sign.png)

Until now, we have just subtracted some 'trust' (based on the confidence we have in the feed, a time factor and the number of occurences of the data across several feeds) from a Hipposcore set at a maximum value (1). But there are no hints on whether or not the data we queried Hippocampe for is malicious or not. This categorization is done through that last part, the sign part.   

Again P is:

![p](p.png)

With:    

* ```n1```: the source's score
* ```n3```: a timeFactor function, depends on the feed data's age  

If the data is malicious, its source's score is negative and P is negative as well.      
If the data is not malicious, its source's score is positive and P is positive.    

Consider the following use cases:

* the data is malicious => ```n1``` is negative => P is negative => ```|P| / P = -1```
   * Hipposcore is negative
* the data is not malicious => ```n1``` is positive => P is positive => ```|P| / P = 1```
   * Hipposcore is positive

A negative Hipposcore means it is probably malicious and the lower the value is (Hipposcore tends towards -100), the higher confidence we have in the malicious nature of the data.   

A positive Hipposcore means it is probably not malicious and the higher the value is (Hipposcosre tends towards 100) and the more confidence in the innocuous nature of the data.

