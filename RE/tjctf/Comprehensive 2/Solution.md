# Comprehensive 2

This is another python problem:
```python
m = '[?????]'
n = '[?????]'

a = 'abcdefghijklmnopqrstuvwxyz'
p = ' !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

assert len(m) == 63 and set(m).issubset(set(a + p))
assert len(n) == 7  and set(n).issubset(set(a))
assert m.count('tjctf{') == 1 and m.count('}') == 1 and m.count(' ') == 5

print(str([x for z in [[[ord(m[i]) ^ ord(n[j // 3]) ^ ord(n[i - j - k]) ^ ord(n[k // 21]) for i in range(j + k, j + k + 3)] for j in range (0, 21, 3)] for k in range(0, len(m), 21)] for y in z for x in y])[1:-1])
```

> Output: `[1, 18, 21, 18, 73, 20, 65, 8, 8, 4, 24, 24, 9, 18, 29, 21, 3, 21, 14, 6, 18, 83, 2, 26, 86, 83, 5, 20, 27, 28, 85, 67, 5, 17, 2, 7, 12, 11, 17, 0, 2, 20, 12, 26, 26, 30, 15, 44, 15, 31, 0, 12, 46, 8, 28, 23, 0, 11, 3, 25, 14, 0, 65]`

The print statement at the very last of the script can be rewritten like this
```python
z = []
for k in [0,21,42]:
	for j in [0,3,6,9,12,15,18]:
		for i in range(k + j, k + j + 3):
			tmp = ord(m[i]) ^ ord(n[j // 3]) ^ ord(n[i - j - k]) ^ ord(n[k // 21])
			z.append(tmp)
print (z)
```

## Solution
Use z3 to solve this problem. Run `solve.py`, we get a lot of solutions
```
(env) osboxes@osboxes:~/Desktop$ python solve.py
hata o sagashiteimtf` ka? dozo, tjctf{s`x|masen_flag_kudasai|h;
kbwb#l#pbgashiteim`rt#hb<#glyl, tjctf{stlhnbpfm\eobg_kudasaih|/
kbwb#l#pbgashiteimdvp#hb<#glyl, tjctf{sphlnbpfm\eobg_kudasailx+
lepe$k$wegashiteimdvp$oe;$`k~k, tjctf{sphliewaj[bheg_kudasailx+
hata o sagashiteimdvp ka? dozo, tjctf{sphlmasen_flag_kudasailx+
hata o sagashiteimftr ka? dozo, tjctf{srjnmasen_flag_kudasainz)
jcvc"m"qcgashiteimftr"ic="fmxm, tjctf{srjnocqgl]dncg_kudasainz)
kbwb#l#pbgashiteimftr#hb<#glyl, tjctf{srjnnbpfm\eobg_kudasainz)
kbwb#l#pbgashiteimbpv#hb<#glyl, tjctf{svnjnbpfm\eobg_kudasaij~-
jcvc"m"qcgashiteim`rt"ic="fmxm, tjctf{stlhocqgl]dncg_kudasaih|/
kbwb#l#pbgashiteimhz|#hb<#glyl, tjctf{s|d`nbpfm\eobg_kudasai`t'
kbwb#l#pbgashiteimjx~#hb<#glyl, tjctf{s~fbnbpfm\eobg_kudasaibv%
l~t~$t he|al}gexotjcz?oz;?dtzp,;pdv~`fqef}mzw~n@bsax[pdntjctfi%
kbwb#l#pbgashiteiml~x#hb<#glyl, tjctf{sx`dnbpfm\eobg_kudasaidp#
jcvc"m"qcgashiteiml~x"ic="fmxm, tjctf{sx`docqgl]dncg_kudasaidp#
jcvc"m"qcgashiteimdvp"ic="fmxm, tjctf{sphlocqgl]dncg_kudasailx+
jcvc"m"qcgashiteimtf`"ic="fmxm, tjctf{s`x|ocqgl]dncg_kudasai|h;
kbwb#l#pbgashiteimtf`#hb<#glyl, tjctf{s`x|nbpfm\eobg_kudasai|h;
kbwb#l#pbgashiteimo}{#hb<#glyl, tjctf{s{cgnbpfm\eobg_kudasaigs
jcvc"m"qcgashiteimo}{"ic="fmxm, tjctf{s{cgocqgl]dncg_kudasaigs
jcvc"m"qcgashiteimewq"ic="fmxm, tjctf{sqimocqgl]dncg_kudasaimy*
jcvc"m"qcgashiteimgus"ic="fmxm, tjctf{sskoocqgl]dncg_kudasaio{(
kbwb#l#pbgashiteimgus#hb<#glyl, tjctf{sskonbpfm\eobg_kudasaio{(
kbwb#l#pbgashiteimewq#hb<#glyl, tjctf{sqimnbpfm\eobg_kudasaimy*
hata o sagashiteimjx~ ka? dozo, tjctf{s~fbmasen_flag_kudasaibv%
hata o sagashiteimo}{ ka? dozo, tjctf{s{cgmasen_flag_kudasaigs
hata o sagashiteimhz| ka? dozo, tjctf{s|d`masen_flag_kudasai`t'
hata o sagashiteimi{} ka? dozo, tjctf{s}eamasen_flag_kudasaiau&
jcvc"m"qcgashiteimi{}"ic="fmxm, tjctf{s}eaocqgl]dncg_kudasaiau&
jcvc"m"qcgashiteimhz|"ic="fmxm, tjctf{s|d`ocqgl]dncg_kudasai`t'
hata o sagashiteiml~x ka? dozo, tjctf{sx`dmasen_flag_kudasaidp#
hata o sagashiteim`rt ka? dozo, tjctf{stlhmasen_flag_kudasaih|/
hata o sagashiteimasu ka? dozo, tjctf{sumimasen_flag_kudasaii}.
```
But I guess this line contains the flag:
`hata o sagashiteimasu ka? dozo, tjctf{sumimasen_flag_kudasaii}.`
Yes, the flag is: `tjctf{sumimasen_flag_kudasaii}`.