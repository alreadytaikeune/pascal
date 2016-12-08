#!/usr/bin/env python
#
# $Id: mach.py 484 2014-10-04 09:05:45Z coelho $
#
# python version of a little stack machine

from __future__ import print_function;

import sys,re

# hmmm... I could have done a nice class, sorry:-)
# raw machine data
pc = 0
program = []
data = []
stack = []

def err(msg):
    # status on error
    print('program length %d, pc=%d' % (len(program), pc), file=sys.stderr)
    print('stack length %d' % len(stack), file=sys.stderr)
    print('data length %d' % len(data), file=sys.stderr)
    # message & exit
    sys.stderr.write(msg + '\n')
    sys.exit(1)

# all available instructions
ONEARG='BGZ|BEZ|PUSH'
NOARG='LOAD|STORE|SWAP|ADD|SUB|MUL|DIV|AND|OR|NOT|STOP|GOTO|IN|OUT'

onearg = re.compile('^(' + ONEARG + ')$')
noarg = re.compile('^(' + NOARG + ')$')
integer = re.compile('^-?\d+$')
split = re.compile('[ \n\t\r]+')
empty = re.compile('^[ \t\r]+\n$')

# build instruction translation
i2n = {}
n2i = []
ni = 0
for ins in re.split('\|', ONEARG + '|' + NOARG):
    i2n[ins] = ni
    n2i.append(ins)
    ni+=1

# get and check code
nline=0
for line in open(sys.argv[1],'r').readlines():
    nline+=1
    if empty.match(line):
        continue
    cmds = split.split(line.upper().lstrip(' \t').rstrip(' \n\t\r'))
    # check command & argument
    if len(cmds)==0 or (len(cmds)==1 and cmds[0]==''):
        continue
    elif onearg.match(cmds[0]):
        assert len(cmds)==2
        if not integer.match(cmds[1]):
            err('expecting integer, got %s on line %d' % (cmds[1],nline))
    elif noarg.match(cmds[0]):
        assert len(cmds)==1
    else: err('unexpected command %s on line %d' % (cmds[0],nline))
    # store program
    program.append(i2n[cmds[0]])
    if len(cmds)==2:
        program.append(int(cmds[1]))

# run machine
while True:
    # sandboxing:-)
    if pc>=len(program) or pc<0:
        err('pc is out of program: %d' % pc)
    cur=n2i[program[pc]]
    pc+=1
    # slow but quite readable handling of instructions
    if cur=='STOP':
        print('program length %d, pc=%d' % (len(program), pc))
        print('stack length %d' % len(stack))
        print('data length %d' % len(data))
        sys.exit(0)
    # stack management
    elif cur=='PUSH':
        stack.append(program[pc])
        pc+=1
    elif cur=='SWAP':
        stack[-2], stack[-1] = stack[-1], stack[-2]
    # memory management...
    elif cur=='STORE':
        val, adr = stack.pop(), stack.pop()
        if adr < 0 or adr > 1000000:
            err('unexpected STORE data address: %d', adr)
        if adr >= len(data):
            # expand memory if necessary
            data += [0] * (adr-len(data)+1)
        assert adr < len(data)
        data[adr] = val
    elif cur=='LOAD':
        adr = stack.pop()
        if adr < 0 or adr > 1000000:
            err('unexpected LOAD data address: %d', adr)
        if adr < len(data):
            stack.append(data[adr])
        else:
            # set zero if out of bound...
            sys.stderr.write('out of bounds memory load: data[%d]\n' % adr)
            stack.append(0)
    # ALU
    elif cur=='ADD':
        stack.append(stack.pop()+stack.pop())
    elif cur=='MUL':
        stack.append(stack.pop()*stack.pop())
    elif cur=='AND':
        stack.append(stack.pop()&stack.pop())
    elif cur=='OR':
        stack.append(stack.pop()|stack.pop())
    elif cur=='SUB':
        i,j = stack.pop(),stack.pop()
        stack.append(j-i)
    elif cur=='DIV':
        i,j = stack.pop(),stack.pop()
        stack.append(j/i)
    elif cur=='NOT':
        # binary inversion, not logical!
        stack.append(~stack.pop())
    # input-output
    elif cur=='OUT':
        print('output: %d' % stack.pop())
    elif cur=='IN':
        sys.stdout.write('input: ')
        stack.append(int(sys.stdin.readline()))
    # branches
    elif cur=='GOTO':
        pc = stack.pop()
    elif cur=='BGZ':
        if stack.pop()>0: pc = program[pc]
        else: pc+=1
    elif cur=='BEZ':
        if stack.pop()==0: pc = program[pc]
        else: pc+=1
    else:
        err('unexpected instruction: ' + cur)
