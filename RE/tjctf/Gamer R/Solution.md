# Game R

 - We get a zip file, with file size of ~24mb. This is a Unity game
   challenge.
 - The game is simple, just throw the knife, but don't kill the duck or
   you will lose.
 - Unity game usually contains code in `Assembly-CSharp.dll` file, so I
   use dnspy to open it.
- After reading the source code, I realize this piece of code look suspicious
```csharp
protected  override  void  OnUpdate()  
{  
	for  (int  i  =  0;  i  <  this.text.Length;  i++)  
	{  
		if  (this.text.ScoreComponents[i].Score  /  20  <  this.text.ScoreComponents[i].TextSeq.Length  &&  this.text.ScoreComponents[i].Score  %  20  ==  0)  
		{  
			this.text.Texts[i].text  =  ((char)(this.text.ScoreComponents[i].TextSeq[this.text.ScoreComponents[i].Score  /  20]  ^  (int)(this.text.ScoreComponents[i].CumScore  %  4096.0))).ToString();  
		}  
		else  
		{  
			this.text.Texts[i].text  =  this.text.ScoreComponents[i].Score.ToString();   
		}  
	}  
}
```
The is a `xor` operation in the `ScoreUpdateSystem` class method, so I think that there are something to do with the score.
The code above will give us 1 letter when we reach `20, 40, 60, 80, ...` point.
After some debugging, I found that `this.text.ScoreComponents[i].TextSeq.Length` is 80, so we have to get 1600 point to get all letters.
Play the game is borring, so I modify the code above to:
```csharp
protected  override  void  OnUpdate()  
{  
	for  (int  i  =  0;  i  <  this.text.Length;  i++)  
	{  
		if  (this.text.ScoreComponents[i].Score  /  20  <  this.text.ScoreComponents[i].TextSeq.Length  &&  this.text.ScoreComponents[i].Score  %  20  ==  0)  
		{  
			this.text.Texts[i].text  =  ((char)(this.text.ScoreComponents[i].TextSeq[this.text.ScoreComponents[i].Score  /  20]  ^  (int)(this.text.ScoreComponents[i].CumScore  %  4096.0))).ToString();  
		}  
		else  
		{  
			this.text.Texts[i].text  =  this.text.ScoreComponents[i].Score.ToString();
			string  contents  =  string.Join<int>("|",  this.text.ScoreComponents[i].TextSeq);
			File.WriteAllText("out.txt",  contents); 
		}  
	}  
}
```
Recompile the dll, and run the game again, now I have all value of this array.
## Solution
Run this script, I got the flag
```python
a = '72|183|838|1859|3215|969|3196|1786|568|4039|3748|3728|148|1259|2507|126|2265|541|3489|2785|2362|2367|2780|3650|671|2349|335|2815|1526|589|108|3992|303|1120|2133|3654|1408|3739|2548|1455|944|648|943|1628|2643|4068|1730|4016|2496|1479|890|618|749|1257|2127|3392|1054|3244|1627|502|3756|3328|3567|3914|742|1833|3547|1492|3917|2644|1718|1383|1167|1613|2422|3351|790|2925|1097|3747'
a = a.split('|')
a = list(map(int, a))

m = ''
score = 0
cum_score = 0
for i in range(1600):
    if divmod(score, 20)[0] < len(a) and divmod(score, 20)[1] == 0:
        m += chr((a[score//20] ^ (cum_score % 4096)) & 0xFF)
    score += 1
    cum_score += score
print (m)
```

Flag: `tjctf{orenji_orange}`