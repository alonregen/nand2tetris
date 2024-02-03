from pathlib import Path
import os
import sys
import CompilationEngine as Ce
import JackTokenizer as Jt

if __name__ == '__main__':
    source = "/Users/alonregen/Desktop/code/nand2tetris/projects/10/ArrayTest/Main.jack"
    path = Path(source)

    if path.is_dir():
        for filename in os.listdir(source):
            name, ext = os.path.splitext(filename)
            if ext == '.jack':
                outfile = source + '/' + name + '.xml'
                tokenizer = Jt.JackTokenizer(source + '/' + filename)
                Ce.CompilationEngine(tokenizer, outfile)
    else:
        outfile = source.replace('.jack', '.xml')
        tokenizer = Jt.JackTokenizer(source)
        Ce.CompilationEngine(tokenizer, outfile)
