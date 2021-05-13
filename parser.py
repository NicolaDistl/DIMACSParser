def eliminateImpl(formula):
  if beginsWith("And(", formula):
    andArray = splitOnComma(formula[3:])

    return "And(" + eliminateImpl(andArray[0]) + "," + eliminateImpl(andArray[1]) + ")"

  elif beginsWith("Or(", formula):

    orArray = splitOnComma(formula[2:])

    return "Or(" + eliminateImpl(orArray[0]) + "," + eliminateImpl(orArray[1]) + ")"

  elif beginsWith("Not(", formula):
    return "Not(" + eliminateImpl(formula[4:-1]) + ")"

  elif beginsWith("Impl(", formula):
    [left, right] = splitOnComma(formula[4:])
    # print("Or(Not("+ (left) + ")," + (right) + ")")
    return "Or(Not("+ eliminateImpl(left) + ")," + eliminateImpl(right) + ")"

  elif beginsWith("BiImpl(", formula):
    [left, right] = splitOnComma(formula[6:])
    # print("And(" + "Impl(" + left + "," + right + ")"  + "," + "Impl(" + right + "," + left +")" + ")")
    return "And(" + eliminateImpl("Impl(" + left + "," + right + ")")  + "," + eliminateImpl("Impl(" + right + "," + left +")") + ")"

  elif beginsWith("TOP", formula):
    return "TOP"
  
  elif beginsWith("BOT", formula):
    return "BOT"
  else:
    return formula

def eliminateNot(formula):
  if beginsWith("And(", formula):
    andArray = splitOnComma(formula[3:])
    

    return "And(" + eliminateNot(andArray[0]) + "," + eliminateNot(andArray[1]) + ")"

  elif beginsWith("Or(", formula):

    orArray = splitOnComma(formula[2:])

    return "Or(" + eliminateNot(orArray[0]) + "," + eliminateNot(orArray[1]) + ")"

  elif beginsWith("Not(", formula):
    changedFormula = changeNotOrAnd(formula[4:-1])
    if ("Not(" + changedFormula + ")" == formula):
      return "Not(" + eliminateNot(formula[4:-1]) + ")"
    return eliminateNot(changedFormula)

  elif beginsWith("TOP", formula):
    return "TOP"
  
  elif beginsWith("BOT", formula):
    return "BOT"
  else:
    return formula

def distributeOrInwards(formula):
  if beginsWith("And(", formula):
    andArray = splitOnComma(formula[3:])
    
    return "And(" + distributeOrInwards(andArray[0]) + "," + distributeOrInwards(andArray[1]) + ")"

  elif beginsWith("Or(", formula):
    changedFormula = changeOrAnd(formula)
    if ("Or(" + changedFormula + ")" == formula):
      print("Alaaaaarm")
      return "Or(" + distributeOrInwards(formula[3:-1])

    return changedFormula

  elif beginsWith("Not(", formula):
    return "Not(" + distributeOrInwards(formula[4:-1]) + ")"

  elif beginsWith("TOP", formula):
    return "TOP"
  
  elif beginsWith("BOT", formula):
    return "BOT"
  else:
    return formula

def boolean(formula):
  return bool(int(formula[0]))

# we know it begins with Or() and want to check if it continues with a,And() to change from
# Or(P,And(Q,R)) to And(Or(P,Q),Or(P,R))
def changeOrAnd(text):
  [pRaw, right] = splitOnComma(text)

  if beginsWith("And(", right):
    # pRaw[2:] weil blöderweise r( immer vorne dran ist
    p = pRaw[2:]
    [qRaw,r] = splitOnComma(right)
    # qRaw[3:] weil blöderweise nd( immer vorne dran ist
    q = qRaw[3:]

    return "And(Or(" + distributeOrInwards(p) + "," + distributeOrInwards(q) + "),Or(" + distributeOrInwards(p) + "," + distributeOrInwards(r) + "))"

  return text

# we know it had a Not and want to change it with theMorgans law if it begins with And() or Or()
def changeNotOrAnd(text):
  if beginsWith("And(", text):
    andArray = splitOnComma(text[3:])
    return "Or(Not(" + eliminateNot(andArray[0]) + "),Not(" + eliminateNot(andArray[1]) + "))"

  elif beginsWith("Or(", text):

    orArray = splitOnComma(text[2:])
    return "And(Not(" + eliminateNot(orArray[0]) + "),Not(" + eliminateNot(orArray[1]) + "))"

  return text

# split a logical statement in two sections if it contains a comma. Needs the brackets to function properly
# eg (a,b)  and Or(Not(Not(a)),And(a,b)) works but a,b not
def splitOnComma(formula):
  counter = 0

  for i in range(len((formula))):
    
    if formula[i] == "(":
      counter += 1

    if formula[i] == ")":
      counter -=1

    if counter == 1 and formula[i+1] == ",":
      return [formula[1:i+1], formula[i+2:-1]]

  return False

def beginsWith(word, text):
  if len(word) > len(text):
    return False
  
  for i in range(len(word)):
    if text[i] != word[i]:
      return False

  return True

def eliminateIAndE(text):
  return eliminateImpl(text)


def convertToCNF(text):
  text = eliminateIAndE(text)
  while True:
    oldText = text
    text = eliminateNot(text)

    if oldText == text:
      break

  while True:
    oldText = text
    text = distributeOrInwards(text)

    if oldText == text:
      break

  return text

# if beginsWith("And(", formula):

#   andArray = splitOnComma(formula)

#   andString = translate(andArray[0])
#   for i in range(1, len(andArray)):
#     andString = andString + "," + translate(andArray[i])
#   return andString

# elif beginsWith("Or(", formula):

#   orArray = splitOnComma(formula)

#   orString = translate(orArray[0])
#   for i in range(1, len(orArray)):
#     orString = orString + "," + translate(orArray[i])

#   return orString



# def splitOnComma(formula):
#   counter = 0
#   numberOfItems = 1
#   firstBracketEncountered = False
#   returnArray = []
#   lastIWhenComma = -1

#   for i in range(len((formula))):
  
#     if formula[i] == "(":
#       firstBracketEncountered = True
#       counter += 1

#     if formula[i] == ")":
#       counter -=1

#     if counter == 1 and formula[i+1] == ",":
#       returnArray.append(formula[lastIWhenComma+1:i+1])
#       lastIWhenComma = i+1
#       numberOfItems += 1

#   returnArray.append(formula[lastIWhenComma+1:])
#   return returnArray