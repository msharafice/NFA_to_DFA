temp = 0
userstring = '' 
initial_state = '' 
initial = []
temp1 = []
input_symbols = set()
with open('input.txt', 'r') as file:
    file_content = file.read()


lines = file_content.split('\n')
general = []

for line in lines:
    if line == '':
        pass
    elif line == '#NFA':
        pass
    else:
        general.append(line)
while temp<3:
    x = general.pop()
    if "final_state" in x:
        temp1 = x.split('=')
        local = 'q' + temp1[1].strip('[]')
        initial.append(local)
    elif "initial_state" in x:
        temp1 = x.split('=')
        initial_state = 'q' + temp1[1]  
    elif "user_input_string" in x:
        temp1 = x.split('=')
        userstring = temp1[1].strip('""')          
    temp += 1    


input_list = general


states_with_transitions = set()


transitions = {}


for item in input_list:

    key, value = item.split('=')
    index, symbol = key.strip('()').split(',')
    if symbol == 'lambda':
        pass
    else:
        input_symbols.add(symbol)


    index_str = 'q' + index
    value_str = 'q' + value
    

    states_with_transitions.add(index_str)
    states_with_transitions.add(value_str)


    if index_str not in transitions:
        transitions[index_str] = {}

    
    if symbol not in transitions[index_str]:
        transitions[index_str][symbol] = set()


    transitions[index_str][symbol].add(value_str)


for state in range(int(max(index for index, _ in (item.strip('()').split(',') for item in input_list)))+1):
    state_str = 'q' + str(state)
    if state_str not in states_with_transitions:
        transitions[state_str] = {}

for states in states_with_transitions:
    if states not in transitions:
        transitions[states] = {}

states = states_with_transitions
final_states = set(initial)



states_dfa = set()
initial_state_dfa = '' 
transitions_dfa = {} 
final_states_dfa = set() 
def LambdaChecker(): 
    LambdaList = [] 
    for states_, input_symbols_ in transitions.items(): 
        if 'lambda' in input_symbols_: 
            LambdaList.append(states_) 
    return LambdaList 
def FirstState(): 
    Temp = [] 
    Final = [] 
    Temp.append(initial_state) 
    Final.append(initial_state) 
    LambdaList = LambdaChecker() 
    while Temp: 
        current_state = Temp.pop(0) 
        if current_state in LambdaList: 
            for next_state in transitions[current_state]['lambda']: 
                if next_state not in Final: 
                    Final.append(next_state) 
    return Final 
 

def StateNameConvertion(Input): 
    Temp = "" 
    for x in Input: 
        Temp += x + ","    
    return(Temp[:-1]) 
 
 
def sort_lists_in_dict(wholeldic): 
    sorted_lists = [(key, sorted(wholeldic[key])) for key in sorted(wholeldic.keys())] 
    return tuple(sorted_lists) 
 
def transitions_finder(states): 
    wholedic = {} 
    for symbol_ in input_symbols: 
        wholedic[symbol_] = [] 
 
    for state_ in states: 
        for symbol__ in input_symbols: 
            try: 
                for State in transitions[state_][symbol__]: 
                    wholedic[symbol__].append(State) 
            except KeyError: 
                pass 
 
    sorted_lists = sort_lists_in_dict(wholedic) 
    return sorted_lists 
 
 
def Convert(State): 
    global transitions_dfa 
    transitions_dfa[StateNameConvertion(State)] = {} 
    result = transitions_finder(State) 
    for x in result: 
        if x[1] != []: 
            transitions_dfa[StateNameConvertion(State)][x[0]] = StateNameConvertion(x[1]) 
            if StateNameConvertion(x[1]) not in transitions_dfa: 
                Convert(x[1]) 
 
def nfatodfa(): 
    global transitions_dfa, states_dfa, initial_state_dfa 
     
    first_state = FirstState() 
    Convert(first_state) 
    for x in transitions_dfa: 
        states_dfa.add(x) 
     
    for x in states_dfa: 
        for y in final_states: 
            if y in x: 
                final_states_dfa.add(x) 
     
    initial_state_dfa = StateNameConvertion(first_state) 
 
    print("states:", states_dfa) 
    print("initial state:", initial_state_dfa) 
    print("transitions:", transitions_dfa) 
    print("final states:", final_states_dfa) 

nfatodfa()

def String_Checker(InputSTR): 
    State = initial_state_dfa 
    for x in InputSTR: 
        try: 
            State = transitions_dfa[State][x] 
        except KeyError: 
            return "Rejected" 
    for fs in final_states_dfa: 
        if fs in State: 
            return "Accepted" 
    return "Rejected" 
 
print("reshte karbar:", String_Checker(userstring)) 
 
states_dfa.add("∅") 
 
transitions_dfa['∅'] = {} 
for symbol in input_symbols: 
   transitions_dfa['∅'][symbol] = '∅' 
 
for state, transitions in transitions_dfa.items(): 
    for symbols in input_symbols: 
        if symbols not in transitions: 
            transitions_dfa[state][symbols] = '∅' 


with open('output.txt', 'w' ,encoding='utf-8') as f:
    f.write("#DFA\n")
    f.write(f"{transitions_dfa}\n")
    f.write(f"initial_state={initial_state_dfa}\n")
    f.write(f'final_state=[{final_states_dfa}]\n')
    f.write(f'python >> "Input string is {String_Checker(userstring)}"')

# The input file has data like the example below


# #NFA
# (0,lambda)=4
# (0,a)=1
# (0,a)=3
# (1,b)=1
# (1,b)=2
# (2,a)=0
# (3,a)=2

# final_state=[4]

# initial_state=0

# user_input_string="aaaabbbbba"