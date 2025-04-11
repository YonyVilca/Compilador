initialize stack = <S $> and next
repeat
    case stack of 
     <X, rest> : if T[X,*next] = Y1...Yn
                then stack <- <Y1...Yn rest>;
                else error();
     <t, rest> : if t == *next ++
                then stack <- <rest>;
                else error();
until stack == <>;



PREDICTIVE PARSING: Parsing table method similar to recursive descent, except

for the leftmost non-terminal S
We look at the next input token a
And choose the production shown at [S,a]

A stack records frontier of parse tree 
Non-terminals that have yet to be expanded
terminals that have yet to be expanded
Top of stack = leftmost pending terminal or non-terminal

Reject on raching error state
Accept on end input & empty stack