# Bias assessment report

Dataset: Marketing Research.sav (1400 respondents, 50 columns)

## 1. Representation in the dataset

GENDER:
           n   pct
GENDER            
Male    1124  80.3
Female   276  19.7

Age band (detail):
                     n   pct
Age band (detail)           
35-44              518  37.0
25-34              517  36.9
45-54              210  15.0
Under 25           120   8.6
55-64               32   2.3
65+                  3   0.2
  -> groups with fewer than 30 respondents (too small for reliable conclusions): 65+

INCOME:
                      n   pct
INCOME                       
$80,000 - $95,000   301  21.5
Over $110,000       291  20.8
$95,000 - $110,000  218  15.6
$65,000 - $80,000   194  13.9
$35,000 - $50,000   150  10.7
Under $35,000       131   9.4
$50,000 - $65,000   115   8.2

EDUCATE:
                         n   pct
EDUCATE                         
Some college           328  23.4
Undergraduate degree   295  21.1
Graduate degree        235  16.8
High school            229  16.4
Other                  163  11.6
Less than high school  150  10.7

RACE:
                   n   pct
RACE                      
Caucasian        959  68.5
Black            217  15.5
Asian            127   9.1
Hispanic          87   6.2
Other              8   0.6
American Indian    2   0.1
  -> groups with fewer than 30 respondents (too small for reliable conclusions): Other, American Indian

MARITAL:
             n   pct
MARITAL             
Married    581  41.5
Single     558  39.9
Divorced   208  14.9
Separated   45   3.2
Widowed      8   0.6
  -> groups with fewer than 30 respondents (too small for reliable conclusions): Widowed

Columns with the most missing answers (% of respondents):
HOWMUCH     80.6
BETTER      79.5
CHILDREN    39.9
WORTH        7.4
RESEARCH     0.0
SAFEWEB      0.0

Not in the dataset: region or country, industry, and competitor data.
Findings apply to this survey's car-buying context only (coverage gap).

## 2. Differences in answers between groups

By GENDER (agree / Yes %, with 95% margin of error):
  EASYUSE ['The web site was easy to use.']: Female 64% (n=276, +/-6), Male 65% (n=1124, +/-3) -> gap 0 pts, within sampling noise
  SAFEWEB ['I think purchasing items from the Internet is safe']: Female 15% (n=276, +/-4), Male 38% (n=1124, +/-3) -> gap 23 pts, possible real difference
  HELPFUL ['I found the web site was very helpful in my purcha']: Female 49% (n=276, +/-6), Male 51% (n=1124, +/-3) -> gap 2 pts, within sampling noise
  LIKENET ['I like using the Internet.']: Female 18% (n=276, +/-5), Male 37% (n=1124, +/-3) -> gap 19 pts, possible real difference
  SENGINE ['Found out about Auto Online from a search engine']: Female 67% (n=276, +/-6), Male 66% (n=1124, +/-3) -> gap 1 pts, within sampling noise
  TV ['Found out about Auto Online from television']: Female 31% (n=276, +/-5), Male 33% (n=1124, +/-3) -> gap 2 pts, within sampling noise
  NWSPAPER ['Found out about Auto Online from a newspaper']: Female 6% (n=276, +/-3), Male 5% (n=1124, +/-1) -> gap 1 pts, within sampling noise

By Age group (agree / Yes %, with 95% margin of error):
  EASYUSE ['The web site was easy to use.']: Under 30 62% (n=363, +/-5), 30-44 66% (n=792, +/-3), 45+ 65% (n=245, +/-6) -> gap 4 pts, within sampling noise
  SAFEWEB ['I think purchasing items from the Internet is safe']: Under 30 41% (n=363, +/-5), 30-44 37% (n=792, +/-3), 45+ 12% (n=245, +/-4) -> gap 29 pts, possible real difference
  HELPFUL ['I found the web site was very helpful in my purcha']: Under 30 50% (n=363, +/-5), 30-44 52% (n=792, +/-3), 45+ 49% (n=245, +/-6) -> gap 2 pts, within sampling noise
  LIKENET ['I like using the Internet.']: Under 30 41% (n=363, +/-5), 30-44 34% (n=792, +/-3), 45+ 16% (n=245, +/-5) -> gap 24 pts, possible real difference
  SENGINE ['Found out about Auto Online from a search engine']: Under 30 64% (n=363, +/-5), 30-44 67% (n=792, +/-3), 45+ 66% (n=245, +/-6) -> gap 3 pts, within sampling noise
  TV ['Found out about Auto Online from television']: Under 30 33% (n=363, +/-5), 30-44 32% (n=792, +/-3), 45+ 32% (n=245, +/-6) -> gap 1 pts, within sampling noise
  NWSPAPER ['Found out about Auto Online from a newspaper']: Under 30 6% (n=363, +/-2), 30-44 5% (n=792, +/-2), 45+ 4% (n=245, +/-2) -> gap 2 pts, within sampling noise

By Income tier (agree / Yes %, with 95% margin of error):
  EASYUSE ['The web site was easy to use.']: higher-income 61% (n=509, +/-4), lower-income 68% (n=281, +/-5), middle-income 66% (n=610, +/-4) -> gap 8 pts, within sampling noise
  SAFEWEB ['I think purchasing items from the Internet is safe']: higher-income 34% (n=509, +/-4), lower-income 21% (n=281, +/-5), middle-income 39% (n=610, +/-4) -> gap 19 pts, possible real difference
  HELPFUL ['I found the web site was very helpful in my purcha']: higher-income 52% (n=509, +/-4), lower-income 47% (n=281, +/-6), middle-income 51% (n=610, +/-4) -> gap 5 pts, within sampling noise
  LIKENET ['I like using the Internet.']: higher-income 35% (n=509, +/-4), lower-income 21% (n=281, +/-5), middle-income 37% (n=610, +/-4) -> gap 16 pts, possible real difference
  SENGINE ['Found out about Auto Online from a search engine']: higher-income 66% (n=509, +/-4), lower-income 64% (n=281, +/-6), middle-income 67% (n=610, +/-4) -> gap 3 pts, within sampling noise
  TV ['Found out about Auto Online from television']: higher-income 31% (n=509, +/-4), lower-income 34% (n=281, +/-6), middle-income 32% (n=610, +/-4) -> gap 3 pts, within sampling noise
  NWSPAPER ['Found out about Auto Online from a newspaper']: higher-income 4% (n=509, +/-2), lower-income 9% (n=281, +/-3), middle-income 5% (n=610, +/-2) -> gap 4 pts, within sampling noise


## 3. Prompt audit (training_data.jsonl)

Examples audited: 6
- Prompts that target a demographic segment: 1/6
- Examples mentioning race: 0/6 (race is excluded from prompt generation by design)
- Examples with judgmental wording about a group: 0/6
- Demographic prompts whose response makes a comparison/generalization: 1/6
- Responses with no figures (unsupported claims): 6/6
- Mention a region: 0/6; mention an industry: 0/6

Flagged for manual review:
  * Prompt: Segment respondents by AGE and INCOME and describe how their attitudes toward onli...  [age, income]