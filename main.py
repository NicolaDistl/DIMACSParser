from parser import convertToCNF

if __name__ == "__main__":
  #print((eliminateImpl("BiImpl(And(And(Not(Or(0,0)),1),1),1)")))
  #print(translate(eliminateImpl("BiImpl(And(1,Not(0)),Or(1,0))")))
  #print(eliminateImpl("BiImpl(1,1)"))
  #print(eliminateImpl("And(0,1,1,1,1,1,1)"))

  print(convertToCNF("BiImpl(Not(a),And(a,b))"))