@256
D=A
@SP
M=D
@RETURN_ADDRESS0
D=A
@SP
A=M
M=D
@SP
M=M+1
@1
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=M
@SP
A=M
M=D
@SP
M=M+1
@3
D=M
@SP
A=M
M=D
@SP
M=M+1
@4
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@0
D=D-A
@5
D=D-A
@2
M=D
@SP
D=M
@1
M=D
@Sys.init
0;JMP
(RETURN_ADDRESS0)
(Main.fibonacci)
@2
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@TRUE1
D;JLT
@FALSE1
0;JMP
(TRUE1)
D=-1
@END1
0;JMP
(FALSE1)
D=0
(END1)
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@Main.fibonacci:N_LT_2
D;JNE
@Main.fibonacci:N_GE_2
0;JMP
(Main.fibonacci:N_LT_2)
@2
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@frame
M=D
@frame
D=M
@5
D=D-A
A=D
D=M
@ret
M=D
@SP
M=M-1
A=M
D=M
@2
D=M
@0
D=D+A
@R13
M=D
@SP
A=M
D=M
@R13
A=M
M=D
@2
D=M
@1
D=D+A
@SP
M=D
@frame
D=M
@1
D=D-A
A=D
D=M
@THAT
M=D
@frame
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@frame
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@frame
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
@ret
A=M
0;JMP
(Main.fibonacci:N_GE_2)
@2
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M-D
@SP
M=M+1
@RETURN_ADDRESS1
D=A
@SP
A=M
M=D
@SP
M=M+1
@1
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=M
@SP
A=M
M=D
@SP
M=M+1
@3
D=M
@SP
A=M
M=D
@SP
M=M+1
@4
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@1
D=D-A
@5
D=D-A
@2
M=D
@SP
D=M
@1
M=D
@Main.fibonacci
0;JMP
(RETURN_ADDRESS1)
@2
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M-D
@SP
M=M+1
@RETURN_ADDRESS2
D=A
@SP
A=M
M=D
@SP
M=M+1
@1
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=M
@SP
A=M
M=D
@SP
M=M+1
@3
D=M
@SP
A=M
M=D
@SP
M=M+1
@4
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@1
D=D-A
@5
D=D-A
@2
M=D
@SP
D=M
@1
M=D
@Main.fibonacci
0;JMP
(RETURN_ADDRESS2)
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M+D
@SP
M=M+1
@LCL
D=M
@frame
M=D
@frame
D=M
@5
D=D-A
A=D
D=M
@ret
M=D
@SP
M=M-1
A=M
D=M
@2
D=M
@0
D=D+A
@R13
M=D
@SP
A=M
D=M
@R13
A=M
M=D
@2
D=M
@1
D=D+A
@SP
M=D
@frame
D=M
@1
D=D-A
A=D
D=M
@THAT
M=D
@frame
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@frame
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@frame
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
@ret
A=M
0;JMP
(Sys.init)
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
@RETURN_ADDRESS3
D=A
@SP
A=M
M=D
@SP
M=M+1
@1
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=M
@SP
A=M
M=D
@SP
M=M+1
@3
D=M
@SP
A=M
M=D
@SP
M=M+1
@4
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@1
D=D-A
@5
D=D-A
@2
M=D
@SP
D=M
@1
M=D
@Main.fibonacci
0;JMP
(RETURN_ADDRESS3)
(Sys.init:END)
@Sys.init:END
0;JMP
(END)
@END
0;JMP
