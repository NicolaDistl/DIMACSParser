def translate(formula):
  if beginsWith("And(", formula):
    [left, right] = splitOnComma(formula)
    return translate(left[4:]) and translate(right[:-1])

  elif beginsWith("Or(", formula):
    [left, right] = splitOnComma(formula)
    return translate(left[3:]) or translate(right[:-1])

  elif beginsWith("Not(", formula):
    return not translate(formula[4:])

  elif beginsWith("Impl(", formula):
    [left, right] = splitOnComma(formula)
    return not translate(left[5:]) or translate(right[:-1])

  elif beginsWith("BiImpl(", formula):
    [left, right] = splitOnComma(formula)
    return translate("Impl(" + left[7:] + "," + right[:-1] + ")")  and translate("Impl(" +right[:-1] + "," + left[7:] +")")
  
  elif beginsWith("TOP", formula):
    return True
  
  elif beginsWith("BOT", formula):
    return False

  else:
    return boolean(formula)

def boolean(formula):
  return bool(int(formula[0]))


def splitOnComma(formula):
  counter = 0
  firstBracketEncountered = False
  for i in range(len((formula))):
    
    if formula[i] == "(":
      firstBracketEncountered = True
      counter += 1

    if formula[i] == ")":
      counter -=1

    if counter == 1 and formula[i+1] == ",":
      return [formula[:i+1], formula[i+2:]]


def beginsWith(word, text):
  if len(word) > len(text):
    return False
  
  for i in range(len(word)):
    if text[i] != word[i]:
      return False

  return True