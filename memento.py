# TODO finish it
import copy


def Memento(obj, deep=False):
    state = (copy.copy, copy.deepcopy)[bool(deep)](obj.__dict__) ##backup original state of an object
    def Restore(): ##restore original state of an object
        obj.__dict__.clear()
        obj.__dict__.update(state)
    return Restore

class Transaction:
    """A transaction guard. This is realy just syntactic suggar arount a memento
    closure."""
    deep = False
    def __init__(self, *targets):
        self.targets = targets
        self.Commit()
    def Commit(self):##backup original state of objects
        self.states = [Memento(target, self.deep) for target in self.targets] 
    def Rollback(self):##restore original state of objects
        for state in self.states:
            state()

class transactional(object):
    """Adds transactional semantics to methods. Methods decorated with
    @transactional will rollback to entry state upon exceptions."""
    def __init__(self, method):
        self.method = method
    def __get__(self, obj, T):
        def transaction(*args, **kwargs):
            state = Memento(obj)##backup original state of an object
            try:
                return self.method(obj, *args, **kwargs)##call method eg:DoStuff
            except:
                state()##rollback or restore
                raise
        return transaction

if __name__ == '__main__':

   class NumObj(object):
      def __init__(self, value):
         self.value = value
      def __repr__(self):
         return '<%s: %r>' % (self.__class__.__name__, self.value)
      def Increment(self):
         self.value += 1
      @transactional
      def DoStuff(self):
         self.value = '1111' # <- invalid value
         self.Increment()    # <- will fail and rollback

   print
   n = NumObj(-1)
   print n
   t = Transaction(n)
   try:
      for i in range(3):
         n.Increment()
         print n
      t.Commit()##commit
      print '-- commited'
      for i in range(3):
         n.Increment()
         print n
      n.value += 'x' # will fail
      print n
   except:
      t.Rollback()##rollback or restore
      print '-- rolled back'
   print n
   print '-- now doing stuff ...'
   try:
      n.DoStuff()
   except:
      print '-> doing stuff failed!'
      import traceback
      traceback.print_exc(0)
      pass
   print n

"""
<saju_m> Which is the Originator, Caretaker and Memento in this example  ?
<lillis> saju_m: the memento is Memento, the caretacker I'd say is Transaction in this case (i.e. something which keeps check of all the memento object and their status
<lillis> saju_m: originator is NumObj
<lillis> i.e. the actual stateful object
<lillis> saju_m: think of it like "some value", "a thing that holds the current and older values, as well as methods to go back" and "something that keeps track of all the things that are holding the values" basically
<lillis> saju_m: Memento can be used to implement Undo operations for example
<lillis> you have a stack of all the actions performed and these actions contain a method to revert themselves
<lillis> then you just pop them off in run the .undo() or whatever
<lillis> saju_m: try to focus on why to implement them instead ;)
<lillis> that is, it's easier to understand a pattern if you understand its real world use
<lillis> make a calculator in the console, with undo
<lillis> where you can step back one operation at a time
<lillis> it shouldnt be too hard and allows you to try out the memento pattern for example
<saju_m> I this is the only way to implement memento design pattern in python ? https://github.com/gennad/Design-Patterns-in-Python/blob/master/memento.py
<lillis> saju_m: no, that focuses on transactions (which is often very useful with the pattern)
<lillis> but for example the undo/redo wouldn't be using transactions
<lillis> saju_m: you dont have to focus on the exact code too much, the idea is the same in all programming languages
<lillis> (or most)
"""