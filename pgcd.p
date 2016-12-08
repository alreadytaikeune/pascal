a=125;
b=1000;
while(a*b > 0){
	if(a > b){
		a = a%b;
	}
	else{
		b = b%a;
	}
}
c=0;
if(a == 0){
	c = b;
}
else{
	c = a;
}
print c;
