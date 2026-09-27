class ILifecycle:
    def step(self):
        pass
        
    def pause(self):
        pass
        
    def resume(self):
        pass

class IRuntime(ILifecycle):
    def run(self, task: str):
        pass
        
    def observe(self, observation: str):
        pass
        
    def snapshot(self):
        pass
        
    def restore(self, snapshot):
        pass
