package primitive

#AttVal: [=~"^\\p{Lu}\\p{Ll}+$"]: [...=~"^\\p{Ll}+$"] & [_, ...=~"^\\p{Ll}+$"]

#ListAttVal: [...#AttVal] & [_, ...#AttVal]

#Gloses: [=~"^\\p{Lu}+$"]: #AttVal | #ListAttVal

