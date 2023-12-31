// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen
// by writing 'black' in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen by writing
// 'white' in every pixel;
// the screen should remain fully clear as long as no key is pressed.


@8192
D=A
@pixels
M=D



(INITLOOP)
    @SCREEN
    D=A
    @addr
    M=D
    @i
    M=0 
    @KBD
    D=M
    @BLACKLOOP
    D;JNE
    @WHITELOOP
    D;JEQ
 

(BLACKLOOP)
    @i
    D=M
    @pixels
    D=D-M 
    @END
    D;JEQ

    @addr
    A=M
    M=-1

    @i
    M=M+1
    @addr
    M=M+1
    @BLACKLOOP
    0;JMP

(WHITELOOP)
    @i
    D=M
    @pixels
    D=D-M 
    @END
    D;JEQ

    @addr
    A=M
    M=0

    @i
    M=M+1
    @addr
    M=M+1
    @WHITELOOP
    0;JMP

(END)
    @INITLOOP
    0;JMP 