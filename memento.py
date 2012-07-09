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
