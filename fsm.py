# -*- coding: utf-8 -*-
"""
@author: hittun
@time: 2021/04/06
@desc: 有限状态机

事件触发状态转换
"""

class CState(object):
    m_Name = None
    
    def __init__(self):
        pass
    
    def Start(self):
        pass
    
    def End(self):
        pass
    
    def Run(self):
        pass
    
    def GetStateName(self):
        if self.m_Name is None:
            return self.__class__
        return self.m_Name

class CModel(object):
    def __init__(self):
        self.m_InitialState = None
        self.m_State = None
    
    def SetInitialState(self, initial_state):
        self.m_InitialState = initial_state
        if self.m_State is None:
            self.SetState(initial_state)
    
    def GetInitialState(self):
        return self.m_InitialState

    def SetState(self, state):
        if isinstance(self.m_State, state):
            return
        # release old state
        if self.m_State:
            self.m_State.End()
        # create new state
        self.m_State = state()
        self.m_State.Start()
        self.m_State.Run()
    
    def GetStateObj(self):
        obj = self.m_State
        if not obj:
            raise Exception("Exception can not find model state obj")
        return obj
    
    def GetState(self):
        obj = self.GetStateObj()
        return obj.__class__

class CFiniteStateMachine(object):
    """
    This is a Finite State Machine (FSM)
    """
    def __init__(self, model, transitions, initial_state):
        self.m_ModelWeakref = None
        self.m_TransitionTable = {}
        self.SetModel(model)
        self.AddTransitions(transitions)
        self.SetModelInitialState(initial_state)
    
    def SetModel(self, model):
        import weakref
        self.m_ModelWeakref = weakref.ref(model)
    
    def GetModel(self):
        pModel = None
        if self.m_ModelWeakref:
            pModel = self.m_ModelWeakref()
        if not pModel:
            raise Exception("Exception can not find fsm model")
        else:
            return pModel
    
    def SetModelInitialState(self, initial_state):
        self.GetModel().SetInitialState(initial_state)
    
    def AddTransition(self, input_event, source_state, dest_state):
        if not self.m_TransitionTable.has_key(source_state):
            self.m_TransitionTable[source_state] = {}
        if self.m_TransitionTable[source_state].has_key(input_event):
            raise Exception("Exception exist transition(from %s to %s by %s) conflict add transition: from %s to %s by %s" % (source_state, self.m_TransitionTable[source_state][input_event], input_event, source_state, dest_state, input_event))
        self.m_TransitionTable[source_state][input_event] = dest_state
        
    def AddTransitions(self, transitions):
        # transitions = [
        #   {'event': '保存', 'source': '未保存', 'dest': '已保存' },
        #   {'event': '提交', 'source': '已保存', 'dest': '已提交' },
        #   {'event': '审核', 'source': '已提交', 'dest': '已审核' },
        # ]
        for transition in transitions:
            input_event = transition['event']
            source_state = transition['source']
            dest_state = transition['dest']
            self.AddTransition(input_event, source_state, dest_state)
    
    def Process(self, input_event):
        pModel = self.GetModel()
        current_state = pModel.GetState()
        dest_state = self.GetDestState(current_state, input_event)
        pModel.SetState(dest_state)
    
    def Reset(self):
        pModel = self.GetModel()
        initial_state = pModel.GetInitialState()
        pModel.SetState(initial_state)
    
    def GetDestState(self, source_state, input_event):
        return self.m_TransitionTable[source_state][input_event]















# --------------------------------------------------------------------------- 
# --------------------------------------------------------------------------- 
# --------------------------------------------------------------------------- 
# --------------------------------------------------------------------------- 
# --------------------------------------------------------------------------- 
# --------------------------------------------------------------------------- 
# --------------------------------------------------------------------------- 
def Test():
    class CUnSave(CState):
        m_Name = "UnSave"
        def __init__(self):
            super(CUnSave, self).__init__()

    class CSaveFinish(CState):
        m_Name = "SaveFinish"
        def __init__(self):
            super(CSaveFinish, self).__init__()

    class CCommitFinish(CState):
        m_Name = "CommitFinish"
        def __init__(self):
            super(CCommitFinish, self).__init__()

    class CAuditFinish(CState):
        m_Name = "AuditFinish"
        def __init__(self):
            super(CAuditFinish, self).__init__()

    class CTestModel(CModel):
        def __init__(self):
            super(CTestModel, self).__init__()
    
    pModel = CTestModel()
    # transitions = [
    #   {'event': '保存', 'source': '未保存', 'dest': '已保存' },
    #   {'event': '提交', 'source': '已保存', 'dest': '已提交' },
    #   {'event': '审核', 'source': '已提交', 'dest': '已审核' },
    # ]
    transitions = [
        {'event': 'event_save', 'source': CUnSave, 'dest': CSaveFinish },
        {'event': 'event_commit', 'source': CSaveFinish, 'dest': CCommitFinish },
        {'event': 'event_audit', 'source': CCommitFinish, 'dest': CAuditFinish },
    ]
    p = CFiniteStateMachine(model=pModel, transitions=transitions, initial_state=CUnSave)
    print(pModel.GetStateObj().GetStateName())
    p.Process('event_save')
    print(pModel.GetStateObj().GetStateName())
    p.Process('event_commit')
    print(pModel.GetStateObj().GetStateName())
    
    # output:
    # UnSave
    # SaveFinish
    # CommitFinish

if __name__ == '__main__':
    Test()