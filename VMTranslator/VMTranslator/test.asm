//--push constant 10--
//get constant 10
@10
D=A
//push to stack
@0
A=M
M=D

//incr stack pointer
@0
M=M+1

//decr stack pointer
@0
M=M-1

//--pop temp 0--
//get addr temp 0
@5
D=A
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
@0
A=M
M=0
//clear gen reg value
@13
M=0
