class BaseCheck(object):

    def check(self):
        pass

    def result(self):
        if self.check():
            return True
        else:
            return False


    def name(self):
        pass

    def description(self):
        pass