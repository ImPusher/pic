import itertools
import graphviz
import os
import shutil

k = 2
to_print = False

def sort_tuple(tup):
    return (tup[0], tup[1]) if tup[0] < tup[1] else (tup[1],tup[0])

def nextflag(flag): # flag = [0,flag]
    n = len(flag)
    if flag[-1] == n-2:
        return -1
    j = 1
    for i in range(n-1, 1, -1):
        if flag[i-1] != flag[i] - 1:
            j = i
            break
    flag[j] -= 1
    for i in range(j+1, n):
        flag[i] = k*i - 1
    return flag

def nextdfa(last, flag):
    j = 0
    l = 1
    n = len(flag)
    if last != -1:
        i = n - 1
        s = last
        for j in range(k*n-1, -1, -1):
            if i != 0 and flag[i] == j:
                i -= 1
            elif s[j] < i:
                break
        if j == 0 and (flag[1] == 1 or s[0] == 1):
            return -1
        else:
            s[j] += 1
            j += 1
            l = i+1
    else:
        s = [0 for i in range(k*n)]
        for i in range(len(flag)):
            s[flag[i]] = i
    for i in range(j,k*n):
        if l < n and i == flag[l]:
            l += 1
        else:
            s[i] = 0
    return s

class dfa:
    def __init__(self, flag, delta, n = 2, strings = [], f = [], not_f = []):
        self.n = n
        if flag == 0:
            self.flag = [0] + [i*k-1 for i in range(1,self.n)]
        else:
            self.flag = flag.copy()
        if delta == 0:
            self.delta = nextdfa(-1, self.flag)
        else:
            self.delta = delta.copy()
        self.strings = strings.copy()
        self.f = f.copy()
        self.not_f = not_f.copy()
        self.count = 1
        self.count_final = 1
        self.start()
    
    def start(self):
        if os.path.exists("./current_session"):
            shutil.rmtree("./current_session", ignore_errors=True)
        os.mkdir("./current_session")
        file = open("./current_session/strings.txt", 'w')
        file.close()    
        self.draw_dfa()
    
    def draw_dfa(self):
        graph = graphviz.Digraph()
        graph.attr(rankdir='LR')
        graph.attr(splines='true')
        graph.node(" ", style="invisible",width="0", height="0")
        for i in range(self.n):
            if i in self.f:
                graph.node(str(i), shape="doublecircle")
            else:
                graph.node(str(i), shape="circle")
        graph.edge(' ', '0', dir="both", arrowtail="dot")
        for i in range(len(self.delta)):
            graph.edge(str(int(i/2)), str(self.delta[i]), label=str(i%2), dir="forward")
        graph.render("./current_session/out" + str(self.count_final-1), format='png')
        os.remove("./current_session/out" + str(self.count_final-1))
        
    def show_dfa(self):
        print()
        print("showing dfa")
        print("flag: ", self.flag)
        print("delta: ", self.delta)
        print("f: ", self.f)
        print("not_f: ", self.not_f)
        print("strings: ", self.strings, "\n")
        
    def get_strings(self):
        return self.strings
    
    def verify_last_string(self):
        (target, string) = self.strings[-1]
        current_state = 0
        for i in range(len(string)):
            current_state = self.delta[k*current_state + int(string[i])]
            
        return (current_state in self.f) == target
    
    def get_final_state_by_index(self, string_index):
        string = self.strings[string_index][1]
        current_state = 0
        for i in range(len(string)):
            
            current_state = self.delta[k*current_state + int(string[i])]
        
        return current_state
    
    def get_final_state_by_string(self, string):
        current_state = 0
        for i in range(len(string)):
            current_state = self.delta[k*current_state + int(string[i])]
        return current_state
        
    def update_dfa(self):
        if to_print:
            print("updating dfa")
        while True:
            while self.flag != -1:
                if to_print:
                    print("flag: ", self.flag)
                self.delta = nextdfa(self.delta, self.flag)
                while self.delta != -1:
                    if to_print:
                        print("delta: ",self.delta)
                    self.count += 1
                    if self.count%10000 == 0:
                        print("\r" + str(self.count) + " dfas processed", end="", flush=True)
                    if self.update_final_states() and self.is_minimal():
                        self.count_final += 1
                        if to_print:
                            print("end of update")
                            self.show_dfa()
                        self.draw_dfa()
                        print("\r" + str(self.count) + " dfas processed", end="", flush=True)
                        return
                    self.delta = nextdfa(self.delta, self.flag)

                self.flag = nextflag(self.flag)
            
            self.n += 1
            self.flag = [0] + [i*k-1 for i in range(1,self.n)]
            self.delta = nextdfa(-1, self.flag)
        
        
    def update_final_states(self):
        self.f = []
        self.not_f = []
        for x in self.strings:
            if x[0]:
                self.add_final_state(self.get_final_state_by_string(x[1]))
        self.f = list(set(tuple(self.f)))
        
        for x in self.strings:
            if x[0] == 0:
                state = self.get_final_state_by_string(x[1])
                if state in self.f:
                    return False
                self.add_not_final_state(state)
                
        self.not_f = list(set(tuple(self.not_f)))
        return True
    
    def is_minimal(self):
        marked = {}
        for x in itertools.combinations(range(self.n), 2):
            marked[x] = [0]
        
        not_f = [x for x in range(self.n) if x not in self.f]
        for x in itertools.product(self.f, not_f):
            marked[sort_tuple(x)] = [1]
        found = False
        for x in list(itertools.combinations(self.f, 2)) + list(itertools.combinations(not_f, 2)):
            for i in range(k):
                next_pair = [self.delta[k*x[0]+i], self.delta[k*x[1]+i]]
                next_pair.sort()
                next_pair = tuple(next_pair)
                if next_pair not in marked or marked[next_pair][0] == 0:
                    continue
                    
                found = True
                to_mark = [x]
                while len(to_mark) != 0:
                    if to_mark[0] in marked:
                        target = marked[to_mark[0]]
                        target[0] = 1
                        for x in target[1:]:
                            if marked[x][0] == 0:
                                to_mark += [x]
                    to_mark = to_mark[1:]
            if not found:
                for i in range(k):
                    next_pair = [self.delta[k*x[0]+i], self.delta[k*x[1]+i]]
                    next_pair.sort()
                    next_pair = tuple(next_pair)
                    if next_pair[0] != next_pair[1]:
                        marked[next_pair] += [x]
            found = False
        for x in marked.values():
            if x[0] == 0:
                return False
        return True
    
    def add_final_state(self, state):
        if state < self.n:
            self.f += [state]
            
    def add_not_final_state(self, state):
        if state < self.n:
            self.not_f += [state]
            
    def add_accepted_string(self, state):
        if state in self.f:
            return
        elif state not in self.not_f:
            self.add_final_state(state)
            if self.is_minimal():
                self.count += 1
                self.count_final += 1
                self.draw_dfa()
                return
        self.update_dfa()
        
    def add_rejected_string(self, state):
        if state in self.not_f:
            return
        elif state not in self.f:
            self.add_not_final_state(state)
            return
        self.update_dfa()
    
    def known_string(self, string):
        if (0, string) in self.strings or (1, string) in self.strings:
            return True
        return False
    
    def add_string(self, is_in, string):
        if to_print:
            print("adding: ", is_in, string, "\n")
        
        self.strings += [(is_in, string)]
        file = open("./current_session/strings.txt", 'a')
        if string == "":
            file.write(str(is_in) + " " + "eps" + "\n")
        else:
            file.write(str(is_in) + " " + string + "\n")
        file.close()
        
        string_final_state = self.get_final_state_by_index(-1)
        
        if is_in:
            self.add_accepted_string(string_final_state)
        else:
            self.add_rejected_string(string_final_state)
