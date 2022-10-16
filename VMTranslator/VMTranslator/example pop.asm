//--pop local 5--
//get addr local 5
@5
D=A // d=5
@1
D=D+M //A=5+baseAddr
//save location to gen reg 
@13
M=D
//get value from stack, accounting for the moved pointer
@0
A=M
D=M
//move back to stored value
@13
A=M
M=D

//clear stack value
@13
A=M
M=0
//clear gen reg value
@13
M=0
