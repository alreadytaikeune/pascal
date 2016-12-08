	PUSH	jump3
	GOTO	
fact	EQU	*
a_fact	DS	1
	PUSH	a_fact
	SWAP	
	STORE	
	PUSH	a_fact
	LOAD	
	PUSH	1
	SUB	
	BEZ	true2
	PUSH	0
	PUSH	end2
	GOTO	
true2	EQU	*
	PUSH	1
end2	EQU	*
	BEZ	else2
	PUSH	1
	SWAP	
	GOTO	
	PUSH	finif2
	GOTO	
else2	EQU	*
	PUSH	a_fact
	LOAD	
	PUSH	retfact1
	PUSH	a_fact
	LOAD	
	PUSH	1
	SUB	
	PUSH	fact
	GOTO	
retfact1	EQU	*
	MUL	
	SWAP	
	GOTO	
finif2	EQU	*
	PUSH	a_fact
	LOAD	
	PUSH	1
	SUB	
	GOTO	
jump3	EQU	*
b	DS	1
	PUSH	b
	IN	
	STORE	
;/ print...
	PUSH	retfact4
	PUSH	b
	LOAD	
	PUSH	fact
	GOTO	
retfact4	EQU	*
	OUT
	STOP

