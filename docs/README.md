# flang
A simple flow chart programming language
"F" is for flow chart.
"F" is for functional.
"lang" is for programming language.

# Tutorial
Flang is a functional language, which means it's made of functions. Functions take input(s) and give output(s). Some people call these arguments and return values, respectively. The outputs of functions are sent to inputs of others along arrows. Arrows look like this:
###### picture
Aren't they cute? The computer loves to pick and choose among its babies, so it sends outputs to inputs along arrows in any order it wants, as long as the function is ready with the outputs.
Arrows are NOT functions.
Functions are drawn as something inside a polygon or a lemon shape instead of a 2-gon.
###### picture (examples)
### Start
It is not a function.
It looks like a "9" with an arrow going out the bottom.
###### picture
It is where the flow of the program starts. The flow is the places where the computer is reading the program at the moment. You can think of it as a function that will start the program, give a 0, but take nothing. 
By itself, it is a complete program. If you run it, the program will do nothing.
The smallest program has the same effect and is composed of nothing, nothing, and more nothing.
### Print
Assume every heading is for a function.
It takes a value, prints it to the console (terminal), and gives it back.
Here is a program that will, again do nothing:
###### picture start --> print
### Constant
A constant is a box with a value in it.
###### picture
When a constant takes an input, it gives its value as output.
#### First Program
Now, we have enough knowledge to make "Hello world!" programs.
One looks like this: 
###### picture using a start, then 11 constant/print pairs
You could try this:
###### picture using 11 start/constant/print triplets
but the letters would be out of order.
### Keyboard
When a keyboard takes an input, it gives a value from the console (terminal) as output.
###### picture
#### Second Program
Take five characters, printing each.
###### picture
### Equality
Equality takes three inputs, one on the top left, one on the top middle and the last on the top right.
It gives two outputs, one on the bottom left, and the other on the bottom right.
Once it takes all inputs, if the outermost are equal, it will output the middle input on the bottom left; if they are not equal, it will output the middle input on the bottom left.
###### picture
#### Third Program
If z is inputted, say ":)"
Otherwise, say ":("
###### picture
### Sum
It gives the sum of its two inputs as an output.
###### picture
#### Fourth Program
Output the sum of two and three.
###### picture
### Difference
It gives left input - right input as an output.
###### picture
### Multiplication and Division carry the pattern.
### Greater than (>)
It gives the middle input if left input > right input on the left output.
Otherwise, it gives the middle input on the right output.
###### picture
#### Fifth Program
Determine if the input is greater than f.
###### picture
### Less than (\<)
It gives the middle input if left input < right input on the left output.
Otherwise, it gives the middle input on the right output.
###### picture
### Function
You can create custom functions in flang. They need to have their own name, number of inputs and outputs, and logic.
They look like this.
###### picture
#### Sixth Program
Print the letter "q" sixteen times.
###### picture
### Bus
Busses are not functions.
They are a group of arrows, all going in the same direction.
They walk side-by-side, going at the same pace.
They are usually much neater than having an arbitrary number of arrows.
### Push
Push has two inputs; the left takes a bus and the right takes a value (arrow).
It has one output: the group on the left with the arrow on the right attatched to the right side.
###### picture
###### example
###### example
### Pop
Pop takes a bus.
It gives that bus without its rightmost member on the left output, and that rightmost member on the right output.
###### picture
###### example
### Rotate Left
The leftmost member will walk over to become the rightmost member.
###### picture
To get the leftmost member of a bus, rotate left then pop.
### Rotate Right
The rightmost member will walk over to become the leftmost member.
###### picture
### Length
It will output the number of arrows in the inputted bus.
###### picture
## Language Features
### You can include C libraries.
### Typelessness
An "a" is the same as a 97.
If you want to get a number in its text form, add it to the character for 0 ('0')
For the converse, subtract.
### Busses
If you want to have many characters in a bus from constants, you can use double quotes, and the constant will output a bus of the characters in the quotes.
###### picture
If you want a bus of numbers, separate them by commas.
### Nothing is tacked down.
Normies will flip out since there aren't variables, much less types or objects.
### Easy to visualize.
