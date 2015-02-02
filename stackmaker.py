import sys,re,string

# settings:
prefix="var"
returnName="retval"
stackName="__STACK"
stackPointerName="__SP"
# end of settings

def numToStr(num):
	if num==0:
		return ""
	if num>0:
		return "+"+str(num)
	return str(num)

def translate(strng,dic,minus):
	ls=re.split("("+prefix+"[a-zA-Z_0-9]+)",strng)
	out=[]
	for id in ls:
		if re.match("("+prefix+"[a-zA-Z_0-9]+)",id):
			id=id.lower()
			out.append(stackName+"["+stackPointerName+\
				numToStr(dic[id]-minus)+"]")
		else:
			out.append(id)
	return string.join(out,"")


lines=sys.stdin.readlines()

returnVariable=""

for i in lines:
	m=re.match("^//@return ("+prefix+"([a-zA-Z_0-9]+))$",i.lower())
	if m:
		returnVariable=m.groups()[0].lower()

identifiers={}
if returnVariable:
	identifiers[returnVariable]=0

for i in lines:
	m=re.findall("("+prefix+"[a-zA-Z_0-9]+)",i)
	for id in m:
		id=id.lower()
		if not identifiers.has_key(id):
			identifiers[id]=len(identifiers)


out=[]

for i in lines:
	m=re.match("declare parameter ("+prefix+"[a-zA-Z_0-9]+).",i.lower())
	if m:
		id=m.groups()[0].lower()
		out.append(i)
		out.append("SET "+stackName+"["+stackPointerName+
			"+"+str(identifiers[id])+"] TO "+id+".\n")
		continue
	m=re.match("run ",i.lower())
	if m:
		out.append("SET "+stackPointerName+" TO "+
			stackPointerName+"+"+str(len(identifiers))+".\n")
		out.append(translate(i,identifiers,len(identifiers)))
		out.append("SET "+returnName+" TO "+stackName+"["+
			stackPointerName+"].\n")
		out.append("SET "+stackPointerName+" TO "+
			stackPointerName+"-"+str(len(identifiers))+".\n")
		continue
	out.append(translate(i,identifiers,0))
		
for i in out:
	print i,
